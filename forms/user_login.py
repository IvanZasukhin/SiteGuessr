from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired


# TODO: доделать description
class LoginForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired(), Length(min=3, max=100), InputRequired()])
    description = EmailField('О себе', validators=[DataRequired(), Length(min=3, max=500), InputRequired()])
    hashed_password = PasswordField('Пароль', validators=[DataRequired(), Length(min=3, max=100), InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
