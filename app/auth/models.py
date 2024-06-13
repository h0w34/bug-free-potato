'''from app import db
from sqlalchemy import Column, Boolean, Enum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, DateTime
from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(), nullable=False)
    cadet_id = db.Column(db.Integer(), nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)
    last_seen = db.Column(DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()



    '''