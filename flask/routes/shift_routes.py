from flask import Blueprint, render_template, abort, request
from db import db, SQLALCHEMY_DATABASE_URI
from models.shift import Shift, ShiftSchema
from models.vehicle import Vehicle
from models.shift_index import ShiftIndex

from utils.path_finder import PathFinder

# ...query.order_by(collate(Table.column, 'ICU_EXT_1'))

shift_page = Blueprint('shift_page', __name__)

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


@shift_page.route('/shifts/<int:id>', methods=['GET'])
# view a shift/all vehicles in a shift
def show_shift(id):
  target_shift = Shift.query.get(id)
  return ShiftSchema().dump(target_shift)



@shift_page.route('/shifts/<int:id>/continue', methods=['PATCH'])
def perform_swap():
  target_shift = Shift.query.get(id)
  link = target_shift.link
  current_vehicle = Vehicle.query.get(link.next_vehicle_id)

  link.next_vehicle_id = current_vehicle.next_id
  current_vehicle.battery_level = 100.0

  db.session.commit()
  return


@shift_page.route('/shifts/<int:id>/complete', methods=['GET'])
def is_complete(id):
  res = { 'shift_complete': False }
  target_shift = Shift.query.get(id)
  link = target_shift.link
  if link.next_vehicle_id == None:
    res['shift_complete'] = True
  return res

@shift_page.route('shifts/<int:id>/check_v/<int:vehicle_id>', methods=['GET'])
def check_vehicle_swapped(id, vehicle_id):
  res = { 'swap_completed': True }
  target_shift = Shift.query.get(id)

  link = target_shift.link
  vehicles = target_shift.vehicles;

  vehicles_by_id = {}

  for v in vehicles:
    vehicles_by_id[v.id] = v

  if vehicle_id not in vehicles_by_id:
    # this vehicle is not in this shift
    abort(404)

  next_v = vehicles_by_id[link.next_vehicle_id]
  while next_v != None:
    if next_v.id == vehicle_id:
      res['swap_completed'] = False
      break
    next_v = vehicles_by_id[next_v.next_id]

  return res
  
  

    
@shift_page.route('/auto_shift/<int:latitude>/<int:longitude>', methods=['POST','PUT'])
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

  path = PathFinder(vehicles, new_shift).initial_route[1:len(vehicles) + 1]
  # pathing logic for vehicles goes HERE
  # currently employing nearest neighbor heuristic, need to hook up the Two_opt solution for further accuracy
  # then iterate through the newly sorted/pathed vehicles

  # not enough time to implement two_opt confidently. Will do further research and go over during onsite, currently just using Nearest Neighbor
  if len(path) > 0:
    for i in range(0, len(path)):
      # set the Vehicle.next_id to be the next vehicle
      current_vehicle_index = path[i] - 1
      if i < len(path) - 1:
        db.session.query(Vehicle).filter(Vehicle.id == vehicles[current_vehicle_index].id).update({
          'next_id': vehicles[path[i + 1] - 1].id,
          'shift_id': new_shift.id
        })
      else:
        db.session.query(Vehicle).filter(Vehicle.id == vehicles[current_vehicle_index].id).update({
          'shift_id': new_shift.id
        })
    # create the shift_index row
    new_link = ShiftIndex(shift_id = new_shift.id, next_vehicle_id=vehicles[path[0]].id)
    db.session.add(new_link)

  # # commit all changes
  db.session.commit()
  return ShiftSchema().dump(new_shift)