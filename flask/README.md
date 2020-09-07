### Install

pip install -r requirements.txt

### reset db

FLASK_APP=app.py FLASK_ENV=development flask reset-db

### create vehicles

FLASK_APP=app.py FLASK_ENV=development flask create-vehicles

### run

FLASK_APP=app.py FLASK_ENV=development flask run

### get list of vehicles

http://127.0.0.1:5000/vehicles

### Tests

pytest
