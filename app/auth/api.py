from pprint import pprint

import app
from app import db
from flask import jsonify, request
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import current_user, create_access_token, create_refresh_token, jwt_required, get_jti
from app.users.models import User
from random_username.generate import generate_username
from .models import RefreshSession
from datetime import datetime
from uuid import UUID


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
        parser.add_argument('login_input', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('fingerprint', type=str, required=False)

        args = parser.parse_args()

        print('ARGS!!!!!')
        pprint(args)
        print(args)

        if '@' in args.get('login_input'):
            user = User.get_by_email(args.get('login_input'))
        else:
            user = User.get_by_username(args.get('login_input'))

        if user and user.check_password(args.get('password')):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            refresh_token_jti = get_jti(refresh_token)
            fingerprint = args.get('fingerprint')
            # fingerprint_hash = sha256(fingerprint.encode()).hexdigest()

            # some security checks
            print(f'Fingerprint for user {user.username}: ', fingerprint)
            # delete all the previous sessions (and access tokens as well) if there's more than 5 current logins
            if RefreshSession.query.filter_by(user_id=user.id).count() >= 5:
                RefreshSession.query.filter_by(user_id=user.id).delete()
                db.session.commit()
                print(f'LOG (Security warning): > 5 refresh sessions for user {user.username}. Clearing them.')

            RefreshSession.create_for_user(user=user, jti=refresh_token_jti, ip=request.remote_addr,
                                           ua=request.headers.get('User-Agent'), fprint=fingerprint)
            user = user.to_dict()
            user['access_token'] = access_token
            user['refresh_token_jti'] = refresh_token_jti

            return {
                       "message": "Logged in",
                       "user": user
                   }, 200

        return {"error": "Invalid password or username"}, 400


class UserLogout(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('refresh_token', required=True)
        args = parser.parse_args()

        # ...


class RefreshTokens(Resource):
    # @jwt_required(refresh=True)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fingerprint', type=str, required=False)
        parser.add_argument('refresh_token_jti', type=str, required=True)
        args = parser.parse_args()
        print('data:', args.get('refresh_token_jti'))

        jti = UUID(args.get('refresh_token_jti'))

        refresh_session = RefreshSession.query.filter_by(refresh_token_jti=jti).first()
        # some token validity checks
        if not refresh_session:
            return {'message': 'No active refresh sessions for this token.', 'error': 'token_expired'}, 401
        elif refresh_session.expires_in < (datetime.now() - refresh_session.created_at).total_seconds():
            return {'message': 'Refresh token has expired', 'error': 'token_expired'}, 401

        user = refresh_session.user

        # remove all the old refresh sessions
        RefreshSession.query.filter_by(user_id=user.id).delete()

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        refresh_token_jti = get_jti(refresh_token)
        fingerprint = args.get('fingerprint')

        # create a new refresh session
        RefreshSession.create_for_user(user=user, jti=refresh_token_jti, ip=request.remote_addr,
                                       ua=request.headers.get('User-Agent'), fprint=fingerprint)
        return {
                   'message': 'Tokens refreshed successfully',
                   'access_token': access_token,
                   'refresh_token_jti': refresh_token_jti
               }, 200


class WhoAmI(Resource):
    @jwt_required()
    def get(self):
        return current_user.to_dict(), 200
