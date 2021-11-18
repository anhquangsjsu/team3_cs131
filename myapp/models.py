from myapp import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from myapp import login


class User(UserMixin, db.Model):
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
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    note = db.Column(db.String(256))
    finished = db.Column(db.Boolean)
    remained_time = db.Column(db.Integer) #seconds
    date_started = db.Column(db.Date)
    date_ended = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Flashcard(db.Model):
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
"""
"""
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.id}: {self.body}>'
"""
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
