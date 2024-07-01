from pprint import pprint

from app import db
from flask import jsonify
from flask_restful import Resource, reqparse, abort

from ..duties.models import Duty, Location, DutyType, Cadet, \
    ReplacementDoc, DutyReplacement, Faculty, Group, Course, Rank, Position, PMCell, AKCell
from ..users.models import User
from ..users.helpers import generate_user
from datetime import datetime, date

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


# ------- resources APIs ------- #

# TODO: May add a special marking col depending on curr jwt showing if the resource is available or not
# or simply not to include it in json
class ResourcesTreeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_username(get_jwt_identity())

        university_data = {'name': 'Университет'}
        locations_data = []
        locations = Location.query.all()
        for location in locations:
            location_data = location.to_dict()
            location_data['pm_cells'] = [pm_cell.to_dict() for pm_cell in location.pm_cells]
            location_data['ak_cells'] = [ak_cell.to_dict() for ak_cell in location.ak_cells]

            faculties_data = []
            for faculty in location.faculties:
                faculty_data = faculty.to_dict()
                courses_data = []
                for course in faculty.courses:
                    course_data = course.to_dict()
                    groups_data = []
                    for group in course.groups:
                        group_data = group.to_dict()
                        cadets_data = [cadet.to_dict() for cadet in group.cadets]
                        group_data['cadets'] = cadets_data
                        groups_data.append(group_data)
                    course_data['groups'] = groups_data
                    courses_data.append(course_data)
                faculty_data['courses'] = courses_data
                faculties_data.append(faculty_data)
            location_data['faculties'] = faculties_data
            locations_data.append(location_data)

        university_data['locations'] = locations_data
        university_data['positions'] = [p.to_dict() for p in Position.query.order_by(Position.id.desc()).all()]
        # university_data['ranks'] = [r.to_dict() for r in Rank.query.filter(Rank.id <= user.cadet.rank_id).all()]
        university_data['ranks'] = [r.to_dict() for r in Rank.query.all()]
        return {'university': university_data}, 200


# TODO: consider removing
class PositionsResource(Resource):
    def get(self):
        return [p.to_dict() for p in Position.query.all()], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        position = Position(name=args.get('name'))

        db.session.add(position)
        db.session.commit()
        return {
           'message': f'Position {args.get("name")} successfully created',
           'location': position.to_dict()
        }, 201

# TODO: may add ranks resource (yet no real need since ranks dont change for years)


class CadetsResource(Resource):
    @jwt_required()
    def post(self):
        user: User = User.get_by_username(get_jwt_identity())

        print('Handling the request!!!')
        # cannot create a cadet with no user for user page support
        # the user for the cadet either generated or registered manually
        data = request.get_json()
        print('Got the data:', data)
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('surname', type=str, required=True)
        parser.add_argument('patronymic', type=str, required=False)
        parser.add_argument('sex', type=str, choices=['M', 'F'], required=True)
        parser.add_argument('rank_id', type=int, required=True)
        parser.add_argument('position_id', type=int, required=True)
        parser.add_argument('pm_cell_id', type=int, required=True)
        parser.add_argument('ak_cell_id', type=int)  # , required=True)
        # single group arg is sufficient
        parser.add_argument('group_id', type=int, required=True)

        parser.add_argument('username', type=str)
        args = parser.parse_args()
        print('Got the args!!!!')
        print('Got the args!!!!')
        print('Got the args!!!!')
        pprint(args)
        pprint(args)
        pprint(args)
        pprint(args)
        print(args)
        group = Group.query.get_or_404(args.get('group_id'), description='Group for the cadet not found')
        location = group.faculty.location

        new_user = None
        new_user_password = None

        if args.get('username'):
            user = User.get_by_username(args.get('username'))
            if user is None:
                abort(400, message=f'Cadet creation failed. User {args.get("username")} not found')
            if user.cadet is not None:
                abort(400, message=f'Cadet creation failed. User {args.get("username")} already has a linked cadet')
        else:
            try:
                new_user, new_user_password = generate_user()
            except:
                abort(400, message=f'Cadet creation failed when generating a user')

        if args.get('rank_id') not in [rank.id for rank in Rank.query.all()]:
            abort(400, message='Not valid rank_id')
        if args.get('position_id') not in [position.id for position in Position.query.all()]:
            abort(400, message='Not valid position_id')

        if args.get('pm_cell_id') not in [cell.id for cell in location.pm_cells]:
            abort(400, message=f'Not valid pm_cell_id for location {location.name}')

        if args.get('ak_cell_id') and args.get('ak_cell_id') not in [cell.id for cell in location.ak_cells]:
            abort(400, message=f'Not valid ak_cell_id for location {location.name}')

        # privilege level control
        if args.get('rank_id') > user.cadet.rank_id:
            abort(403, message='Not enough rights to perform this action')

        try:
            cadet = Cadet(
                name=args.get('name'),
                surname=args.get('surname'),
                patronymic=args.get('patronymic', None),
                sex=args.get('sex'),
                rank_id=args.get('rank_id'),
                position_id=args.get('position_id'),
                pm_cell_id=args.get('pm_cell_id'),
                ak_cell_id=args.get('ak_cell_id'),
                user=new_user,
                group=group,
                faculty=group.faculty,
                course=group.course
            )
            db.session.add_all([cadet, user])
            db.session.commit()

            response = {
                'message': f'Cadet at {cadet.group.name} group successfully created',
                'cadet': cadet.to_dict(),
            }
            if new_user_password:
                response['password'] = new_user_password

            return response, 201
        except:
            abort(500, message='Internal server error. Failed to create a cadet')


