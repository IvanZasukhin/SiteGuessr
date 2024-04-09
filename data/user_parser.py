from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('description')
parser.add_argument('games_played', type=int)
parser.add_argument('best_score', type=int)
parser.add_argument('hashed_password', required=True)
