import pprint

from app import db
from flask import jsonify
from flask_restful import Resource, reqparse, abort
from .models import Duty, Location, DutyType, Cadet, ReplacementDoc, DutyReplacement
from app.helpers import get_object_or_404
from datetime import datetime, date

from .services import generate_schedule, delete_duties, update_reserves
from collections import defaultdict

from flask import request
#from flask_jwt_extended import jwt_required

from .helpers import lock_duty, unlock_duty, is_locked_by

from app.users.models import User


# TODO: user roles handling
# TODO: use this one as a search endpoint so that the home page is one of the applications

class DutiesHomeResource(Resource):
    # return the schedule for a specified location
    # the main api: all the logic about the Roles etc. (is) must be implemented here
    # returns a schedule for a specific user grouped by locations and types
    parser = reqparse.RequestParser()
    parser.add_argument('location_ids', type=int)

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
            # print(location_id)
            if location_id in location_ids:
                # print(location_id)
                year = duty.date.year
                month = duty.date.month
                day = duty.date.day
                duties_by_location_type[location_id][duty_type_id].setdefault(year, defaultdict(dict))
                duties_by_location_type[location_id][duty_type_id][year].setdefault(month, defaultdict(dict))
                duties_by_location_type[location_id][duty_type_id][year][month][day] = duty.to_dict()

        response_data = {'locations': []}
        for location_id in location_ids:
            # print(f'location_id is {location_id}!')
            location_data = Location.query.get(location_id).to_dict()
            location_data['duty_types'] = []
            for duty_type_id, data in duties_by_location_type[location_id].items():
                # print(duty_type_id, data)
                duty_type = DutyType.query.get(duty_type_id).to_dict()
                duties = {}
                for year, months in data.items():
                    for month, days in months.items():
                        duties.setdefault(year, {})[month] = days
                duty_type['duties'] = duties
                location_data['duty_types'].append(duty_type)
            response_data['locations'].append(location_data)

        return jsonify(response_data)

    def generateDuties(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=str, help='Start date of the duty in ISO 8601 format')
        parser.add_argument('end_date', type=str, help='Start date of the duty in ISO 8601 format')
        parser.add_argument('location_ids', type=list)
        parser.add_argument('duty_type_ids', type=list)
        args = {}  # duties_generate_post_args.parse_args()
        result = generate_schedule(args['start_date'], args['end_date'], args['location_ids'], args['duty_type_ids'])
        print(result)
        return result

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('location_id', type=int)
        parser.add_argument('duty_type_id', type=int, required=True)
        parser.add_argument('cadet_roles_ids', type=list, required=True)

        args = parser.parse_args()
        duty_date = args['date']
        # Check if duty for the date already exists
        if Duty.query.filter_by(date=duty_date).first():
            abort(409, message=f"Duty for {duty_date} already exists.")

        if args['location_id']:
            location: Location = Location.query.get(args['location_id'])
            if args['duty_type_id'] not in location.duty_type_ids:
                abort(400, message=f"Failed to create a duty. Duty's type and location don't match!")

        duty = Duty()
        cadet_roles_ids = args['cadet_roles_ids']  # here is torubles how to parse it
        duty.create_duty(date=duty_date, duty_type_id=args['duty_type_id'], cadet_roles_ids=cadet_roles_ids)

        # some hard validation logic to check if a user is allowed to modify the duty
        # ...

        return {'message': f'Successfully created a duty at f{duty_date}'}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=str, help='Start date of the duty in ISO 8601 format')
        parser.add_argument('end_date', type=str, help='Start date of the duty in ISO 8601 format')
        parser.add_argument('location_ids', type=list)
        parser.add_argument('duty_type_ids', type=list)
        args = parser.parse_args()

        result = delete_duties(args['start_date'], args['end_date'], args['location_ids'], args['duty_type_ids'])
        print(result)

        return result


