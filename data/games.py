import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=True)
    website_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scores = sqlalchemy.Column(sqlalchemy.Integer)
    finish_date = sqlalchemy.Column(sqlalchemy.DateTime)

    user = orm.relationship('User')
