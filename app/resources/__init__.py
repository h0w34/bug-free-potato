from flask import Blueprint
from flask_restful import Api
from flask import request, jsonify

from .api import ResourcesListResource

resources_bp = Blueprint('resources', __name__)
api = Api(resources_bp)

api.add_resource(ResourcesListResource, '/list')

