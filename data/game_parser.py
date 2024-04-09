from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True)
parser.add_argument('website_id', required=True, type=int)
parser.add_argument('scores', required=True, type=int)
