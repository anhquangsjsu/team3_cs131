from myapp import myapp_obj
from myapp.forms import CancelAddForm, LoginForm, StartTimerForm, StopTimerForm, ResetTimerForm, AddTaskForm, ChangeToTaskAddForm
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
adding = False
def refresh():
    return redirect("/timer")

class Timer():
        def __init__(self, m = maxTimer):
            self.max = m
        def start(self):
            global timerStopped
            global timerRemain
            if timerRemain == 0 :
                timerRemain = self.max
            timerStopped = False
            while (not timerStopped and timerRemain > 0):
                refresh()
                timerRemain -= 1
                print(timerRemain)
                time.sleep(1) 
                
        def reset(self):
            global timerRemain
            timerRemain = self.max
        def stop(self):
            global timerStopped
            timerStopped = True
            

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
    return render_template("notes.html") #expect the notes.htm  l will be render when user navigate to /notes

@myapp_obj.route("/flashcard")
def flashcard():
    #more code about flashcard are put here, this section is for Jason
    return render_template("flashcard.html") #expect the flashcard.html will be render when user navigate to /notes

@myapp_obj.route("/timer", methods=["GET", "POST"])
def timer():
    #timer forms
    stop_timer = StopTimerForm()
    start_timer = StartTimerForm()
    reset_timer = ResetTimerForm()
    #add task forms
    add_task_form = AddTaskForm()
    change_to_add = ChangeToTaskAddForm()
    cancel_add = CancelAddForm()
    timer = Timer(maxTimer)
    global timerStopped 
    global adding
    u =  User.query.filter_by(username = current_user.username).first()
    tasks = u.tasks.filter_by(finished = False)
    current_task = tasks.first()
    #more code about the timer are put here, this is Quang's section
    #timer control functions
    if start_timer.validate_on_submit() and start_timer.start_timer.data:
        timer.start()   
    elif stop_timer.validate_on_submit() and stop_timer.stop_timer.data:
        timer.stop()
        refresh()
    elif reset_timer.validate_on_submit() and reset_timer.reset_timer.data:
        timer.reset()
        refresh()
    #add task controller
    if change_to_add.validate_on_submit() and change_to_add.submit.data:
        adding = True
        refresh()
    if cancel_add.validate_on_submit() and cancel_add.cancel.data:
        adding= False
        refresh()
    if add_task_form.validate_on_submit() and add_task_form.add_task.data:
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
    return render_template("timer.html", 
                            timer = timer, 
                            stop_timer = stop_timer, 
                            start_timer = start_timer,
                            reset_timer = reset_timer,
                            timerRemain = timerRemain,
                            add_task_form = add_task_form,
                            change_to_add = change_to_add,
                            cancel_add = cancel_add,
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
    for t in tasks:
        print(t.id)
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
        print(current_user)
        return render_template('home.html', username = current_user.username)
    else: 
        return redirect('/login')