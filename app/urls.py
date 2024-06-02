# from .auth.api import ...
from .duties.api import DutyApi, DutiesApi, DutySearchApi
from app import api


def initialize_apis():
    api.add_resource(DutiesApi, '/duties')
    api.add_resource(DutyApi, '/duty/<int:duty_id>')
    api.add_resource(DutySearchApi, ...)

    # user apis registration

