import datetime

from flask import abort, jsonify
from flask_restful import Resource

from . import db_session
from .statistic import Statistic
from .statistic_parser import *


class StatisticResource(Resource):
    def get(self, statistic_id):
        abort_if_user_not_found(statistic_id)
        session = db_session.create_session()
        statistic = session.query(Statistic).get(statistic_id)
        return jsonify({'statistic': statistic.to_dict(
            only=("id", "user_id", "total_games", "correct_answers",
                  "wrong_answers", "average_score", "best_score"))})

    def delete(self, statistic_id):
        abort_if_user_not_found(statistic_id)
        session = db_session.create_session()
        statistic = session.query(Statistic).get(statistic_id)
        session.delete(statistic)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, statistic_id):
        args = parser.parse_args()
        abort_if_user_not_found(statistic_id)
        session = db_session.create_session()
        statistic = session.query(Statistic).get(statistic_id)
        statistic.user_id = args['user_id']
        statistic.total_games = args['total_games']
        statistic.correct_answers = args['correct_answers']
        statistic.wrong_answers = args['wrong_answers']
        statistic.average_score = args['average_score']
        statistic.best_score = args['best_score']
        session.commit()
        return jsonify({'success': 'OK'})


class StatisticListResource(Resource):
    def get(self):
        session = db_session.create_session()
        statistic = session.query(Statistic).all()
        return jsonify({'statistic': [
            item.to_dict(
                only=("id", "user_id", "total_games", "correct_answers",
                      "wrong_answers", "average_score", "best_score")) for
            item in statistic]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        statistic = Statistic()
        statistic.user_id = args['user_id']
        statistic.total_games = args['total_games']
        statistic.correct_answers = args['correct_answers']
        statistic.wrong_answers = args['wrong_answers']
        statistic.average_score = args['average_score']
        statistic.best_score = args['best_score']
        session.add(statistic)
        session.commit()
        return jsonify({'id': statistic.id})


def abort_if_user_not_found(statistic_id):
    session = db_session.create_session()
    statistic = session.query(Statistic).get(statistic_id)
    if not statistic:
        abort(404, message=f"User {statistic_id} not found")
