from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[InputRequired()])
