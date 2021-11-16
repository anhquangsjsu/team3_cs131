from myapp import myapp_obj
from myapp.forms import LoginForm, TimerForm, AddTaskForm, ChangeToTaskAddForm, SignUpForm
from flask import request, render_template, flash, redirect
from datetime import date
import time
from myapp import db
from myapp.models import User, Task
from flask_login import current_user, login_user, logout_user, login_required

#global variables for the pomodoro timer
maxTimer = 1800
timerStopped = False
timerRemain = maxTimer
adding = False #flag to toggle the add task form when click "Add task"

#helper functions
def refreshTimerPage():
    return redirect('/timer')

class Timer():
        def __init__(self, m = maxTimer):
            self.max = m
        '''
        the functions will start the timer and countdown every 1 second
        '''
        def start(self):
            global timerStopped
            global timerRemain
            if timerRemain == 0 :
                timerRemain = self.max
            timerStopped = False
            while (not timerStopped and timerRemain > 0):
                timerRemain -= 1
                time.sleep(1) 
                
        def reset(self):
            global timerRemain
            timerRemain = self.max

        def stop(self):
            global timerStopped
            timerStopped = True
            
###Login logout features
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
        #if user click submit
        if form.submit.data:
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Login invalid username or password")
                return redirect('/login')
            login_user(user, remember=form.remember_me.data)
            flash(f'login requested for user {form.username.data}')
            return redirect('/')
        #or user choose to sign up
        elif form.signup.data:
            return redirect('/signup')
    return render_template("login.html", form=form)

@myapp_obj.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.submit.data == True:
            #check if the user is already there
            user =  User.query.filter_by(username=form.username.data).first()
            if user is None:
                user = User.query.filter_by(email=form.email.data).first()
                if user is None: #check if email is used
                    u = User(username = form.username.data, email = form.email.data)
                    u.set_password(form.password.data)
                    db.session.add(u)
                    db.session.commit()
                    return redirect(f'/signedup/{form.username.data}')
                else:
                    flash('The email is already used')
                    return redirect('/signup')
            else:
                flash('User already exists, please try a differen user')
                return redirect('/signup')
        elif form.login.data == True:
            return redirect('/login')
    return render_template('signup.html', form = form)

@myapp_obj.route('/signedup/<string:user>', methods=['GET', 'POST'])
def signedup(user):
    return render_template('signedup.html',user = user)
#Notes features
@myapp_obj.route("/notes")
def notes():
    #more code about notes are put here, this section is for Kim
    return render_template("notes.html") #expect the notes.htm  l will be render when user navigate to /notes

#Flashcards features
@myapp_obj.route("/flashcard")
def flashcard():
    #more code about flashcard are put here, this section is for Jason
    return render_template("flashcard.html") #expect the flashcard.html will be render when user navigate to /notes

#podomorotimer features
@myapp_obj.route("/timer", methods=["GET", "POST"])
def timer():
    timer_form = TimerForm()
    add_task_form = AddTaskForm()
    #to toggle the add task form when clicking "Add task"
    change_to_add = ChangeToTaskAddForm()
    timer = Timer(maxTimer)
    global timerStopped 
    global adding
    u =  User.query.filter_by(username = current_user.username).first()
    tasks = u.tasks.filter_by(finished = False)
    current_task = tasks.first()
    #more code about the timer are put here, this is Quang's section
    #timer control form action and functions
    if timer_form.validate_on_submit():
        if timer_form.start_timer.data:
            timer.start()   
        elif timer_form.stop_timer.data:
            timer.stop()
            refreshTimerPage()
        elif timer_form.reset_timer.data:
            timer.reset()
            refreshTimerPage()
    #add task controller
    if change_to_add.validate_on_submit() and change_to_add.submit.data:
        adding = True
        refreshTimerPage()

    if add_task_form.validate_on_submit():
        if add_task_form.add_task.data:
            adding= False
            t = Task(title = add_task_form.title.data,
                    note = add_task_form.note.data,
                    finished = False,
                    date_started = date.today())
            u =  User.query.filter_by(username = current_user.username).first()
            if u != None:
                u.tasks.append(t)
                db.session.add(t)
                db.session.commit()
                return redirect('/timer')
        elif add_task_form.cancel.data:
            adding = False
            add_task_form.title = ''
            add_task_form.note = ''
            return redirect('/timer')

    return render_template("timer.html", 
                            timer = timer, 
                            timer_form = timer_form,
                            timerRemain = timerRemain,
                            add_task_form = add_task_form,
                            change_to_add = change_to_add,
                            adding = adding,
                            tasks = tasks,
                            current_task = current_task,
                             )

@myapp_obj.route("/edit_task/<string:taskid>")
def edit_task(taskid):
    return redirect('/timer')

@myapp_obj.route("/delete_task/<string:taskid>")
def delete_task(taskid):
    Task.query.filter_by(id= taskid).delete()
    db.session.commit()
    u =  User.query.filter_by(username = current_user.username).first()
    tasks = u.tasks.all()
    return redirect('/timer')

@myapp_obj.route("/finish_task/<string:taskid>")
def finish_task(taskid):
    t = Task.query.filter_by(id = taskid).first()
    t.finished = True
    db.session.commit()
    return redirect('/timer')

@myapp_obj.route("/")
def home():
    if current_user.is_authenticated:
        return render_template('home.html', username = current_user.username)
    else: 
        return redirect('/login')