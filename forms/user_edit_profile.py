from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional


class EditProfileForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=4, max=45), InputRequired()])
    description = TextAreaField("Описание", validators=[
        Optional(), Length(min=0, max=200, message='Описание не может превышать 200 символов')])
    role = SelectField("Роль", choices=["admin", "main admin", "newbie"], validators=[Optional(), ])
    total_games = IntegerField("Количество сыгранных игр", validators=[NumberRange(0, 10000), Optional(), ])
    correct_answers = IntegerField("Количество правильных ответов", validators=[NumberRange(0, 10000), Optional()])
    wrong_answers = IntegerField("Количество неправильных ответов", validators=[NumberRange(0, 10000), Optional()])
    average_score = FloatField("Средний балл за игру", validators=[Optional()])
    best_score = IntegerField("Лучший счёт", validators=[NumberRange(0, 10000), Optional()])
    submit = SubmitField('Сохранить изменения')
