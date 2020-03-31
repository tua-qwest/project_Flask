from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class GroupForm(FlaskForm):
    group_name = StringField('Название класса/группы', validators=[DataRequired()])
    submit = SubmitField('Применить')
