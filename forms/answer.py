from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length, InputRequired, URL


class AnswerForm(FlaskForm):
    title = StringField('Имя сайта', validators=[DataRequired(), Length(min=1, max=20), InputRequired()])
    submit = SubmitField('Отправить')