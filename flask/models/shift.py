from datetime import datetime
from db import db
from models.vehicle import VehicleSchema
from marshmallow import Schema, fields


class Shift(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
  location_lat = db.Column(db.Float, nullable=False)
  location_long = db.Column(db.Float, nullable=False)
  vehicles = db.relationship('Vehicle', backref='shift', lazy=True)
  link = db.relationship('ShiftIndex', backref='shift', lazy=True, cascade='all, delete-orphan')

class ShiftSchema(Schema):
  vehicles = fields.List(fields.Nested(VehicleSchema))
  class Meta:
    # Fields to expose
    model: Shift
    fields = ('id', 'vehicles', 'location_lat', 'location_long', 'created_at', 'updated_at')