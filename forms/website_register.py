from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, InputRequired, URL


class WebsiteRegisterForm(FlaskForm):
    name = StringField('Имя сайта', validators=[DataRequired(), Length(min=1, max=25), InputRequired()])
    url = URLField('Url сайта', validators=[DataRequired(), URL(message="Введите действительный URL-адрес.")])
    submit = SubmitField('Отправить')
