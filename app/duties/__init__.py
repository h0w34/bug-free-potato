from flask import Blueprint
from flask_restful import Api

from .api import DutiesHomeApi, DutyApi, DutyTypesApi, DutySuitableReservesApi, LocationsApi
from .views import some_view

duties_bp = Blueprint('duties', __name__)
api = Api(duties_bp)

api.add_resource(DutiesHomeApi, '/duties')
api.add_resource(DutyApi, '/duties/<duty_id>')
api.add_resource(DutySuitableReservesApi, '/duties/<duty_id>/reserves')
api.add_resource(DutyTypesApi, '/duty-types/<duty_type_ids>')
api.add_resource(LocationsApi, '/locations/<locations_ids>')

duties_bp.add_url_rule('/someview', view_func=some_view)