duty_put_args = reqparse.RequestParser()
duty_put_args.add_argument('replaced_id', type=int, required=True)
duty_put_args.add_argument('replacing_id', type=int, required=True)
# duty_put_args.add_argument('reason', type=dict, required=True)
# duty_put_args.add_argument('start_date', type=dict, required=False)  # assume we use the currdate
# duty_put_args.add_argument('reason', type=dict, required=True)
duty_put_args.add_argument('commentary', type=str, required=False)
# doc related stuff
duty_put_args.add_argument('replacement_doc', type=dict, required=False)
# duty_put_args.add_argument('doc_type_id', type=int, required=False)
'''duty_put_args.add_argument('doc_contents', type=int, required=False)
duty_put_args.add_argument('start_date', type=int, required=False)
duty_put_args.add_argument('end_date', type=int, required=False)'''

duty_get_args = reqparse.RequestParser()
duty_get_args.add_argument('location_id', type=int, required=True)


# CRUD for a single duty
class DutyResource(Resource):
    def get(self, duty_id):
        duty: Duty = get_object_or_404(Duty, id=duty_id)

        if duty.locked:
            # heck if it's the editing user updating his layout
            mock_user = User.query.first()
            if is_locked_by(duty_id, mock_user.id):
                return duty.to_dict()
            else:
                '''print('Error 423: trying to modify a locked duty')
                abort(423, message="The duty is currently being modified!")'''
                # TODO: consider separating editing and fetching info apis
                return duty.to_dict(), 423

        '''mock_user = User.query.first()
        print(f'> Duty {duty_id} locked by {mock_user.id}')
        lock_duty(duty_id, mock_user.id)'''

        return duty.to_dict()

    # used only to update reserves??
    def put(self, duty_id):
        args = duty_put_args.parse_args()
        duty: Duty = get_object_or_404(Duty, id=duty_id)

        if duty.archived:
            print('Error 404: trying to modify an archived duty')
            abort(400, message="Can't modify an archived duty.")

        elif duty.locked:
            # TODO get the actual user identity
            mock_user = User.query.first()
            if not is_locked_by(duty_id, mock_user.id):
                print('Error 423: trying to modify a locked duty')
                abort(423, message="The duty is currently being modified!")

        pprint.pprint(args)
        replaced_cadet = get_object_or_404(Cadet, id=args['replaced_id'])
        replacing_cadet = get_object_or_404(Cadet, id=args['replacing_id'])
        role_id = next((cd.duty_role_id for cd in duty.cadet_duties if cd.cadet_id == args['replaced_id']), None)
        print('role_id', role_id)
        try:
            duty.replace_cadets(args['replaced_id'], args['replacing_id'])
            if replacing_cadet in duty.reserve_cadets:
                duty.remove_reserve_cadet(args['replacing_id'])
                update_reserves(duty_id)
        except:
            abort(500, message='Internal server error while replacing cadets')

        # creating a replacement entry
        replacement = DutyReplacement(duty_id=duty_id,
                                        replaced_id=args['replaced_id'], replacing_id=args['replacing_id'],
                                        duty_role_id=role_id, commentary=args.get('commentary', None))

        print(f'Created a replacement {replacement}!')
        replacement_doc_data = args['replacement_doc']
        print('replacement doc:', replacement_doc_data)
        if replacement_doc_data:
            if not (replacement_doc_data['start_date']):  # and replacement_doc_data['doc_type_id']):
                abort(400, message='No required replacement doc properties provided')

            start_date = datetime.strptime(replacement_doc_data['start_date'], '%Y-%m-%d').date()  # from str to datetime

            end_date = replacement_doc_data.get('end_date', None)

            if end_date:
                end_date = datetime.strptime(replacement_doc_data['end_date'], '%Y-%m-%d').date()
                if start_date > end_date:
                    abort(400, message='End date cannot be before the start date')
                    print('date order error')
                if end_date < duty.date:
                    abort(400, message="Whoah! This doc wont work! It's useless.")
                    print('doc error')
            else:
                if start_date > duty.date:
                    abort(400, message="Whoah! This doc wont work! It's useless.")
                    print('doc error')

            # TODO: allow not to specify the end date

            doc = ReplacementDoc(cadet_id=args['replaced_id'], start_date=start_date,
                                 end_date=end_date, contents=replacement_doc_data.get('contents', None))
            db.session.add(doc)
            db.session.commit()
            print('doc_id:', doc.id)
            print(replacement)
            replacement.replacement_doc_id = doc.id

            # TODO: some hard logic to exclude the cadet from participating in duties
            db.session.add(doc)
        db.session.add(replacement)
        db.session.commit()

        print(f'replaced cadet {replaced_cadet.surname} with {replacing_cadet.surname}!')

        return {'message': 'Cadet replaced'}, 200

    # used to execute actions on a duty
    def patch(self, duty_id):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True)
        args = parser.parse_args()
        print("WELCOME AT PATCH!!!!!!!!!!")
        duty = get_object_or_404(Duty, id=duty_id)
        if args['action'] == 'lock':
            # TODO use the current user identity instead
            mock_user = User.query.first()
            print(f'> Duty {duty_id} locked by {mock_user.id}')
            lock_duty(duty_id, mock_user.id)
            return {'message': f'Duty {duty_id} locked successfully'}, 200
        elif args['action'] == 'unlock':
            # TODO use the current user identity instead
            mock_user = User.query.first()
            print(f'> Duty {duty_id} unlocked by {mock_user.id}')
            unlock_duty(duty_id, mock_user.id)
            return {'message': f'Duty {duty_id} unlocked successfully'}, 200
        else:
            abort(400, message='Unknown action')

    def delete(self, duty_id):
        duty = get_object_or_404(Duty, id=duty_id)
        try:
            db.session.delete(duty)
        except:
            abort(500, message='Failed to delete duty')


