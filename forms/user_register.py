from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, InputRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login/email', validators=[DataRequired(), Email(), InputRequired()])
    password = PasswordField('Password', validators=[DataRequired(), InputRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired(), InputRequired()])
    surname = StringField('Surname', validators=[DataRequired(), InputRequired()])
    name = StringField('Name', validators=[DataRequired(), InputRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=80), InputRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField("Speciality")
    address = StringField("Address")
    submit = SubmitField('Submit')
