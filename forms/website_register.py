from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, InputRequired, URL, Optional


class WebsiteRegisterForm(FlaskForm):
    name = StringField('Имя сайта',
                       validators=[Length(min=1, max=25), Optional()])
    url = URLField('Url сайта', validators=[DataRequired(message="Это поле обязательно к заполнению."),
                                            InputRequired(message="Это поле обязательно к заполнению."),
                                            URL(message="Введите действительный URL-адрес.")])
    submit = SubmitField('Отправить')
