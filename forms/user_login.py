from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, BooleanField, StringField
from wtforms.validators import DataRequired, Length, InputRequired, Email


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), InputRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=45), InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
