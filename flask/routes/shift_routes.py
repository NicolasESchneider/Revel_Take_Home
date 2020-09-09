from flask import Blueprint, render_template, abort, request
from db import db, SQLALCHEMY_DATABASE_URI
from models.shift import Shift, ShiftSchema
from models.vehicle import Vehicle
from models.shift_index import ShiftIndex

from utils.path_finder import PathFinder

# ...query.order_by(collate(Table.column, 'ICU_EXT_1'))

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

@shift_page.route('/auto_shift/<int:latitude>/<int:longitude>', methods=['POST','PUT', 'GET'])
# only have get methods here for easy testing,
def automatic_shift_creation(latitude, longitude):
  # create the new shift
  new_shift = Shift(location_lat=latitude, location_long=longitude)
  db.session.add(new_shift)
  # instantiate the new shift. We need to get the ID to stamp our vehicles
  db.session.commit()
  # query for 20 nearest not in use/not fully charged vehicles
  target_data = db.session.execute(
    """SELECT *,
      SQRT(
        POW(69.1 * (location_lat - :lat), 2) +
        POW(69.1 * (location_long - :long) * COS(location_lat / 57.3), 2)
      ) AS distance
      FROM vehicle
      WHERE battery_level != 100.0
      AND shift_id IS NULL
      AND in_use = 'False'
      ORDER BY distance LIMIT 20"""
  , { 'lat': latitude, 'long': longitude })

  vehicles = []
  for v in target_data:
    vehicles.append(Vehicle(
      id = v.id,
      license_plate = v.license_plate,
      battery_level = v.battery_level,
      in_use = v.in_use,
      model = v.model,
      location_lat = v.location_lat,
      location_long = v.location_long,
      shift_id = new_shift.id,
      created_at = v.created_at,
    ))
  path = PathFinder(vehicles, new_shift)
  # pathing logic for vehicles goes HERE
  # then iterate through the newly sorted/pathed vehicles
  if len(vehicles) > 0:
    for i in range(0, len(vehicles)):
      # set the Vehicle.next_id to be the next vehicle
      if i < len(vehicles) - 1:
        db.session.query(Vehicle).filter(Vehicle.id == vehicles[i].id).update({
          'next_id': vehicles[i + 1].id,
          'shift_id': new_shift.id
        })
      else:
        db.session.query(Vehicle).filter(Vehicle.id == vehicles[i].id).update({
          'shift_id': new_shift.id
        })
    # create the shift_index row
    new_link = ShiftIndex(shift_id = new_shift.id, next_vehicle_id=vehicles[0].id)
    db.session.add(new_link)

  # commit all changes
  db.session.commit()
  return ShiftSchema().dump(new_shift)


@shift_page.route('/shifts', methods=['POST','PUT'])
def create_shift():
  new_shift = Shift()
  db.session.add(new_shift)
  db.session.commit()
  return ShiftSchema().dump(new_shift)
