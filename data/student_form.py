from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class StudentForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Отчество (не обязательно)') 
    # здесь нужно поле для выбора класса
    submit = SubmitField('Применить')
