from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    signup = SubmitField('Sign up')

class TimerForm(FlaskForm):
    start_timer = SubmitField('Start timer')
    stop_timer = SubmitField('Stop timer')
    reset_timer = SubmitField('Reset timer')

class AddTaskForm(FlaskForm):
    title = StringField('Task title', validators=[DataRequired()])
    note = StringField('Note')
    add_task = SubmitField('Add task')
    cancel = SubmitField('Cancel')

class ChangeToTaskAddForm(FlaskForm):
    submit = SubmitField('Add new task')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email=StringField('Email')
    submit = SubmitField('Add me')
    login = SubmitField('Log in')