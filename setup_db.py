from app import db, Restaurant
import pandas as pd

def create():
    db.create_all()
    if Restaurant.query.first() is None:
        data = pd.read_csv('restaurantes.csv')
        for _, row in data.iterrows():
            restaurant = Restaurant(**row)
            db.session.add(restaurant)
        db.session.commit()

if __name__ == '__main__':
    create()