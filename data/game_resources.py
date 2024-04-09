from flask import abort, jsonify
from flask_restful import Resource

from . import db_session
from .games import Game
from .user_parser import *


class GameResource(Resource):
    def get(self, game_id):
        abort_if_games_not_found(game_id)
        session = db_session.create_session()
        game = session.query(Game).get(game_id)
        return jsonify({'user': game.to_dict(
            only=("id", "user_id", "website_id", "scores"))})

    def delete(self, game_id):
        abort_if_games_not_found(game_id)
        session = db_session.create_session()
        game = session.query(Game).get(game_id)
        session.delete(game)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, game_id):
        args = parser.parse_args()
        abort_if_games_not_found(game_id)
        session = db_session.create_session()
        game = session.query(Game).get(game_id)
        game.user_id = args['user_id']
        game.website_id = args['website_id']
        game.scores = args['scores']
        session.commit()
        return jsonify({'success': 'OK'})


class GameListResource(Resource):
    def get(self):
        session = db_session.create_session()
        game = session.query(Game).all()
        return jsonify({'users': [
            item.to_dict(
                only=("id", "user_id", "website_id", "scores")) for
            item in game]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        game = Game()
        game.user_id = args['user_id']
        game.website_id = args['website_id']
        game.scores = args['scores']
        session.commit()
        return jsonify({'id': game.id})


def abort_if_games_not_found(game_id):
    session = db_session.create_session()
    game = session.query(Game).get(game_id)
    if not game:
        abort(404, message=f"Game {game_id} not found")
