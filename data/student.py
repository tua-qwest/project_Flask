import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'student'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_group = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("group.id"))
    student_group = orm.relation('Group')
