from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
#from app.models import User
from flask import jsonify

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate(db=db)
