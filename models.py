from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    product_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

class Location(db.Model):
    location_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String, db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String, db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer, nullable=False)
