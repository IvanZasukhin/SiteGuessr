import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String)  # описание
    games_played = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # количество сыгранных игр
    best_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # лучший счёт
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime)

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    games = orm.relationship("Game", back_populates='user')
    websites = orm.relationship("Website", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
