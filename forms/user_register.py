from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, InputRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=4, max=18), InputRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(
        min=8, max=45, message='Ваш пароль должен быть больше чем 7 символов'),
                                                   InputRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), InputRequired()])
    description = TextAreaField("Описание",
                                validators=[Length(min=0, max=500, message='Описание не может превышать 500 символов')])
    submit = SubmitField('Отправить')
