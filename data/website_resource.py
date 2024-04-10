from flask import abort, jsonify
from flask_restful import Resource

from . import db_session
from .website_parser import *
from .websites import Website


class WebsiteResource(Resource):
    def get(self, website_id):
        abort_if_websites_not_found(website_id)
        session = db_session.create_session()
        websites = session.query(Website).get(website_id)
        return jsonify({'websites': websites.to_dict(
            only=("id", "name", "url", "link_file", "user_id"))})

    def delete(self, website_id):
        abort_if_websites_not_found(website_id)
        session = db_session.create_session()
        websites = session.query(Website).get(website_id)
        session.delete(websites)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, website_id):
        args = parser.parse_args()
        abort_if_websites_not_found(website_id)
        session = db_session.create_session()
        websites = session.query(Website).get(website_id)
        websites.name = args['name']
        websites.url = args['url']
        websites.link_file = args['link_file']
        websites.user_id = args['user_id']
        session.commit()
        return jsonify({'success': 'OK'})


class WebsiteListResource(Resource):
    def get(self):
        session = db_session.create_session()
        websites = session.query(Website).all()
        return jsonify({'websites': [
            item.to_dict(
                only=("id", "name", "url", "link_file", "user_id")) for
            item in websites]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        websites = Website()
        websites.name = args['name']
        websites.url = args['url']
        websites.link_file = args['link_file']
        websites.user_id = args['user_id']
        session.add(websites)
        session.commit()
        return jsonify({'id': websites.id})


def abort_if_websites_not_found(website_id):
    session = db_session.create_session()
    websites = session.query(Website).get(website_id)
    if not websites:
        abort(404, message=f"Websites {website_id} not found")
