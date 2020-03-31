from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class MarkForm(FlaskForm):
    date = StringField('Дата в формате "Y-M-D" (по умолчанию текущая дата)')
    mark = IntegerField('Оценка', validators=[DataRequired()])
    submit = SubmitField('Применить')
