from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flask_login import current_user
from blog_project.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Это имя занято. Пожалуйста, выберите другое.'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email.data).first()
        if user:
            raise ValidationError(
                'Этот email занят. Пожалуйста, выберите другой.'
            )


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    to_remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля', validators=[FileAllowed('jpg', 'png')])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Это имя занято. Пожалуйста, выберите другое.'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email.data).first()
        if user:
            raise ValidationError(
                'Этот email занят. Пожалуйста, выберите другой.'
            )


class RequestReserForm(FlaskForm):  # запрос на восст пароля проверяет тот ли это юзер
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Измеинть пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email не существует. Зарегистрируйтесь')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Введите пароль: ', validators=[DataRequired()])
    password_confirm = PasswordField('Подтвердите пароль: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Установить новый пароль')

