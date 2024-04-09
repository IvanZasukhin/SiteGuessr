import datetime

from flask import abort, jsonify
from flask_restful import Resource

from . import db_session
from .users import User
from .user_parser import *


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=(
                "id", "login", "description", "games_played", "best_score", "created_date",
                "modified_date"))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = parser.parse_args()
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.login = args['login']
        user.description = args['description']
        user.games_played = args['games_played']
        user.best_score = args['best_score']
        user.modified_date = datetime.datetime.now()
        user.set_password(args['hashed_password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'users': [
            item.to_dict(
                only=("id", "login", "description", "games_played", "best_score", "created_date",
                      "modified_date")) for
            item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.login = args['login']
        user.description = args['description']
        user.games_played = args['games_played']
        user.best_score = args['best_score']
        user.modified_date = datetime.datetime.now()
        user.created_date = datetime.datetime.now()
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
