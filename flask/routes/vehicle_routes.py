from flask import Blueprint, render_template, abort
from models.vehicle import Vehicle, VehicleSchema
from db import db

vehicle_page = Blueprint('vehicle_page', __name__)

@vehicle_page.route('/vehicles/<int:id>', methods=['GET'])
def show_vehicle(id):
  target_vehicle = Vehicle.query.get(id)
  return VehicleSchema().dump(target_vehicle)
  
@vehicle_page.route('/vehicles', methods=['GET'])
def list_vehicles():
  vehicles_schema = VehicleSchema(many=True)
  vehicles = Vehicle.query.all()
  return vehicles_schema.dumps(vehicles)


@vehicle_page.route('/swap/<int:id>', methods=['PATCH'])
# move the swap logic onto the Vehicle model. it will be called here, and within the shift logic
def swap_battery(id):
  target_vehicle = Vehicle.query.get(id)
  target_vehicle.battery_level = 100.0
  db.session.commit()
  return VehicleSchema().dump(target_vehicle)

@vehicle_page.route('/vehicles/<int:id>/shift/<int:shift_id>', methods=['PATCH'])
def add_to_shift(id, shift_id):
  target_vehicle = Vehicle.query.get(id)
  target_vehicle.shift_id = shift_id
  
  db.session.commit()
  return VehicleSchema().dump(target_vehicle)