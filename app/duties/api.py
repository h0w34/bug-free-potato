from app import db
from flask import jsonify
from flask_restful import Resource, Api, reqparse, abort
from .models import Duty, Location, DutyType, CadetDuty, Cadet
from .helpers import get_object_or_404
from datetime import datetime, date

from .services import generate_schedule, delete_duties, update_reserves
from collections import defaultdict

from flask import request

duties_post_args = reqparse.RequestParser()
duties_post_args.add_argument('start_date', type=str, help='Start date of the duty in ISO 8601 format')
duties_post_args.add_argument('end_date', type=str, help='Start date of the duty in ISO 8601 format')
duties_post_args.add_argument('location_ids', type=list)
duties_post_args.add_argument('duty_type_ids', type=list)

duties_delete_args = reqparse.RequestParser()
duties_delete_args.add_argument('start_date', type=str, help='Start date of the duty in ISO 8601 format')
duties_delete_args.add_argument('end_date', type=str, help='Start date of the duty in ISO 8601 format')
duties_delete_args.add_argument('location_ids', type=list)
duties_delete_args.add_argument('duty_type_ids', type=list)

duty_post_args = reqparse.RequestParser()
duty_post_args.add_argument('date', type=date, required=True)
duty_post_args.add_argument('duty_type_id', type=int, required=True)
duty_post_args.add_argument('cadet_roles_ids', type=list, required=True)
duty_post_args.add_argument('location_ids', type=list, required=True)

duty_get_args = reqparse.RequestParser()
duty_get_args.add_argument('location_id', type=int, required=True)


# the main api: all the logic about the Roles etc. (is) must be implemented here
# returns a schedule for a specific user grouped by locations and types
duties_get_args = reqparse.RequestParser()
duties_get_args.add_argument('location_ids', type=int)
# TODO: user roles handling
class DutiesHomeApi(Resource):
    # return the schedule for a specified location
    def get(self):
        # assume the locations are fetched either by main_location in Cadet
        # or whatever for admins
        args = request.args
        location_ids = [int(id) for id in request.args.getlist('location_ids')]
        today = date.today()
        current_month = today.month
        current_year = today.year

        duties = Duty.query.all()  # filter(Duty.date >= date.today()).all()

        duties_by_location_type = defaultdict(lambda: defaultdict(dict))
        for duty in duties:
            location_id = duty.duty_type.location.id
            duty_type_id = duty.duty_type_id
            #print(location_id)
            if location_id in location_ids:
                #print(location_id)
                year = duty.date.year
                month = duty.date.month
                day = duty.date.day
                duties_by_location_type[location_id][duty_type_id].setdefault(year, defaultdict(dict))
                duties_by_location_type[location_id][duty_type_id][year].setdefault(month, defaultdict(dict))
                duties_by_location_type[location_id][duty_type_id][year][month][day] = duty.to_table_dict()
        #print(duties_by_location_type[1])

        #response_data = {'locations': []}
        response_data = {'locations': []}
        for location_id in location_ids:
            #print('AAA', type(location_id))
            # print(f'location_id is {location_id}!')
            location_data = Location.query.get(location_id).to_dict()
            location_data['duty_types'] = []
            for duty_type_id, data in duties_by_location_type[location_id].items():
                #print(duty_type_id, data)
                duty_type = DutyType.query.get(duty_type_id).to_table_dict()
                duties = {}
                for year, months in data.items():
                    for month, days in months.items():
                        duties.setdefault(year, {})[month] = days
                duty_type['duties'] = duties
                location_data['duty_types'].append(duty_type)
            response_data['locations'].append(location_data)

        return jsonify(response_data)

    def post(self):
        args = duties_post_args.parse_args()
        result = generate_schedule(args['start_date'], args['end_date'], args['location_ids'], args['duty_type_ids'])
        print(result)
        return result

    def delete(self):
        args = duties_delete_args.parse_args()
        result = delete_duties(args['start_date'], args['end_date'], args['location_ids'], args['duty_type_ids'])
        print(result)
        return result


