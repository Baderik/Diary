from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,\
    RadioField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Email

from database.db import *

db = DB()
users_table = UsersTable(db.get_connection())


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired("Пожалуйста, введите ваш логин")])
    password = PasswordField('Пароль', validators=[DataRequired("Пожалуйста, введите ваш пароль")])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired("Пожалуйста, введите ваш логин")])
    email = StringField('Email', validators=[DataRequired("Пожалуйста, введите ваш email"),
                                             Email("Пожалуйста, введите ваш email")])
    password1 = PasswordField('Пароль', validators=[DataRequired("Пожалуйста, введите ваш пароль")])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired("Пожалуйста, повторите ваш пароль")])
    name = StringField('Имя', validators=[DataRequired("Пожалуйста, введите ваше имя")])
    surname = StringField('Фамилия', validators=[DataRequired("Пожалуйста, введите вашу фамилию")])
    age = IntegerField('Возраст', validators=[DataRequired("Пожалуйста, укажите ваш возраст")])
    sex = RadioField('Ваш пол', validators=[DataRequired("Пожалуйста, укажите пол")], choices=[("мужской", "Мужской"),
                                                                                               ("женский", "Женский")])
    submit = SubmitField('Зарегистрироваться')


class SettingsForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Пожалуйста, введите ваш email"),
                                             Email("Пожалуйста, введите ваш email")])
    password_old = PasswordField('Старый пароль')
    password1 = PasswordField('Новый пароль')
    password2 = PasswordField('Повторите пароль')
    name = StringField('Имя', validators=[DataRequired("Пожалуйста, введите ваше имя")])
    surname = StringField('Фамилия', validators=[DataRequired("Пожалуйста, введите вашу фамилию")])
    age = IntegerField('Возраст', validators=[DataRequired("Пожалуйста, укажите ваш возраст")])
    sex = RadioField('Ваш пол', validators=[DataRequired("Пожалуйста, укажите пол")],
                     choices=[("мужской", "Мужской"), ("женский", "Женский")], default='мужской')
    image = FileField('Выберите аватарку')
    submit = SubmitField('Сохранить')


class CreateClubForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired("Пожалуйста, введите название")])
    description = TextAreaField('Описание', validators=[DataRequired("Пожалуйста, опишите кружок")])
    address = StringField('Адрес', validators=[DataRequired("Пожалуйста, введите адрес проведения")])
    image = FileField('Выберите аватарку')

    monday = BooleanField('Понедельник')
    tuesday = BooleanField('Вторник')
    wednesday = BooleanField('Среда')
    thursday = BooleanField('Четверг')
    friday = BooleanField('Пятница')
    saturday = BooleanField('Суббота')
    sunday = BooleanField('Воскресенье')

    submit = SubmitField('Сохранить')
