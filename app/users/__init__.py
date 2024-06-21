from flask import Blueprint, jsonify, send_from_directory, abort
from flask_restful import Api
from .api import UserResource, UserStatisticsResource, UserAdminResource, AvatarResource
from app.users.models import User

users_bp = Blueprint('users', __name__)
api = Api(users_bp)


'''# TODO: use user/avatar instead of static folder request
@users_bp.route('/<username>/avatar')
def send_avatar(username):
    user = User.get_by_username(username)
    if not user:
        abort(404, message=f'User {username} not found')

    return send_from_directory(app.static_folder, f'static/img/avatars/{user.avatar}')'''


api.add_resource(UserResource, '/<username>')
api.add_resource(UserStatisticsResource, '/<username>/statistics')
api.add_resource(UserAdminResource, '/admin')
api.add_resource(AvatarResource, '/<username>/avatar')
