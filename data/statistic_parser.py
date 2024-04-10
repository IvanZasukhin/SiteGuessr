from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True)
parser.add_argument('total_games', type=int)
parser.add_argument('correct_answers', type=int)
parser.add_argument('wrong_answers', type=int)
parser.add_argument('average_score', type=float)
parser.add_argument('best_score', type=int)
