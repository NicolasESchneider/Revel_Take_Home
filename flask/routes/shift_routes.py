from flask import Blueprint, render_template, abort, request
from models.shift import Shift, ShiftSchema
from models.vehicle import Vehicle, VehicleSchema
from db import db

shift_page = Blueprint('shift_page', __name__)

@shift_page.route('/shifts/<int:id>', methods=['GET'])
def show_shift(id):
  target_shift = Shift.query.get(id)
  vehicles = target_shift.vehicles
  return ShiftSchema().dump(target_shift)
  
@shift_page.route('/shifts', methods=['GET'])
def list_shifts():
  shifts_schema = ShiftSchema(many=True)
  shifts = Shift.query.all()
  return shifts_schema.dumps(shifts)

@shift_page.route('/shifts', methods=['POST','PUT'])
def create_shift():
  new_shift = Shift()
  db.session.add(new_shift)
  db.session.commit()
  return ShiftSchema().dump(new_shift)
