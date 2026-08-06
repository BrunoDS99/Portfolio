from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-change-in-prod'

#Database Config
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'cafes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
db = SQLAlchemy(app)

#Cafe
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    location = db.Column(db.String(250))
    has_sockets = db.Column(db.Boolean, default = False)
    has_toilet = db.Column(db.Boolean, default = False)
    has_wifi = db.Column(db.Boolean, default = False)
    can_take_calls = db.Column(db.Boolean, default = False)
    seats = db.Column(db.String(50))
    coffee_price = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Cafe {self.name}'
    

@app.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)


@app.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
    
    