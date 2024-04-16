import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Statistic(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'statistic'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=True, unique=True)
    total_games = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)  # общее количество сыгранных игр
    correct_answers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)  # количество правильных ответов
    wrong_answers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)  # количество неправильных ответов
    average_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)  # средний балл за игру
    best_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)  # лучший счёт

    user = orm.relationship('User')
