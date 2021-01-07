from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    '''register a user'''

    name = StringField('User Name', validators=[InputRequired()],)

    password = PasswordField('Password',validators=[InputRequired()],)

    email = StringField('Email', validators=[InputRequired(), Email()],)

    first_name = StringField('First Name', validators=[InputRequired()],)
    
    last_name = StringField('Last Name', validators=[InputRequired()],)

class LoginForm(FlaskForm):
    '''login a user'''

    name = StringField('User Name', validators=[InputRequired()],)

    password = PasswordField('Password',validators=[InputRequired()],)

class FeedbackForm(FlaskForm):
    '''add feedback to a user'''

    title = StringField('Title', validators=[InputRequired()],)

    content = StringField('Content', validators[InputRequired()])

class DeleteForm(FlaskForm):
