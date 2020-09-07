from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from vehicle_data import vehicle_data
from db.index import db
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)
ma = Marshmallow(app)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(80), unique=True, nullable=False)
    battery_level = db.Column(db.Float, nullable=False)
    in_use = db.Column(db.Boolean, nullable=False)
    model = db.Column(db.String(10), nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_long = db.Column(db.Float, nullable=False)


class VehicleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        model = Vehicle
        fields = ("id", "license_place", "battery_level",
                  "in_use", "location_lat", "location_long")


@app.cli.command("reset-db")
def reset_db():
    print(db)
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


@app.route('/vehicles')
def list_vehicles():
    vehicles_schema = VehicleSchema(many=True)
    vehicles = Vehicle.query.all()
    return vehicles_schema.dumps(vehicles)
