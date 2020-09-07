import os
import tempfile

import pytest

from app import app, db, Vehicle
from flask import json


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_list_vehicles_empty_db_empty_list(client):
    rv = client.get('/vehicles')
    assert len(json.loads(rv.data)) == 0


def test_list_vehicles_with_data(client):
    db.session.add(Vehicle(**{
        "id": 1,
        "license_plate": "NY0001",
        "battery_level": 90,
        "in_use": True,
        "model": "Niu",
        "location_lat": 40.680245,
        "location_long": -73.996955,
    }))
    db.session.commit()
    rv = client.get('/vehicles')
    assert len(json.loads(rv.data)) == 1
