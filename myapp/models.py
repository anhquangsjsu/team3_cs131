from myapp import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from myapp import login


class User(UserMixin, db.Model):
    '''
    User model, the center of the app, this is where information of the user as well as the app features data are stored

        Relationships with:
            Task        One-to-Many
            Note        One-to-Many
            Flashcard   One-to-Many

        Data Fields:
            id (int)                integer indicate id of user
            username (str)          string indicate username
            password (str)          string indicate password
            email   (str)           string indicate email
            task_timer (int)        integer indicate user task timer setting
            break_timer (int)       integer indicate user break timer setting
            tasks   (List<obj>)     list of object containing tasks added by the user, used in the timer feature, connected the User with the Task model class
            flashcards (List<obj>)  list of object containing flashcards added by the user, used in the flash card feature, connected the User with the Flashcard model class 
            notes (List<obj>)       list of object containing notes added by the user, used in the notes feature, connected the User with the Note model class
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    password  = db.Column(db.String(128))
    task_timer = db.Column(db.Integer)
    break_timer = db.Column(db.Integer)
    auto_break = db.Column(db.Boolean)
    tasks = db.relationship('Task', 
                            backref = 'user', 
                            lazy = 'dynamic', 
                            cascade = 'all, delete, delete-orphan' )
    flashcards = db.relationship('Flashcard', 
				  backref = 'user', 
				  lazy = 'dynamic',
				  cascade = 'all, delete, delete-orphan' )
    notes = db.relationship('Notes', backref='user', lazy='dynamic', cascade = 'all, delete, delete-orphan')

    def set_password(self, password):
        '''
        This function will help set password for user using hash function
            
            Parameters:
                self (obj)          reference to this class instance
                password (string)   a string containing password
        '''
        self.password = generate_password_hash(password)

    def check_password(self, password):
        '''
        this function will check the password using hash function, return a boolean

            Parameters:
                self (obj)          reference to this class instance
                password (string)   a string containing password

            Returns:
                a boolean indicate if the password matches
        '''
        return check_password_hash(self.password, password)

class Task(db.Model):
    '''
    A model present the task added by the user in the timer feature

        Relationships with:
            User        Many-to-One
        
        Data Fields:
            id (int)            unique id integer of the task
            title (str)         title string of the the task
            note (str)          note string of the task
            finished (bool)     finished flag boolean of the the task
            date_started (Date) a date when the task started
            date_ended (Date)   a date when the task is finished
            user_id (int)       id of the user who owned the task
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    note = db.Column(db.String(256))
    finished = db.Column(db.Boolean)
    date_started = db.Column(db.Date)
    date_ended = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Flashcard(db.Model):
    '''
    A model presents the flashcard added by the user in the flashcard feature

        Relationships with:
            User        Many-to-One
        
        Data Fields:
            id (int)            unique id integer of the flashcard
            title (str)         title string of the the flashcard
            description (str)   description string of the flashcard
            date_started (Date) a date when the flashcard was added
            user_id (int)       id of the user who owned the task
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    date_started = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

"""class FlaskCard(db.Model):
    id =
    title =
    description =
    date_added = 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    please work
"""

class Notes(db.Model):
    '''
    Notes model, where users can create and store within their account
        Relationships with:
            User        Many-to-One

        Data Fields:
            id (int)                integer indicate id of note
            body (str)              string indicate body of text
            timstamp (datetime)     datetime indicate creation time
            user_id (int)           integer indicate of user ownership
            password (str)          string indicate password
            title (str)             string indicate of note title
    '''
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    password = db.Column(db.String(128))
    title = db.Column(db.String(32))

    def set_password(self, password):
        '''
        This function will help set password for the note using hash function

            Parameters:
                self (obj)          reference to this class instance
                password (string)   a string containing password
        '''
        self.password = generate_password_hash(password)

    def check_password(self, password):
        '''
        this function will check the password using hash function, return a boolean

            Parameters:
                self (obj)          reference to this class instance
                password (string)   a string containing password

            Returns:
                a boolean indicate if the password matches
        '''
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
