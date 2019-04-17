from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField,\
    RadioField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from database.db import *

db = DB()
users_table = UsersTable(db.get_connection())


def no_comma(form, field):
    if ',' in field.data:
        raise ValidationError('В логине не должно быть запятых')


class LoginForm(FlaskForm):
    login = StringField('Логин', [DataRequired("Пожалуйста, введите ваш логин")])
    password = PasswordField('Пароль', [DataRequired("Пожалуйста, введите ваш пароль")])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    login = StringField('Логин', [DataRequired("Пожалуйста, введите ваш логин"),
                                  Length(4, 12, 'Логин должен быть длинной не меньше 4 и не больше 12'),
                                  no_comma])
    name = StringField('Имя', [DataRequired("Пожалуйста, введите ваше имя")])
    email = StringField('Email', [DataRequired("Пожалуйста, введите ваш email"),
                                  Email("Пожалуйста, введите ваш email")])
    surname = StringField('Фамилия', [DataRequired("Пожалуйста, введите вашу фамилию")])
    password1 = PasswordField('Пароль',
                              [DataRequired("Пожалуйста, введите ваш пароль"),
                               Length(7, 12, 'Пароль должен быть длинной не меньше 7 и не больше 12')])
    age = IntegerField('Возраст', [DataRequired("Пожалуйста, укажите ваш возраст")])
    password2 = PasswordField('Повторите пароль', [EqualTo('password1', 'Пароли не совпадают')])
    sex = RadioField('Ваш пол', [DataRequired("Пожалуйста, укажите пол")], choices=[("мужской", "Мужской"),
                                                                                               ("женский", "Женский")])
    submit = SubmitField('Зарегистрироваться')


class SettingsForm(FlaskForm):
    email = StringField('Email', [DataRequired("Пожалуйста, введите ваш email"),
                                  Email("Пожалуйста, введите ваш email")])
    password_old = PasswordField('Старый пароль')
    password1 = PasswordField('Новый пароль')
    password2 = PasswordField('Повторите пароль')
    name = StringField('Имя', [DataRequired("Пожалуйста, введите ваше имя")])
    surname = StringField('Фамилия', [DataRequired("Пожалуйста, введите вашу фамилию")])
    age = IntegerField('Возраст', [DataRequired("Пожалуйста, укажите ваш возраст")])
    sex = RadioField('Ваш пол', [DataRequired("Пожалуйста, укажите пол")],
                     choices=[("мужской", "Мужской"), ("женский", "Женский")], default='мужской')
    image = FileField('Выберите аватарку', [FileAllowed(['png'], 'Простите, но только png')])
    submit = SubmitField('Сохранить')


class CreateClubForm(FlaskForm):
    name = StringField('Название', [DataRequired("Пожалуйста, введите название")])
    description = TextAreaField('Описание', [DataRequired("Пожалуйста, опишите кружок")])
    address = StringField('Адрес', [DataRequired("Пожалуйста, введите адрес проведения")])
    image = FileField('Выберите аватарку', [FileAllowed(['png'], 'Простите, но только png')])

    monday = BooleanField('Понедельник')
    tuesday = BooleanField('Вторник')
    wednesday = BooleanField('Среда')
    thursday = BooleanField('Четверг')
    friday = BooleanField('Пятница')
    saturday = BooleanField('Суббота')
    sunday = BooleanField('Воскресенье')

    submit = SubmitField('Сохранить')


class ClubForm(FlaskForm):
    submit = SubmitField()


class ClubSettingsForm(FlaskForm):
    image = FileField('Выберите аватарку')
    StringField()
    name = StringField('Название', [DataRequired("Пожалуйста, введите название")])
    description = TextAreaField('Описание', [DataRequired("Пожалуйста, опишите кружок")])

    monday = BooleanField('Понедельник')
    tuesday = BooleanField('Вторник')
    wednesday = BooleanField('Среда')
    thursday = BooleanField('Четверг')
    friday = BooleanField('Пятница')
    saturday = BooleanField('Суббота')
    sunday = BooleanField('Воскресенье')

    submit = SubmitField('Сохранить')
