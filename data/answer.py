import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    __tablename__ = 'answer'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    mark = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now)
    id_student = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("student.id"))
    student = orm.relation('Student')
