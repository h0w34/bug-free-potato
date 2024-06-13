from flask import Flask
from config import Config
##from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# auth imports
from flask_login import LoginManager
from flask_restful import Api
#from flask_rbac import RBAC
from flask_principal import Principal
from flask_cors import CORS
##from flask_jwt_extended import JWTManager

from .extensions import db, jwt, migrate


# logging errors by email imports
import logging
# logging to file
import os
from logging.handlers import RotatingFileHandler

# note how every flask-related extension needs the app object as argument
# initialize an app obj
app = Flask(__name__)
app.config.from_object(Config)
##api = Api(app)
CORS(app)
#CORS(app, resources={r"/*": {"origins": ["http://localhost:8080"]}})

# initialize extensions
db.init_app(app)
jwt.init_app(app)
migrate.init_app(app)


##db = SQLAlchemy(app)  # create a db entry point (could use an engine obj but this (actually a db engine is created)
# will also create an engine and session objects as db.session
#pg_db = SQLAlchemy(app, session_options={"bind": 'postgresql+psycopg2://mew:HelloKitty@localhost:5432/dutiesapp'})
##migrate = Migrate(app, db)
#pg_migrate = Migrate(app, pg_db)
##jwt = JWTManager(app)


'''login = LoginManager(app)
login.login_view = 'login'

principals = Principal(app)
'''

# register bps and initialize routes
from .duties import duties_bp
app.register_blueprint(duties_bp)
from .auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
from .users import users_bp
app.register_blueprint(users_bp, url_prefix='/users')

'''# initialize scheduler routes
from .duties.routes import initialize_routes
initialize_routes(duties_bp, api)'''

#from app import routes, models, errors  # Todo: replace this with a bp
print('imported everything))')



