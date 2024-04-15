from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, InputRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=4, max=18), InputRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=45), InputRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), InputRequired()])
    description = TextAreaField("Описание", validators=[Length(min=0, max=500)])
    submit = SubmitField('Отправить')
