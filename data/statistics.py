import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Statistics(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'statistics'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), nullable=True, unique=True)
    total_games = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # общее количество сыгранных игр
    correct_answers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # количество правильных ответов
    wrong_answers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # количество неправильных ответов
    average_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # средний балл за игру
    best_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # лучший счёт

    user = orm.relationship('User')
