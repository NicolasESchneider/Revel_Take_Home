from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

database_name = 'revel_takehome'
database_user = 'rev_admin'
database_password = 'rev2020'

SQLALCHEMY_DATABASE_URI = 'mysql://rev_admin:rev2020@localhost/revel_takehome'
db = SQLAlchemy()
ma = Marshmallow()
