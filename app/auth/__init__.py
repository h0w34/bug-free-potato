from flask import Blueprint, jsonify
from flask_restful import Api
from .api import UserRegistration, UserLogin, Protected, WhoAmI, RefreshTokens
from app.users import models
from app import jwt
from .models import RefreshSession

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(RefreshTokens, '/refresh')
api.add_resource(Protected, '/admin')
api.add_resource(WhoAmI, '/whoami')


'''# TODO: use separate model for access token block list  (????)
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = RefreshSession.query.filter_by(jti=jti).scalar()
    return token is not None'''

@jwt.user_identity_loader
def user_identity_lookup(user):
    print('loading identity: ', user, user.username)
    return user.username

# User lookup callback
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_headers, jwt_data):
    print('looking up identity from jwt:', jwt_data)
    identity = jwt_data['sub']
    print('looking up identity from jwt:', identity)
    return models.User.query.filter_by(username=identity).one_or_none()

'''# Additional claims
@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    return {'user_id': user.id}'''

# Error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({'message': 'Token has expired', 'error': 'token_expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'Signature verification failed', 'error': 'invalid_token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'message': 'Request doesnt contain valid token', 'error': 'authorization_header'}), 401
