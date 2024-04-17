from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль',
                                 validators=[DataRequired(message="Это поле обязательно к заполнению."), InputRequired(message="Это поле обязательно к заполнению."), Length(
                                     min=8, max=45, message='Ваш пароль должен быть больше чем 7 символов')])
    password = PasswordField('Новый пароль', validators=[DataRequired(message="Это поле обязательно к заполнению."), InputRequired(message="Это поле обязательно к заполнению."), Length(
        min=8, max=45, message='Ваш пароль должен быть больше чем 7 символов')])
    password_again = PasswordField('Повтор нового пароля',
                                   validators=[DataRequired(message="Это поле обязательно к заполнению."), InputRequired(message="Это поле обязательно к заполнению."), Length(
                                       min=8, max=45, message='Ваш пароль должен быть больше чем 7 символов')])
    submit = SubmitField('Изменить пароль')
