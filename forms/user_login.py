from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired, Length, InputRequired


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), InputRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(
        min=8, max=45, message='Ваш пароль должен быть больше чем 7 символов'),
                                                   InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
