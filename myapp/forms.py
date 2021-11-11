from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class StartTimerForm(FlaskForm):
    start_timer = SubmitField('Start timer')
class StopTimerForm(FlaskForm):    
    stop_timer = SubmitField('Stop timer')
class ResetTimerForm(FlaskForm):    
    reset_timer = SubmitField('Reset timer')

class AddTaskForm(FlaskForm):
    title = StringField('Task title', validators=[DataRequired()])
    note = StringField('Note')
    add_task = SubmitField('Add task')


class CancelAddForm(FlaskForm):
    cancel = SubmitField('Cancel')

class ChangeToTaskAddForm(FlaskForm):
    submit = SubmitField('Add new task')