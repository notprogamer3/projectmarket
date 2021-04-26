import datetime

import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Items(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    howm = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')