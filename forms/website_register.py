from flask_wtf import FlaskForm
from wtforms import PasswordField, URLField, SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, InputRequired, URL


class WebsiteRegisterForm(FlaskForm):
    name = StringField('Имя сайта', validators=[DataRequired(), Length(min=1, max=60), InputRequired()])
    url = URLField('Url сайта', validators=[DataRequired(),  URL(message="Введите действительный URL-адрес.")])
    submit = SubmitField('Отправить')
