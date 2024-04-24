from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class VerificationForm(FlaskForm):
    title = StringField('Отправить')
    submit = SubmitField('Отправить')
