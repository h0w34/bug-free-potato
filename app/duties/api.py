from app import db
from flask import jsonify
from flask_restful import Resource, Api, reqparse, abort
from .models import Duty, Location, DutyType
from .helpers import get_object_or_404
from datetime import datetime, date
from .services import update_schedule
from collections import defaultdict

duties_get_args = reqparse.RequestParser()
duties_get_args.add_argument('location_ids', type=int)

duty_post_args = reqparse.RequestParser()
duty_post_args.add_argument('date', type=date, required=True)
duty_post_args.add_argument('duty_type_id', type=int, required=True)
duty_post_args.add_argument('cadet_roles_ids', type=list, required=True)
duty_post_args.add_argument('location_ids', type=list, required=True)

duty_get_args = reqparse.RequestParser()
duty_get_args.add_argument('location_id', type=int, required=True)


# the main api: all the logic about the Roles etc is implemented here
# returns schedule for a specific user, grouped by locations

# TODO: user roles handling
class DutiesHomeApi(Resource):
    # return the schedule for a specified location
    def get(self):
        # assume the locations are fetched either by main_location in Cadet
        # or whatever for admins
        args = {'location_ids': [1, 2]}  # duty_get_args.parse_args()
        location_ids = args.get('location_ids')

        today = date.today()
        current_month = today.month
        current_year = today.year

        duties = Duty.query.all()  # filter(Duty.date >= date.today()).all()

        duties_by_location_type = defaultdict(lambda: defaultdict(dict))
        for duty in duties:
            location_id = duty.duty_type.location_id
            duty_type_id = duty.duty_type_id
            if location_id in location_ids:
                year = duty.date.year
                month = duty.date.month
                day = duty.date.day
                duties_by_location_type[location_id][duty_type_id].setdefault(year, defaultdict(dict))
                duties_by_location_type[location_id][duty_type_id][year].setdefault(month, defaultdict(dict))
                duties_by_location_type[location_id][duty_type_id][year][month][day] = duty.to_table_dict()

        response_data = {'locations': []}

        for location_id, duty_types in duties_by_location_type.items():
            location_data = Location.query.get(location_id).to_dict()
            location_data['duty_types'] = []
            for duty_type_id, data in duty_types.items():
                duty_type = DutyType.query.get(duty_type_id).to_table_dict()
                duties = {}
                for year, months in data.items():
                    for month, days in months.items():
                        duties.setdefault(year, {})[month] = days
                duty_type['duties'] = duties
                location_data['duty_types'].append(duty_type)
            response_data['locations'].append(location_data)

        return jsonify(response_data)

    # add a duty to a specific location (only for future dates)
    def post(self):
        args = duty_post_args.parse_args()

        duty_date = args['date']
        # Check if duty for the date already exists
        if Duty.query.filter_by(date=duty_date).first():
            abort(409, message=f"Duty for {duty_date} already exists.")

        duty = Duty(date=duty_date, duty_type_id=args['duty_type_id'])
        cadet_roles_ids = args['cadet_roles_ids']
        duty.create_duty(date=duty_date, duty_type_id=args['duty_type_id'], cadet_roles_ids=cadet_roles_ids)

        return {'message': f'Duty at {duty_date} created successfully'}, 201


# create a new event
class DutyApi(Resource):
    def get(self, duty_id):
        duty: Duty = get_object_or_404(Duty, id=duty_id)
        return duty.to_dict()

    def put(self, duty_id):
        duty: Duty = get_object_or_404(Duty, id=duty_id)
        if duty.archived:
            abort(400, message="Can't modify an archived duty.")
        # some hard validation logic to check if a user allowed to modify the duty or not
        return {'message': 'mock api'}

    def delete(self, duty_id):
        return {'message': 'mock api'}


# TODO: search API
class DutySearchApi(Resource):
    def get(self):
        return {'message': 'mock api'}

    def post(self):
        return {'message': 'mock api'}

    def put(self):
        return {'message': 'mock api'}


get_types_args = reqparse.RequestParser()
get_types_args.add_argument('duty_types_ids', type=list)

class DutyTypesApi(Resource):
    def get(self):
        args = duty_get_args.parse_args()
        duty_type_ids = args.getlist('duty_type_ids')
        types = [DutyType.query.get(type_id).to_dict() for type_id in duty_type_ids]
        return jsonify(types)

    def post(self):
        return {'message': 'mock api'}

    def put(self):
        return {'message': 'mock api'}


get_locations_args = reqparse.RequestParser()
get_locations_args.add_argument('location_ids', type=list)

class LocationsApi(Resource):
    def get(self):
        args = get_locations_args.parse_args()
        location_ids = args.getlist('location_ids')
        locations = [Location.query.get(location_id).to_dict() for location_id in location_ids]
        return jsonify(locations)

    def post(self):
        return {'message': 'mock api'}

    def put(self):
        return {'message': 'mock api'}