'''class UnlockDutyResource(Resource):
    def post(self, duty_id):
        # TODO use the current user identity instead
        mock_user = User.query.first()
        print(f'> Duty {duty_id} unlocked by {mock_user.id}')
        unlock_duty(duty_id, mock_user.id)
        return {'message': f'Duty {duty_id} unlocked successfully'}, 200'''


# TODO: implement for real
# for now assume that only cadets from the same location are available
# /api/duty/<id>/reserves, role_id in query
class SuitableReservesResource(Resource):
    def get(self, duty_id):
        print('GETTING RESERVES FOR DUTY_ID: ', duty_id)
        duty: Duty = Duty.query.get_or_404(duty_id)
        role_id = request.args.get('role_id')
        try:
            role_id = int(role_id)
        except:
            return {'message': 'the role_id must be an integer value!'}, 400

        if role_id not in [role.id for role in duty.duty_roles]:
            return {'message': 'No role provided to find suitable reserves. Check your request args!'}, 400

        '''cadet = duty.get_cadet_by_role_id(role_id)
        if not cadet:
            abort(400, message='No cadet assigned to this role yet')'''

        cadets = Cadet.query.all()
        permitted_pm_cells = [cadet_duty.cadet.pm_cell_id for cadet_duty in duty.cadet_duties if
                              cadet_duty.duty_role.id != role_id]
        # print('PERMITTED: ', permitted_pm_cells)
        # todo some hard logic to find the suitable ones
        suitable_cadets = []
        for cadet in cadets:
            if cadet.pm_cell_id not in permitted_pm_cells and cadet not in duty.reserve_cadets:
                suitable_cadets.append(cadet.to_dict())

        reserves = duty.get_reserves_for_role(role_id)

        print(f'Got {len(suitable_cadets)} suitables and {len(reserves)} reserves for role_id {role_id}!')
        return jsonify({
            'reserves': [reserve.to_dict_short() for reserve in reserves],
            'suitable_cadets': suitable_cadets
        })


class ReplacementsHistoryResource(Resource):
    def get(self, duty_id):
        duty: Duty = get_object_or_404(Duty, id=duty_id)

        replacements = db.session.query(DutyReplacement).filter_by(duty_id=duty_id).\
            order_by(DutyReplacement.creation_date).all()
        print(f'Replacements for duty {duty_id}: ', replacements)

        if not replacements:
            abort(404, message='No replacements for this duty available')

        return jsonify([rpl.to_dict() for rpl in replacements])



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
