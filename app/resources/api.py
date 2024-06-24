import pprint

from app import db
from flask import jsonify
from flask_restful import Resource, reqparse, abort

from ..duties.models import Duty, Location, DutyType, Cadet, \
    ReplacementDoc, DutyReplacement, Faculty, Group

from datetime import datetime, date

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


# ------- resources APIs ------- #

# TODO: May add a special marking col depending on curr jwt showing if the resource is available or not
# or simply not to include it in json
class ResourcesListResource(Resource):
    def get(self):
        locations_data = []
        locations = Location.query.all()
        for location in locations:
            location_data = location.to_dict()
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

        return {'locations': locations_data}, 200