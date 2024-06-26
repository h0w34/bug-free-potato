from flask import Blueprint
from flask_restful import Api

from .api import DutiesApi, DutyResource
from .views import some_view


def initialize_routes(bp: Blueprint, api: Api):
    api.add_resource(DutiesApi, '/duties')
    api.add_resource(DutyResource, '/duties/<duty_id>')

    bp.add_url_rule('/someview', some_view())
    # ...
