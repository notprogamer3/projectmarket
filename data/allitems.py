import datetime

import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Items1(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'allitems'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    howm = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
