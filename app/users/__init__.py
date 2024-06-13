from flask import Blueprint, jsonify
from flask_restful import Api
from .api import UserResource

users_bp = Blueprint('users', __name__)
api = Api(users_bp)

api.add_resource(UserResource, '/<username>')

