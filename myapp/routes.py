from myapp import myapp_obj
from myapp.forms import LoginForm
from flask import render_template, flash, redirect
from myapp import db
from myapp.models import User
from flask_login import current_user, login_user, logout_user, login_required



@myapp_obj.route("/loggedin")
@login_required
def log():
    return "Hi you are looged in"

@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@myapp_obj.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Login invalid username or password")
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        flash(f'login requested for user {form.username.data}')
        return redirect('/')
    return render_template("login.html", form=form)

@myapp_obj.route("/notes")
def notes():
    #more code about notes are put here, this section is for Kim
    return render_template("notes.html") #expect the notes.html will be render when user navigate to /notes

@myapp_obj.route("/flashcard")
def flashcard():
    #more code about flashcard are put here, this section is for Jason
    return render_template("flashcard.html") #expect the flashcard.html will be render when user navigate to /notes

@myapp_obj.route("/timer")
def timer():
    #more code about the timer are put here, this is Quang's section
    return render_template("timer.html")

@myapp_obj.route("/")
def home():
    return render_template('home.html')