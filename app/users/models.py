from app import db
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
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True, default=str(uuid4()))
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(), nullable=False)
    cadet_id = db.Column(db.Integer, ForeignKey('cadets.id'), nullable=True)

    password_hash = db.Column(db.String(256), nullable=False)
    last_seen = db.Column(DateTime, default=datetime.now(), nullable=True)

    cadet = relationship('Cadet', back_populates='user')

    # statistics props
    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_username(cls, username):
        username = username.lower()
        return cls.query.filter_by(username=username).first()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.strftime('%Y-%m-%d %H:%M:%S') if self.last_seen else None
        }
