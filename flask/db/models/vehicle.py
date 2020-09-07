from flask.db import db
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(80), unique=True, nullable=False)
    battery_level = db.Column(db.Float, nullable=False)
    in_use = db.Column(db.Boolean, nullable=False)
    model = db.Column(db.String(10), nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)
