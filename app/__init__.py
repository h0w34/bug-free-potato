from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# auth imports
from flask_login import LoginManager
from flask_restful import Api
#from flask_rbac import RBAC
from flask_principal import Principal
from flask_cors import CORS

# logging errors by email imports
import logging
# logging to file
import os
from logging.handlers import RotatingFileHandler

# note how every flask-related extension needs the app object as argument
# initialize an app obj
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
CORS(app, resources={r"/duties/*": {"origins": "*"}})
#CORS(app, resources={r"/*": {"origins": ["http://localhost:8080"]}})

# initialize extensions
db = SQLAlchemy(app)  # create a db entry point (could use an engine obj but this (actually a db engine is created)
# will also create an engine and session objects as db.session
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

principals = Principal(app)


# register bps and initialize routes
from .duties import duties_bp
app.register_blueprint(duties_bp)

'''# initialize scheduler routes
from .duties.routes import initialize_routes
initialize_routes(duties_bp, api)'''

from app import routes, models, errors  # Todo: replace this with a bp

print('imported everything))')

