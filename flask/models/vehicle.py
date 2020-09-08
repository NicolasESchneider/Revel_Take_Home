from datetime import datetime
from db import db, ma

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(80), unique=True, nullable=False)
    battery_level = db.Column(db.Float, nullable=False)
    in_use = db.Column(db.Boolean, nullable=False)
    model = db.Column(db.String(10), nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)
    # my changes Below here
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class VehicleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        model = Vehicle
        fields = ("id", "license_place", "battery_level",
                  "in_use", "location_lat", "location_long",
                  "shift_id", 'created_at', 'updated_at')
