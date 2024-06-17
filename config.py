import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = 'ac7350bc431baf5e15f11e09'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 172800  # 2 days

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_BINDS = {
        'db2': 'postgresql+psycopg2://mew:HelloKitty@localhost:5432/dutiesapp',
    }

    '''SQLALCHEMY_PG_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql+psycopg2://mew:HelloKitty@localhost:5432/dutiesapp'''
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    # mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
