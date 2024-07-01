from flask import Blueprint
from flask_restful import Api
from flask import request, jsonify

from .api import ResourcesTreeResource, LocationResource, LocationsResource, CadetResource, CadetsResource,\
    CadetStatisticsResource, GroupResource, GroupsResource, CourseResource, CoursesResource, FacultyResource, \
    FacultiesResource, PositionsResource


resources_bp = Blueprint('resources', __name__)
api = Api(resources_bp)

api.add_resource(ResourcesTreeResource, '/tree')
api.add_resource(LocationResource, '/locations/<location_id>')
api.add_resource(LocationsResource, '/locations')

api.add_resource(CadetResource, '/cadets/<cadet_id>')
api.add_resource(CadetsResource, '/cadets')
api.add_resource(CadetStatisticsResource, '/cadets/<cadet_id>/statistics')

api.add_resource(GroupResource, '/groups/<group_id>')
api.add_resource(GroupsResource, '/groups')

api.add_resource(CourseResource, '/courses/<course_id>')
api.add_resource(CoursesResource, '/courses')

api.add_resource(FacultyResource, '/faculties/<faculty_id>')
api.add_resource(FacultiesResource, '/faculties')

api.add_resource(PositionsResource, '/positions')
