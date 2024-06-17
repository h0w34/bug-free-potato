import app
from app import db
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt_extended import current_user, create_access_token, create_refresh_token, jwt_required, get_jwt_identity,\
    get_jti
from app.users.models import User
from random_username.generate import generate_username
from .models import RefreshSession
from datetime import datetime


class Protected(Resource):
    @jwt_required()
    def get(self):
        return jsonify({'message': 'heya'})


class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=False)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        user = User.get_by_username(username=args.get('username'))
        if user:
            abort(409, message=f'User {args["username"]} already exists')

        username = args.get('username', '')
        if not username:
            while True:
                username = generate_username(1)
                user = User.get_by_username(username)
                if not user:
                    break

        new_user = User(
            username=username.lower(),
            email=args.get('email')
        )

        new_user.set_password(password=args.get('password'))
        db.session.add(new_user)
        db.session.commit()

        return {'message': f'User {username} created'}, 201


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login_input', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        if '@' in args.get('login_input'):
            user = User.get_by_email(args.get('login_input'))
        else:
            user = User.get_by_username(args.get('login_input'))

        if user and user.check_password(args.get('password')):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            refresh_token_jti = get_jti(refresh_token)

            RefreshSession.create_for_user(user, refresh_token_jti, request.remote_addr)

            return {
                    "message": "Logged in",
                    "access_token": access_token,
                    "refresh_token_jti": refresh_token_jti
                }, 200

        return {"error": "Invalid password or username"}, 400


class UserLogout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('refresh_token', required=True)
        args = parser.parse_args()

        # ...


class RefreshTokens(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return {
            'refresh_token': refresh_token,
            'access_token': access_token
        }, 200




class WhoAmI(Resource):
    @jwt_required()
    def get(self):
        return current_user.to_dict(), 200
