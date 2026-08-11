from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(500))
    img_url = db.Column(db.String(500))
    location = db.Column(db.String(250))
    has_sockets = db.Column(db.Boolean, default=False)
    has_toilet = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    can_take_calls = db.Column(db.Boolean, default=False)
    seats = db.Column(db.String(50))
    coffee_price = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Cafe {self.name}>'
    
    def to_dict(self):
        """Convert cafe to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'map_url': self.map_url,
            'img_url': self.img_url,
            'has_wifi': self.has_wifi,
            'has_sockets': self.has_sockets,
            'has_toilet': self.has_toilet,
            'can_take_calls': self.can_take_calls,
            'seats': self.seats,
            'coffee_price': self.coffee_price
        }