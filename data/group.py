import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'group'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    group_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
