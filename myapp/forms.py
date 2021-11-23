from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    '''
    Controling login related feature fields

        Form fields:
            username (str)      a string field indicate username
            password (str)      a string field indicate password 
            remember_me (bool)  a boolean field to indicate if user want to remember the loged in session
            submit              a submit field when user click Sign in
            signup              a submit field when user click Sign up
    '''
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    signup = SubmitField('Sign up')

class TimerForm(FlaskForm):
    '''
    this form class control the timer buttons to start, stop, and reset the timer

        Form fields:
            start_timer         a submit field when user click Start timer
            stop_timer          a submit field when user click Stop timer
            reset_timer         a submit field when user click Reset timer
    '''
    start_timer = SubmitField('Start timer')
    stop_timer = SubmitField('Stop timer')
    reset_timer = SubmitField('Reset timer')

class ChangeTimerForm(FlaskForm):
    '''
    this form class will control the toggle between break timer and task timer

        Form fields:
            task_timer           a submit field when user click Task timer
            break_timer          a submit field when user click Break timer
    '''
    task_timer = SubmitField('Task timer')
    break_timer = SubmitField('Break timer')

class AddTaskForm(FlaskForm):
    '''
    this form class will control the add task form
        
        Form fields:
            title (str)         a string field indicate title of task
            note (str)          a string field indicates note of task
            add_task            a submit field triggered when user hit Add task
            cancel              a submit field triggered when user hit Cancel
    '''
    title = StringField('Task title')
    note = StringField('Note')
    add_task = SubmitField('Add task')
    cancel = SubmitField('Cancel')

class ChangeToTaskAddForm(FlaskForm):
    '''
    this form class will toggle the add task form 

        Form fields:
            submit              a submit field triggered when user click Add new task
    '''
    submit = SubmitField('Add new task')

class EditTaskForm(FlaskForm):
    '''
    this form class will control the edit task form, will be toggled when user click Edit

        Form fields:
            confirm             a submit field triggered when user click Confirm change
            cancel              a submit field triggered when user click Cancel
            title (str)         a string field indicates Task title
            note (str)          a string field indicates Task 's note
    '''
    confirm = SubmitField('Confirm change')
    cancel = SubmitField('Cancel')
    title = StringField('Task title')
    note = StringField('Note')

class SignUpForm(FlaskForm):
    '''
    this form class will control the sign up form

        Form fields:
            username (str)      a string field indicate username
            password (str)      a string field indicate password
            email (str)         a string field indicate email     
            submit              a submit field triggered when user click Add me
            login              a submit field triggered when user click Take me back       
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email=StringField('Email')
    submit = SubmitField('Add me')
    login = SubmitField('Take me back')

class TimerSettingForm(FlaskForm):
    '''
    this form class will control the timer customize or setting form

        Form fields:
            task_time (int)     an integer field indicate task time amount
            break_time (int)    an integer field indicate break time amount
            auto_break (bool)   an boolean field to tell if user want to auto start the break time when the timer finished
            confirm             a submit field triggered when user click Confirm change
            cancel              a submit field triggered when user click Cancel
    '''
    task_time = IntegerField('Task time', default = 1800)
    break_time = IntegerField('Break time', default = 300)
    auto_break = BooleanField('Auto switch to break when finished?')
    confirm = SubmitField("Confirm setting")
    cancel = SubmitField("Cancel")
    
class AddFlashcardForm(FlaskForm):
    '''
    this form class will control the add flashcard form
        
        Form fields:
            title (str)         a string field indicate title of flashcard
            descrition (str)    a string field indicates description of flashcard
            add                 a submit field triggered when user hit Add
            cancel              a submit field triggered when user hit Cancel
    '''
    title = StringField('Title')
    description = TextAreaField('Description')
    add = SubmitField ('Add')
    cancel = SubmitField ('Cancel')

class ShareFlashcardForm(FlaskForm):
    '''
    this form class will control the share flashcard form
        
        Form fields:
            username (str)      a string field indicate destination username to the flashcard with
            submit              a submit field triggered when user hit Share
            cancel              a submit field triggered when user hit Cancel
    '''
    username = StringField('Enter username to share to', validators=[DataRequired()])
    submit = SubmitField ('Share')
    cancel = SubmitField('Cancel')

class AddNoteForm(FlaskForm):
    '''
    This class will allow the user to add a new note

        Form fields:
            title (str)         a string indicate of title
            password (str)      a string field indicate password
            body (str)          a string field indicate body of text
            submit              a submit field when user click Create
    '''
    title = StringField('Title', validators=[DataRequired()])
    password = PasswordField('Password')
    body = StringField('Body')
    submit = SubmitField('Create')


class filterNotesForm(FlaskForm):
    '''
    This class will allow the user to filter their list of notes

        Form fields:
            filter (str)        a string indicate of desired filter
            submit              a submit field when user click Search
    '''
    filter = StringField('Search by', validators = [DataRequired()])
    submit = SubmitField('Search')

class FlashcardToPDF(FlaskForm):
    '''
    this form class will control the flashcard to PDF form
        
        Form fields:
            submit              a submit field triggered when user hit Output flashcards to PDF file
    '''
    submit = SubmitField("Output flashcards to PDF file")


class ControlsBetweenFlashcardInViewForm(FlaskForm):
    '''
    this form class will control the next and previous button the flashcard route
        
        Form fields:
            prev              a submit field triggered when user hit Previous
            next              a submit field triggered when user hit Next
    '''
    prev = SubmitField('Previous')
    next = SubmitField('next')

class RenderMarkdownfileToFlashCardForm(FlaskForm):
    '''
    this form class will control the form that take a fil
        
        Form fields:
            filename(str)   a string field for filename of the markdown file to be converted to flashcards
            submit          a submit field trigger when user click convert markdown to flashcards
    '''
    filename = StringField('Please enter a markdown file name (for example: file.md): ', validators = [DataRequired()])
    submit = SubmitField('Convert markdown to flashcards')