duty_put_args = reqparse.RequestParser()
duty_put_args.add_argument('replaced_id', type=int, required=True)
duty_put_args.add_argument('replacing_id', type=int, required=True)
duty_put_args.add_argument('reason', type=dict, required=True)
# CRUD for a single duty
class DutyApi(Resource):
    def get(self, duty_id):
        duty: Duty = get_object_or_404(Duty, id=duty_id)
        return duty.to_dict()

    # add a duty to a specific location (only for future dates)
    def put(self, duty_id):
        #print("aAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')")
        args = duty_put_args.parse_args()
        #print('THESE ATE THE ARGS:  ', args)
        duty: Duty = get_object_or_404(Duty, id=duty_id)
        replaced_cadet = get_object_or_404(Cadet, id=args['replaced_id'])
        replacing_cadet = get_object_or_404(Cadet, id=args['replacing_id'])

        '''json = {
            'replacement': {
                'replaced_id': 303,
                'replacing_id': 404,
                'reason': {
                    'type': 'sick',
                    'start_date': '2024-04-03',
                    'end_date': '2024-04-13'
                }
            }
        }'''
        duty.replace_cadets(args['replaced_id'], args['replacing_id'])
        if replacing_cadet in duty.reserve_cadets:
            duty.remove_reserve_cadet(args['replacing_id'])
            update_reserves(duty_id)

        print(f'replaced cadet {replaced_cadet.surname} with {replacing_cadet.surname}!')
        # if a reserve cadet is chosen:
        #  - remove the sick one
        #  - add reserved to the duty
        #  - update reserves for the duty

        # if the substitute cadet case:
        # - reserves kept alone
        # - add substitute one to the duty
        return {'message': 'Cadet replaced'}, 200, {
            'Access-Control-Allow-Origin': '*'
        }

    def post(self, duty_id):
        args = {}
        duty_date = args['date']
        # Check if duty for the date already exists
        if Duty.query.filter_by(date=duty_date).first():
            abort(409, message=f"Duty for {duty_date} already exists.")

        duty = Duty(date=duty_date, duty_type_id=args['duty_type_id'])
        cadet_roles_ids = args['cadet_roles_ids']
        duty.create_duty(date=duty_date, duty_type_id=args['duty_type_id'], cadet_roles_ids=cadet_roles_ids)

        duty: Duty = get_object_or_404(Duty, id=duty_id)
        if duty.archived:
            abort(400, message="Can't modify an archived duty.")
        # some hard validation logic to check if a user allowed to modify the duty or not
        return {'message': f'Duty at {duty_date} edited successfully'}, 201

    def delete(self, duty_id):
        return {'message': 'mock api'}


# TODO: implement for real
# for now assume that only cadets from the same location are available
class DutySuitableReservesApi(Resource):
    def get(self, duty_id):
        print('GETTING RESERVES FOR DUTY_ID: ', duty_id)
        duty: Duty = get_object_or_404(Duty, id=duty_id)
        role_id = request.args.get('role_id')
        try:
            role_id = int(role_id)
        except:
            return {'message': 'the role_id must be an integer value!'}, 400

        if role_id not in [role.id for role in duty.duty_roles]:
            return {'message': 'No role provided to find suitable reserves. Check your request args!'}, 400

        cadets = Cadet.query.all()
        permitted_pm_cells = [cadet_duty.cadet.pm_cell_id for cadet_duty in duty.cadet_duties if
                              cadet_duty.duty_role.id != role_id]
        # print('PERMITTED: ', permitted_pm_cells)
        suitable_cadets = []
        for cadet in cadets:
            if cadet.pm_cell_id not in permitted_pm_cells and cadet not in duty.reserve_cadets:
                suitable_cadets.append(cadet.to_dict())

        return jsonify(suitable_cadets)


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
