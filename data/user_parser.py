from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('description')
parser.add_argument('roles')
parser.add_argument('statistics')
parser.add_argument('roles')
parser.add_argument('banned')
parser.add_argument('statistics')
