from flask import Blueprint
from flask_restful import Api
from flask import request, jsonify

from .api import DutiesHomeResource, DutyResource, DutyTypesApi, SuitableReservesResource, LocationsApi, \
    ReplacementsHistoryResource  # , UnlockDutyResource
from .views import some_view

duties_bp = Blueprint('duties', __name__)
api = Api(duties_bp)


@duties_bp.route('/simple', methods=['POST'])
def simple():
    args = request.args
    return 'jsonify(args)'


api.add_resource(DutiesHomeResource, '/duties')
api.add_resource(DutyResource, '/duties/<duty_id>')
# api.add_resource(UnlockDutyResource, '/duties/<duty_id>/unlock')
api.add_resource(SuitableReservesResource, '/duties/<duty_id>/reserves')
api.add_resource(ReplacementsHistoryResource, '/duties/<duty_id>/replacements')

api.add_resource(DutyTypesApi, '/duty-types/<duty_type_ids>')
api.add_resource(LocationsApi, '/locations/<locations_ids>')

duties_bp.add_url_rule('/someview', view_func=some_view)
