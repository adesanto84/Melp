from uuid import uuid4
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)


class Restaurant(db.Model):
    id = db.Column(db.String, primary_key=True)
    rating = db.Column(db.Integer)
    name = db.Column(db.String)
    site = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    street = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)


@app.route('/')
def index():
    return 'Hello, World! Testing Melp API'

@app.route('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    return {'restaurants': [{'id': restaurant.id, 'name': restaurant.name} for restaurant in restaurants]}

@app.route('/restaurants/<id>/info')
def get_restaurant_info(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return {'error': 'Restaurant not found'}, 404
    return {
        'name': restaurant.name,
        'rating': restaurant.rating,
        'site': restaurant.site,
        'email': restaurant.email,
        'phone': restaurant.phone,
        'street': restaurant.street,
        'city': restaurant.city,
        'state': restaurant.state,
        'lat': restaurant.lat,
        'lng': restaurant.lng
    }

@app.route('/restaurants/<id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    db.session.delete(restaurant)
    db.session.commit()
    return {'message': 'Restaurant deleted'}

@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.json
    # Verifico si se estan enviando todos los campos requeridos.
    required_fields = ['name', 'rating', 'site', 'email', 'phone', 'street', 'city', 'state', 'lat', 'lng']
    for field in required_fields:
        if data.get(field) is None or data[field] == '':
            return { 'error': f'{field.capitalize()} is required' }, 400
    
    field_validation = {
        'rating': lambda x: isinstance(x, int) and 0 <= x <= 4,
        'lat': lambda x: isinstance(x, float) and -90 <= x <= 90,
        'lng': lambda x: isinstance(x, float) and -180 <= x <= 180
    }
    
    for field, validation in field_validation.items():
        if field in data and not validation(data[field]):
            return { 'error': f'Invalid value for {field}' }, 400
    
    data['id'] = str(uuid4())
    
    restaurant = Restaurant(**data)
    db.session.add(restaurant)
    db.session.commit()
    return {'message': 'Restaurant created.', 'id': restaurant.id}, 201