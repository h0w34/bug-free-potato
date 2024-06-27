from flask import Blueprint
from flask_restful import Api
from flask import request, jsonify

from .api import ResourcesListResource, LocationResource, LocationsResource, CadetResource, CadetsResource,\
    GroupResource, GroupsResource, CourseResource, CoursesResource, FacultyResource, FacultiesResource


resources_bp = Blueprint('resources', __name__)
api = Api(resources_bp)

api.add_resource(ResourcesListResource, '/list')
api.add_resource(LocationResource, '/locations/<location_id>')
api.add_resource(LocationsResource, '/locations')
api.add_resource(CadetResource, '/cadets/<cadet_id>')
api.add_resource(CadetsResource, '/cadets')
api.add_resource(GroupResource, '/groups/<group_id>')
api.add_resource(GroupsResource, '/groups')
api.add_resource(CourseResource, '/courses/<course_id>')
api.add_resource(CoursesResource, '/courses')
api.add_resource(FacultyResource, '/faculties/<faculty_id>')
api.add_resource(FacultiesResource, '/faculties')

