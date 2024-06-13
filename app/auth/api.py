import pprint

from sqlalchemy.exc import SQLAlchemyError

from app import db
from flask import jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from app.users.models import User
from random_username.generate import generate_username


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
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        user = User.get_by_username(args.get('username'))

        if user and user.check_password(args.get('password')):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            return {
                    "message": "Logged in",
                    "tokens": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }, 200

        return jsonify({"error": "Invalid password or username"}), 400
