from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

SQLALCHEMY_DATABASE_URI = 'mysql://rev_admin:rev2020@localhost/revel_takehome'

db = SQLAlchemy()
ma = Marshmallow()
