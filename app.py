from uuid import uuid4
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
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
    """
    Obtiene la lista de restaurantes en la base de datos.

    Devuelve:

    - Un diccionario con una lista de diccionarios con el ID y el nombre de cada restaurante.

    """
    restaurants = Restaurant.query.all()
    return {'restaurants': [{'id': restaurant.id, 'name': restaurant.name} for restaurant in restaurants]}

@app.route('/restaurants/<id>')
def get_restaurant_info(id):
    """
    Obtiene la información de un restaurante basado en su ID.

    Parámetros:
    - id: El ID del restaurante a buscar.

    Devuelve:
    - Un diccionario con la información del restaurante.

    Errores:
    - 404: Si el restaurante no se encuentra en la base de datos.
    """
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
    """
    Elimina un restaurante de la base de datos.

    Parámetros:
    - id: El ID del restaurante a eliminar.

    Devuelve:
    - Un diccionario con el mensaje 'Restaurant deleted'.
    """
    restaurant = Restaurant.query.get(id)
    db.session.delete(restaurant)
    db.session.commit()
    return {'message': 'Restaurant deleted'}

@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    """
    Crea un nuevo restaurante basado en los datos proporcionados en el body en formato json.

    Devuelve:
        Un diccionario con dos campos:
        - 'message': Una cadena que indica el estado de la operación.
        - 'id': El ID del restaurante creado.

    Errores:
        KeyError: Si falta alguno de los campos requeridos o están vacíos.
        ValueError: Si alguno de los campos tiene valores inválidos.
    """
    data = request.json

    # Verifico si se están enviando todos los campos requeridos.
    required_fields = ['name', 'rating', 'site', 'email', 'phone', 'street', 'city', 'state', 'lat', 'lng']
    for field in required_fields:
        if data.get(field) is None or data[field] == '':
            return { 'KeyError': f'{field.capitalize()} es requerido' }, 400
    
    field_validation = {
        'rating': lambda x: isinstance(x, int) and 0 <= x <= 4,
        'lat': lambda x: isinstance(x, float) and -90 <= x <= 90,
        'lng': lambda x: isinstance(x, float) and -180 <= x <= 180
    }
    
    for field, validation in field_validation.items():
        if field in data and not validation(data[field]):
            return { 'ValueError': f'Invalid value for {field}' }, 400
    
    data['id'] = str(uuid4())
    
    restaurant = Restaurant(**data)
    db.session.add(restaurant)
    db.session.commit()
    return {'message': 'Restaurant created.', 'id': restaurant.id}, 201

@app.route('/restaurants/<id>', methods=['PUT'])
def update_restaurant(id):
    """
    Actualiza un restaurante mediante el ID proporcionado utilizando los datos proporcionados en el body de la solicitud en formato json.

    Args:
        id (int): El ID del restaurante que se va a actualizar.

    Devuelve:
        dict: Un diccionario que contiene el mensaje de respuesta.

    Errores:
        ValueError: Si alguno de los valores de campo proporcionados es inválido.
        KeyError: Si el campo 'id' está incluido en el cuerpo de la solicitud.

    """
    data = request.json
    
    field_validation = {
        'rating': lambda x: isinstance(x, int) and 0 <= x <= 4,
        'lat': lambda x: isinstance(x, float) and -90 <= x <= 90,
        'lng': lambda x: isinstance(x, float) and -180 <= x <= 180
    }
    
    for field, validation in field_validation.items():
        if field in data and not validation(data[field]):
            return { 'ValueError': f'Invalid value for {field}' }, 400
    
    # Verifico si se envio el ID en el body
    if 'id' in data:
        return { 'KeyError': 'ID cannot be updated' }, 400
    
    restaurant = Restaurant.query.get(id)
    for key, value in data.items():
        setattr(restaurant, key, value)
    db.session.commit()
    return {'message': 'Restaurant updated'}

@app.route('/restaurants/statistics')
def search_restaurants():
    lat = request.args.get('latitude')
    lng = request.args.get('longitude')
    radius = request.args.get('radius')
    
    if not lat or not lng or not radius:
        return {'error': 'lat and lng and radius are required'}, 400
    
    lat = float(lat)
    lng = float(lng)
    radius = float(radius)

    point = f'POINT({lat} {lng})'
    geom = func.ST_GeomFromText(point, 4326)

    restaurants = Restaurant.query.filter(func.ST_DistanceSphere(
        geom,
        func.ST_SetSRID(func.ST_MakePoint(Restaurant.lat, Restaurant.lng), 4326)
    ) < radius).all()

    count = len(restaurants)
    if count == 0:
        return {'count': 0, 'avg': 0, 'std': 0}
    
    avg_rating = sum(restaurant.rating for restaurant in restaurants) / count
    std_dev = (sum((restaurant.rating - avg_rating)**2 for restaurant in restaurants) / count)**0.5

    return {'count': count, 'avg_rating': avg_rating, 'std_dev': std_dev}