from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

from models import db, Cafe
from scrape import scrape_cafes_from_osm, geocode_location, add_cafes_to_database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-change-in-prod'

#Database Config
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'cafes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
db.init_app(app)

#Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please Log In to access this page"

#Admin user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False) #to be stored as hash

    def __repr__(self):
        return f'<User {self.username}'
     
#User load for Flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#create table and add admin
with app.app_context():
    db.create_all()
    
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin123') #to be changed to hash
        db.session.add(admin)
        db.session.commit()
        print("Default Admin created!")

@app.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes, current_user=current_user)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form['name'],
            location=request.form['location'],
            map_url=request.form.get('map_url', ''),
            img_url=request.form.get('img_url', ''),
            has_wifi=bool(request.form.get('has_wifi', False)),
            has_sockets=bool(request.form.get('has_sockets', False)),
            has_toilet=bool(request.form.get('has_toilet', False)),
            can_take_calls=bool(request.form.get('can_take_calls', False)),
            seats=request.form.get('seats', ''),
            coffee_price=request.form.get('coffee_price', '')
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash('Cafe added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
@login_required
def delete_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    db.session.delete(cafe)
    db.session.commit()
    flash('Cafe deleted successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    
    if request.method == 'POST':
        cafe.name = request.form['name']
        cafe.location = request.form['location']
        cafe.map_url = request.form.get('map_url', '')
        cafe.img_url = request.form.get('img_url', '')
        cafe.has_wifi = bool(request.form.get('has_wifi', False))
        cafe.has_sockets = bool(request.form.get('has_sockets', False))
        cafe.has_toilet = bool(request.form.get('has_toilet', False))
        cafe.can_take_calls = bool(request.form.get('can_take_calls', False))
        cafe.seats = request.form.get('seats', '')
        cafe.coffee_price = request.form.get('coffee_price', '')
        
        db.session.commit()
        flash(f'Done ! "{cafe.name}" updated successfully!', 'success')
        
        return redirect(url_for('index'))

    return render_template('edit.html', cafe=cafe)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password: 
            login_user(user)
            flash('Log in successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid Username or Password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log out successful', 'info')
    return redirect(url_for('index'))
            

@app.route('/scrape', methods=['GET', 'POST'])
@login_required
def scrape_cafes():
    if request.method == 'POST':
        location = request.form.get('location')
        radius = int(request.form.get('radius', 10000))
        max_results = int(request.form.get('max_results', 25))
        
        if not location:
            flash('Please enter a location!', 'danger')
            return render_template('scrape.html')

        cafes_data = scrape_cafes_from_osm(location, radius, max_results)
        
        if not cafes_data:
            flash('No cafes found in that area! Try a different location.', 'warning')
            return render_template('scrape.html')
        
        added_count, skipped_count = add_cafes_to_database(cafes_data)
        if added_count > 0:
            flash(
                f'Added {added_count} new cafes from "{location}"! '
                f'({skipped_count} already existed)',
                'success'
            )
        else:
            flash(
                f'Found {len(cafes_data)} cafes but all already exist in your database.',
                'info'
            )
                
        return redirect(url_for('index'))
    
    return render_template('scrape.html')

@app.route('/api/cafes', methods=['GET'])
def api_get_cafes():
    cafes = Cafe.query.all()
    return jsonify([cafe.to_dict() for cafe in cafes])

@app.route('/api/cafe/<int:id>', methods=['GET'])
def api_get_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    return jsonify(cafe.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
    
    