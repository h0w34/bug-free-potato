import pprint

from sqlalchemy.exc import SQLAlchemyError

from app import db
from flask import jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from .models import User
from random_username.generate import generate_username


class UserResource(Resource):
    def get(self, username):
        user = User.get_by_username(username)
        if not user:
            print(f'NO USER! {username}')
            abort(404, message=f'User {username} doesnt exist')

        print(user)
        return {'user': user.to_dict(), 'cadet': user.cadet.to_dict()}


