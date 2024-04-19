from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd

app = Flask(__name__)
uri = os.getenv('DATABASE_URL')
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
    return {'restaurants': [{'name': restaurant.name, 'rating': restaurant.rating} for restaurant in restaurants]}