class CadetResource(Resource):
    def get(self, cadet_id):
        cadet = Cadet.query.get_or_404(cadet_id)
        return cadet.to_dict(), 200

    def put(self, cadet_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('patronymic', type=str)
        parser.add_argument('sex', type=str, choices=['M', 'F'])
        parser.add_argument('rank_id', type=int)
        parser.add_argument('position_id', type=int)
        parser.add_argument('pm_cell_id', type=int)
        parser.add_argument('ak_cell_id', type=int)
        # single group arg is sufficient
        parser.add_argument('group_id', type=int)

        parser.add_argument('username', type=str)
        args = parser.parse_args()

        cadet = Cadet.query.get_or_404(cadet_id)

        if 'group_id' in args:
            ...
        '''try:
            if 'group_id' in args:
                faculty = Faculty.query.get_or_404(args.get('faculty_id'))
                if course_id in [c.id for c in faculty.courses]:
                    abort(400, message=f'Cannot create a second {course_id} course for the {faculty.name} faculty')
                course.faculty = faculty
            if 'id' in args:
                if args.get('id') in [c.id for c in course.faculty.courses]:
                    abort(400, message=f'Cannot create a second {course_id} course for the same '
                                       f'{course.faculty.name} faculty')
                course.id = args.get('id')

            db.session.add(course)
            db.session.commit()
            return {
                       'message': f'Course {course_id} successfully modified',
                       'course': course.to_dict()
                   }, 200
        except:
            abort(500, message='Failed to edit the course')

    def delete(self, cadet_id):
        parser = reqparse.RequestParser()
        parser.add_argument('delete_cadets', type=bool)
        args = parser.parse_args()

        course = Course.query.get_or_404(course_id)
        if 'delete_cadets' in args and args.get('delete_cadets') is True:
            permitted_cadets = []
            for cadet in course.cadets:
                if cadet.future_duties:
                    permitted_cadets.append(cadet)
            if permitted_cadets:
                # if all(cadet.future_duties for cadet in group.cadets):
                abort(400, message='Cannot delete course as its cadets have active duties',
                      cadets_with_active_duties=[cadet.to_dict() for cadet in permitted_cadets])
            try:
                cadets = course.cadets
                db.session.delete(cadets)
                db.session.commit()
            except:
                abort(500, message='Failed to delete cadets for the course. Retreating...')
        try:
            db.session.delete(course)
            db.session.commit()
            return {'message': f'Course deleted successfully'}, 200

        except:
            abort(500, message='Failed to delete the course')'''


class LocationsResource(Resource):
    # create a location
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('address', type=str, required=True)
        args = parser.parse_args()

        try:
            location = Location(name=args.get('name'), address=args.get('address'))
            db.session.add(location)
            db.session.commit()
            return {
                       'message': f'Location {args.get("name")} successfully created',
                       'location': location.to_dict()
                   }, 201
        except:
            abort(500, message='Failed to create a location')


class LocationResource(Resource):
    def get(self, location_id):
        location = Location.query.get_or_404(location_id)
        return location.to_dict(), 200

    # edit a location
    def put(self, location_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('address', type=str)
        args = parser.parse_args()

        location = Location.query.get_or_404(location_id)
        try:
            if args.get('name'):
                location.name = args.get('name')
            if args.get('address'):
                location.address = args.get('address')

            db.session.commit()
            return {
               'message': f'Location {args.get("name")} successfully modified',
               'location': location.to_dict()
            }, 200
        except:
            abort(500, message='Failed to edit the location')

    def delete(self, location_id):
        parser = reqparse.RequestParser()
        parser.add_argument('delete_cadets', type=bool)
        args = parser.parse_args()

        location = Location.query.get_or_404(location_id)
        if args.get('delete_cadets'):  # and args.get('delete_cadets') is True:
            permitted_cadets = []
            for cadet in location.cadets:
                if cadet.future_duties:
                    permitted_cadets.append(cadet)
            if permitted_cadets:
                # if all(cadet.future_duties for cadet in group.cadets):
                abort(400, message='Cannot delete location as its cadets have active duties',
                      cadets_with_active_duties=[cadet.to_dict() for cadet in permitted_cadets])
            try:
                cadets = location.cadets
                db.session.delete(cadets)
                db.session.commit()
            except:
                abort(500, message='Failed to delete cadets for the location. Retreating...')

        try:
            db.session.delete(location)
            db.session.commit()
            return {'message': f'location deleted successfully'}
        except:
            abort(500, message='Failed to delete the location')


class FacultiesResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('location_id', type=int, required=True)
        args = parser.parse_args()

        location = Location.query.get_or_404(args.get('location_id'))
        try:
            faculty = Faculty(name=args.get('name'), location=location)
            db.session.add(faculty)
            db.session.commit()
            return {
               'message': f'Faculty {args.get("name")} successfully created',
               'faculty': faculty.to_dict()
            }, 201
        except:
            abort(500, message='Failed to create a faculty')


class FacultyResource(Resource):
    def get(self, faculty_id):
        faculty = Faculty.query.get_or_404(faculty_id)
        return faculty.to_dict(), 200

    def put(self, faculty_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('location_id', type=int)
        args = parser.parse_args()

        faculty = Faculty.query.get_or_404(faculty_id)
        try:
            if args('location_id'):
                location = Location.query.get_or_404(args.get('location_id'))
                faculty.location = location
            if args('name'):
                faculty.name = args.get('name')

            db.session.add(faculty)
            db.session.commit()
            return {
                       'message': f'Location {args.get("name")} successfully modified',
                       'faculty': faculty.to_dict()
                   }, 200
        except:
            abort(500, message='Failed to edit the faculty')

    def delete(self, faculty_id):
        parser = reqparse.RequestParser()
        parser.add_argument('delete_cadets', type=bool)
        args = parser.parse_args()

        faculty = Faculty.query.get_or_404(faculty_id)
        if args.get('delete_cadets'):  # and args.get('delete_cadets') is True:
            permitted_cadets = []
            for cadet in faculty.cadets:
                if cadet.future_duties:
                    permitted_cadets.append(cadet)
            if permitted_cadets:
                # if all(cadet.future_duties for cadet in group.cadets):
                abort(400, message='Cannot delete faculty as its cadets have active duties',
                      cadets_with_active_duties=[cadet.to_dict() for cadet in permitted_cadets])
            try:
                cadets = faculty.cadets
                db.session.delete(cadets)
                db.session.commit()
            except:
                abort(500, message='Failed to delete cadets for the faculty. Retreating...')
        try:
            db.session.delete(faculty)
            db.session.commit()
            return {'message': f'Faculty deleted successfully'}, 200

        except:
            abort(500, message='Failed to delete the faculty')


class CoursesResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('num', type=int, required=True)
        parser.add_argument('faculty_id', type=int, required=True)
        args = parser.parse_args()

        faculty = Faculty.query.get_or_404(args.get('faculty_id'))
        try:
            course = Course(num=args.get('num'), faculty=faculty)
            db.session.add(course)
            db.session.commit()
            return {
                   'message': f'Course {args.get("num")} at {faculty.name} faculty successfully created',
                   'course': course.to_dict()
                }, 201
        except:
            abort(500, message='Failed to create a course')


class CourseResource(Resource):
    def get(self, course_id):
        course = Course.query.get_or_404(course_id)
        return course.to_dict(), 200

    def put(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        parser.add_argument('faculty_id', type=int)
        args = parser.parse_args()

        course = Course.query.get_or_404(course_id)

        try:
            if args('faculty_id'):
                faculty = Faculty.query.get_or_404(args.get('faculty_id'))
                if course_id in [c.id for c in faculty.courses]:
                    abort(400, message=f'Cannot create a second {course_id} course for the {faculty.name} faculty')
                course.faculty = faculty
            if args.get('id'):
                if args.get('id') in [c.id for c in course.faculty.courses]:
                    abort(400, message=f'Cannot create a second {course_id} course'
                                            f' for the same {course.faculty.name} faculty')
                course.id = args.get('id')

            db.session.add(course)
            db.session.commit()
            return {
               'message': f'Course {course_id} successfully modified',
               'course': course.to_dict()
            }, 200
        except:
            abort(500, message='Failed to edit the course')

    def delete(self, course_id):
        parser = reqparse.RequestParser()
        parser.add_argument('delete_cadets', type=bool)
        args = parser.parse_args()

        course = Course.query.get_or_404(course_id)
        if args.get('delete_cadets'):  # and args.get('delete_cadets') is True:
            permitted_cadets = []
            for cadet in course.cadets:
                if cadet.future_duties:
                    permitted_cadets.append(cadet)
            if permitted_cadets:
                # if all(cadet.future_duties for cadet in group.cadets):
                abort(400, message='Cannot delete course as its cadets have active duties',
                      cadets_with_active_duties=[cadet.to_dict() for cadet in permitted_cadets])
            try:
                cadets = course.cadets
                db.session.delete(cadets)
                db.session.commit()
            except:
                abort(500, message='Failed to delete cadets for the course. Retreating...')
        try:
            db.session.delete(course)
            db.session.commit()
            return {'message': f'Course deleted successfully'}, 200

        except:
            abort(500, message='Failed to delete the course')


class GroupsResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('faculty_id', type=int, required=True)
        parser.add_argument('course_id', type=int, required=True)
        args = parser.parse_args()

        faculty = Faculty.query.get_or_404(args.get('faculty_id'))
        course = Course.query.get_or_404(args.get('course_id'))

        try:
            group = Group(name=args.get('name'), faculty=faculty, course=course)
            db.session.add(group)
            db.session.commit()
            return {
                'message': f'Group {args.get("name")} at {args.get("course_id")} course '
                            f'of {faculty.name} faculty successfully created',
                'group': group.to_dict()
            }, 201
        except:
            abort(500, message='Failed to create a group')



class GroupResource(Resource):
    def get(self, group_id):
        group = Group.query.get_or_404(group_id)
        return group.to_dict(), 200

    def put(self, group_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('faculty_id', type=int, required=True)
        parser.add_argument('course_id', type=int, required=True)
        args = parser.parse_args()

        group = Group.query.get_or_404(group_id)

        try:
            if args.get('name'):
                if args.get('faculty_id'):
                    faculty = Faculty.query.get_or_404(args.get('faculty_id'))
                    if args.get('name') in [g.name for g in faculty.groups]:
                        abort(400, message=f'Cannot have two {args.get("name")} groups for the {faculty.name} faculty')
                        group.faculty = faculty
                if args.get('course_id'):
                    course = Course.query.get_or_404(args.get('course_id'))
                    if args.get('name') in [g.name for g in course.groups]:
                        abort(400, message=f'Cannot have two {args.get("name")} groups for the same '
                                           f'{course.faculty.name} faculty')
                        group.course = course

                group.name = args.get('name')

            else:
                if args.get('faculty_id'):
                    faculty = Faculty.query.get_or_404(args.get('faculty_id'))
                    if group.name in [g.name for g in faculty.groups]:
                        abort(400, message=f'Cannot have two {group.name} groups for the {faculty.name} faculty')
                    group.faculty = faculty
                if args.get('course_id'):
                    course = Course.query.get_or_404(args.get('course_id'))
                    if group.name in [g.name for g in course.groups]:
                        abort(400, message=f'Cannot have two {group.name} groups for the same '
                                           f'{course.faculty.name} faculty')
                    group.course = course

            db.session.add(group)
            db.session.commit()

            return {
                   'message': f'Group {group.name} successfully modified',
                   'course': group.to_dict()
               }, 200
        except:
            abort(500, message='Failed to edit the group')

    def delete(self, group_id):
        parser = reqparse.RequestParser()
        parser.add_argument('delete_cadets', type=bool)
        args = parser.parse_args()

        group = Group.query.get_or_404(group_id)
        if args.get('delete_cadets'):  # and args.get('delete_cadets') is True:
            # must deal with all the planned duties
            permitted_cadets = []
            for cadet in group.cadets:
                if cadet.future_duties:
                    permitted_cadets.append(cadet)
            if permitted_cadets:
                # if all(cadet.future_duties for cadet in group.cadets):
                abort(400, message='Cannot delete group as its cadets have active duties',
                      cadets_with_active_duties=[cadet.to_dict() for cadet in permitted_cadets])
            try:
                cadets = group.cadets
                db.session.delete(cadets)
                db.session.commit()
            except:
                abort(500, message=f'Failed to delete cadets for the {group.name} group. Retreating...')
        try:
            db.session.delete(group)
            db.session.commit()
            return {'message': f'Group deleted successfully'}, 200

        except:
            abort(500, message='Failed to delete the group')
