from myapp import myapp_obj

from myapp.forms import TimerSettingForm,AddFlashcardForm, EditTaskForm, ChangeTimerForm, LoginForm, TimerForm, AddTaskForm, ChangeToTaskAddForm, SignUpForm
from flask import request, render_template, flash, redirect
from datetime import date
import time
from myapp import db
from myapp.models import User, Task, Flashcard
from flask_login import current_user, login_user, logout_user, login_required

#global variables for the pomodoro timer
    #default options
maxTime = 2000
breakTime = 300
timerRemain = maxTime
timerLeft = maxTime
timerStopped = False
autoBreak = False
timerMessage = ""
timerType = 'task timer'
editTaskID = 999999999
    #toggle flags 
adding = False #flag to toggle the add task form when click "Add task"
editing = False
timerSetting = False

#helper functions
def refreshTimerPage():
    return redirect('/timer')

#Classes
class Timer():
        def __init__(self, m):
            self.max = m
            self.auto_break = False
        '''
        the functions will start the timer and countdown every 1 second
        '''
        def start(self):
            global timerStopped
            global timerRemain
            global timerType
            global autoBreak
            global timerMessage
            timerStopped = False
            while (not timerStopped and timerRemain > 0):
                timerRemain -= 1
                time.sleep(1) 
            self.stop()
            timerMessage = "Timer is done!"
            self.reset()
            if autoBreak and timerType ==  'task timer':
                timerType = 'break timer'
                self.change_time(current_user.break_timer)
                refreshTimerPage()

        def reset(self):
            global timerRemain
            timerRemain = self.max

        def stop(self):
            global timerStopped
            global timerMessage
            timerMessage = "Timer stopped"
            timerStopped = True

        def change_time(self, time):
            global timerRemain
            self.max = time
            timerRemain = time
            
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
                    u = User(   auto_break = False, 
                                username = form.username.data, 
                                email = form.email.data, 
                                task_timer = maxTime, 
                                break_timer = breakTime)
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
    #more code about notes are put here, this section is for Jason
    return render_template("notes.html") #expect the notes.htm  l will be render when user navigate to /notes

#Flashcards features
@myapp_obj.route("/flashcard", methods=["GET", "POST"])
def flashcard():
    form = AddFlashcardForm()
    u = User.query.filter_by(username = current_user.username).first() 
    if u != None:
        flashcards = u.flashcards.all()
    if form.validate_on_submit():
        if form.add.data:
            if form.title.data != "" and form.description.data != "":
                f = Flashcard (title = form.title.data, description = form.description.data)
                u.flashcards.append(f)
                db.session.add(f)
                db.session.commit()
                return redirect('/flashcard')
            else:
                flash("title and description should be not empty")
                return redirect('/flashcard')
    #more code about flashcard are put here, this section is for Kim 
    return render_template("flashcard.html", form=form, flashcards=flashcards) #expect the flashcard.html will be render when user navigate to /notes

#podomorotimer features
@myapp_obj.route("/timer", methods=["GET", "POST"])
def timer():
    #forms
    timer_form = TimerForm()
    add_task_form = AddTaskForm()
    timer_change_form = ChangeTimerForm()
    edit_task_form = EditTaskForm()
    timer_setting_form = TimerSettingForm()
    
    #to toggle the add task form when clicking "Add task"
    change_to_add = ChangeToTaskAddForm()
    current_task = None
    
    #global variables usage declartion
    global adding
    global timerType
    global editing
    global editTaskID
    global autoBreak
    global timerMessage
    global timerSetting
    u =  User.query.filter_by(username = current_user.username).first()
    tasks = u.tasks.filter_by(finished = False).all()
    if tasks:
        current_task = tasks[0]
    
    #more code about the timer are put here, this is Quang's section
    #initialize the timer with user's settings 
    if timerType == 'task timer':
        timer = Timer(u.task_timer) #1800s by default if not set
    else:
        timer = Timer(u.break_timer) #300s by default  
    autoBreak = u.auto_break #False by default

     #timer controller
    if timer_form.validate_on_submit():
        if timer_form.start_timer.data: #if user hit start timer
            timer.start()   
        elif timer_form.stop_timer.data: #if user hit stop timer
            timer.stop()
            refreshTimerPage()
        elif timer_form.reset_timer.data: #if user hit reset timer
            timerMessage = "" 
            timer.reset()
            refreshTimerPage()
    
    #change timer controller
    if timer_change_form.validate_on_submit():
        if timer_change_form.task_timer.data:
            timerType = 'task timer'
            timer.change_time(u.task_timer)
        elif timer_change_form.break_timer.data:
            timerType = 'break timer'
            timer.change_time(u.break_timer)
    
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
        elif add_task_form.cancel.data:
            add_task_form.title = ''
            add_task_form.note = ''
        return redirect('/timer')
    
    #edit task controller
    if edit_task_form.validate_on_submit():
        editing = False
        if edit_task_form.confirm.data:
            u =  User.query.filter_by(username = current_user.username).first()
            if u != None:
                task = u.tasks.filter_by(id = editTaskID).first()
                if task:
                    if edit_task_form.title.data != '':
                        task.title = edit_task_form.title.data
                        task.note = edit_task_form.note.data
                        db.session.commit()
        editTaskID = 99999999
        return redirect('/timer')
    
    #timer setting controller
    if timer_setting_form.validate_on_submit():
        timerSetting = False
        if timer_setting_form.confirm.data:
            u =  User.query.filter_by(username = current_user.username).first()
            if u != None:
                u.task_timer = timer_setting_form.task_time.data
                u.break_timer = timer_setting_form.break_time.data
                u.auto_break = timer_setting_form.auto_break.data
                print("here")
                db.session.commit()
        return redirect('/timer')
        
    return render_template("timer.html", 
                            timer = timer, 
                            timer_form = timer_form,
                            timerRemain = timerRemain,
                            add_task_form = add_task_form,
                            change_to_add = change_to_add,
                            edit_task_form = edit_task_form,
                            adding = adding,
                            tasks = tasks,
                            current_task = current_task,
                            timer_type = timerType.capitalize(),
                            timer_change_form = timer_change_form,
                            editing = editing,
                            editid = editTaskID,
                            timer_message = timerMessage,
                            timer_setting = timerSetting,
                            timer_setting_form = timer_setting_form
                            )

@myapp_obj.route("/edit_task/<string:taskid>")
def edit_task(taskid):
    global editing
    global editTaskID
    editing = True
    editTaskID = int(taskid)
    return redirect('/timer')

@myapp_obj.route("/delete_task/<string:taskid>")
def delete_task(taskid):
    Task.query.filter_by(id= taskid).delete()
    db.session.commit()
    u =  User.query.filter_by(username = current_user.username).first()
    return redirect('/timer')

@myapp_obj.route("/finish_task/<string:taskid>")
def finish_task(taskid):
    t = Task.query.filter_by(id = taskid).first()
    t.finished = True
    t.date_ended = date.today()
    db.session.commit()
    return redirect('/timer')

@myapp_obj.route("/timer_setting")
def timer_setting():
    '''
    function trigger when user click "Customize timer", set the global
    variable timerSetting to true to toggle on the timer setting form

    Return
        redirecting route back to the /timer route 
    '''
    global timerSetting 
    timerSetting = True
    return redirect('/timer')

@myapp_obj.route("/")
def home():
    '''
    Home page of the app after the user logged in

    Returns:
            html to home page if user logged in
        Or
            html to login page otherwise
    '''
    if current_user.is_authenticated:
        return render_template('home.html', username = current_user.username)
    else: 
        return redirect('/login')
