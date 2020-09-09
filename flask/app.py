from flask import Flask
from vehicle_data import vehicle_data

from db import db, ma, SQLALCHEMY_DATABASE_URI

from models.vehicle import Vehicle
from models.shift import Shift
from models.shift_index import ShiftIndex

from routes.vehicle_routes import vehicle_page
from routes.shift_routes import shift_page

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
ma.init_app(app)

# register all blueprintes

app.register_blueprint(vehicle_page)
app.register_blueprint(shift_page)

@app.cli.command("reset-db")
def reset_db():
    db.drop_all()
    db.create_all()


@app.cli.command("create-vehicles")
def create_vehicles():
    for vehicle in vehicle_data:
        db.session.add(Vehicle(**vehicle))
    db.session.commit()

@app.route('/')
def hello_world():
    return 'Hello, World!'