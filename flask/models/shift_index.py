from datetime import datetime
from db import db
from marshmallow import Schema

class ShiftIndex(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'))
  next_vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class ShiftIndexSchema(Schema):
  class Meta:
    model = ShiftIndex
    fields = ('id','shift_id', 'next_vehicle_id', 'created_at', 'updated_at')