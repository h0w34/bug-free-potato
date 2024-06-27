from app import db
from sqlalchemy import Column, Boolean, Enum
from sqlalchemy import ForeignKey, UniqueConstraint, UUID
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
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(), nullable=True)
    cadet_id = db.Column(db.Integer, ForeignKey('cadets.id'), nullable=True)

    password_hash = db.Column(db.String(256), nullable=False)
    last_seen = db.Column(DateTime, default=datetime.now(), nullable=True)
    refresh_sessions = relationship('RefreshSession', back_populates='user')

    avatar = db.Column(db.String(120), nullable=True, default='default_avatar.gif')

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

    @classmethod
    def get_by_email(cls, email):
        email = email.lower()
        return cls.query.filter_by(email=email).first()

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'last_seen': self.last_seen.strftime('%Y-%m-%d %H:%M:%S') if self.last_seen else None,
            'avatar': {
                'url': self.avatar
            },
            'cadet': self.cadet.to_dict_short()
        }

    def to_dict_short(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'last_seen': self.last_seen.strftime('%Y-%m-%d %H:%M:%S') if self.last_seen else None,
            'avatar': {
                'url': self.avatar
            }
        }
