from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# auth imports
from flask_login import LoginManager
from flask_restful import Api, Resource
#from flask_rbac import RBAC
from flask_principal import Principal


# logging errors by email imports
import logging
from logging.handlers import SMTPHandler
# logging to file
import os
from logging.handlers import RotatingFileHandler

# note how every flask-related extension needs the app object as argument
# initialize an app obj
app = Flask(__name__)
app.config.from_object(Config)

# initialize extensions
db = SQLAlchemy(app)  # create a db entry point (could use an engine obj but this (actually a db engine is created)
# will also create an engine and session objects as db.session
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

principals = Principal(app)

# email logging
'''if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
'''

# file logging
if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors

print(db.__dict__)
print('imported everything))')
