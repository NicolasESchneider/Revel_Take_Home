from datetime import datetime
from db import db
from models.vehicle import VehicleSchema
from marshmallow import Schema, fields


class Shift(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  index = db.Column(db.Integer, default=0)
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
  vehicles = db.relationship('Vehicle', backref='shift', lazy=True)

class ShiftSchema(Schema):
  vehicles = fields.List(fields.Nested(VehicleSchema))
  class Meta:
    # Fields to expose
    model: Shift
    fields = ('id', 'index', 'vehicles', 'created_at', 'updated_at')