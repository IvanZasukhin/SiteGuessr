from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин',
                        validators=[DataRequired(message="Некорректный логин"), Length(min=4, max=18),
                                    InputRequired(message="Некорректный логин")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Некорректный пароль"), Length(
        min=8, max=45, message='Ваш пароль должен быть больше чем 7 символов'),
                                                   InputRequired(message="Некорректный пароль")])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired(message="Некорректный пароль"),
                                               Length(min=8, max=45,
                                                      message='Ваш пароль должен быть больше чем 7 символов'),
                                               InputRequired(message="Некорректный пароль")])
    description = TextAreaField("Описание",
                                validators=[Length(min=0, max=500, message='Описание не может превышать 500 символов')])
    submit = SubmitField('Отправить')
