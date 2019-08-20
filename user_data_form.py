from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UserDataForm(FlaskForm):
    surname = StringField('Фамилия')
    name = StringField('Имя')
    patronymic = StringField('Отчество')
    address = StringField('Адрес')
    counter_number = StringField('Номер счетчика')
    submit = SubmitField('Сохранить')
