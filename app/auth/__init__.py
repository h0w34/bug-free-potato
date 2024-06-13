from flask import Blueprint, jsonify
from flask_restful import Api
from .api import UserRegistration, UserLogin, Protected
from app.users import models
from app import jwt

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Protected, '/admin')

# User lookup callback
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_headers, jwt_data):
    identity = jwt_data['sub']
    return models.User.query.filter_by(username=identity).one_or_none()

# Additional claims
@jwt.additional_claims_loader
def make_additional_claims(identity):
    return {'user_id': identity.id}

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
