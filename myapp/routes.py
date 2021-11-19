from myapp import myapp_obj

from myapp.forms import AddNoteForm, filterNotesForm, TimerSettingForm,AddFlashcardForm, EditTaskForm, ChangeTimerForm, LoginForm, TimerForm, AddTaskForm, ChangeToTaskAddForm, SignUpForm
from flask import request, render_template, flash, redirect
from datetime import date
import time
from myapp import db
from myapp.models import User, Task, Flashcard, Notes
from flask_login import current_user, login_user, logout_user, login_required

#global variables for the pomodoro timer
    #default options
maxTime = 2000
breakTime = 300
timerRemain = -99
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
    #Notes global variables
filtered = False
filterList = []
#helper functions
def refreshTimerPage():
    return redirect('/timer')

#Classes
class Timer():
    '''
    Global variables are used in this class to form a basic countdown timer a few controls:
    1. Start timer
    2. Stop timer
    3. Reset timer
    4. Change to different time
    '''
    def __init__(self, m):
        '''
        the constructor, take in self and a time amount in seconds, will initialize the instance's max
            
            Parameters
                self (obj) refererence to the obj instance
                m (int)    max amount of time set for the timer 
        '''
        self.max = m
    def start(self):
        '''
        the functions will start the timer and countdown every 1 second, when timer reached 0, 
        notify the user that timer is stopped, and switch to break timer if the user has the auto break setting on

            Parameters:
                self (obj)                  a reference to this object instance
                global autoBreak (bool)     a boolean that keep track of user's auto entering break timer setting when finished the timer     
                global timerStopped(bool)   a boolean to indicate when the timer is stopped, used to stop the while loop
                global timerRemain (int)    an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly
                global timerType (str)      a string indicates which type of timer is chosen from the change timer form
                global timerMessage (str)   a string stored message regarding the timer            
        
        '''
        global timerStopped
        global timerRemain
        global timerType
        global autoBreak
        global timerMessage
        timerStopped = False
        while (not timerStopped and timerRemain > 0):
            timerRemain -= 1 
            time.sleep(1)    
        if timerRemain <= 0:
            self.stop()
            timerMessage = "Timer is done!"
            self.reset()
            if autoBreak and timerType ==  'task timer':
                timerType = 'break timer'
                self.change_time(current_user.break_timer)
                refreshTimerPage()

    def reset(self):
        '''
        reset the timer countdown to max time
            
            Parameters:
                self (obj)                  a reference to this object instance
                global timerRemain (int)    an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly
        '''
        global timerRemain
        timerRemain = self.max

    def stop(self):
        '''
        stops the timer by signaling with timerStopped flag and notifies the user with a message

            Parameters:
                self (obj)                  a reference to this object instance
                global timerStopped(bool)   a boolean to indicate when the timer is stopped, used to stop the while loop
                global timerType (str)      a string indicates which type of timer is chosen from the change timer form
                global timerMessage (str)   a string stored message regarding the timer    
        '''
        global timerStopped
        global timerMessage
        timerMessage = "Timer stopped"
        timerStopped = True

    def change_time(self, time):
        '''
        change the max time of timer and the remaining time

            Parameters:
                self (obj)                      a reference to this object instance
                time (int)                      an integer presents amount of time in seconds
                global timerRemain (int)        an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly
        '''
        global timerRemain
        self.max = time
        timerRemain = time
            
###Login logout features
@myapp_obj.route("/loggedin")
@login_required
def log():
    '''
    to notify the user that they logged in

        Returns
            a string message to inform user their loged in status
    '''
    return "Hi you are loged in"

@myapp_obj.route("/logout")
def logout():
    '''
    will log out the current user and redirect back to the login page
    '''
    logout_user()
    return redirect('/login')

@myapp_obj.route("/login", methods=['GET','POST'])
def login():
    '''
    returns the sign in page when navigating to /login and controls the log in form, 
    The log in page will be initially displayed when user starts the app 

        Returns
                redirecting back to the page
            or
                a html corresponding to the login page that holds form for user to sign in
    '''
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
    '''
    returns the sign up user page when navigating to /signup and controls the sign up form 

        Returns
                redirecting back to the page
            or
                a html corresponding to the sign up page that holds form for user to register new user
    '''
    form = SignUpForm()
    if form.validate_on_submit():
        #when user click add me
        if form.submit.data:
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
        #when user click take me back
        elif form.login.data:
            return redirect('/login')
    return render_template('signup.html', form = form)

@myapp_obj.route('/signedup/<string:user>', methods=['GET', 'POST'])
def signedup(user):
    '''
    returns the signedup.html to notify user successful sign up and give them option to sign in later

        Returns
            a html to notify that user succesfully signed up
    '''
    return render_template('signedup.html',user = user)

#Notes features
@myapp_obj.route("/notes", methods=["GET", "POST"])
def notes():
    #more code about notes are put here, this section is for Jason
    global filterList
    global filtered
    addnoteform = AddNoteForm()
    filterform = filterNotesForm()
    u = User.query.filter_by(username = current_user.username).first()
    if u != None:
        if filtered: 
            notes = filteredList
        else:
            notes = u.notes.all()
        

    if filterform.validate_on_submit():
        if filterform.key.data != "":
            filtered = True
            filterList.clear()
            for n in notes:
                if filterform.filter.data in n.title:
                    filterList.append(n)

            return redirect("/notes")
    if addnoteform.validate_on_submit():
        if addnoteform.submit.data:
            if addnoteform.title.data != "":
                n = Notes(title = addnoteform.title.data, body = addnoteform.body.data, password = addnoteform.password.data)
                db.session.add(n)
                db.session.commit()
                flash(f'The note {form.title.data} has been added')
                return redirect("/notes")
            else:
                flash("Your note needs a title in order to be created")
                return redirect("/notes")
    return render_template("notes.html", form = addnoteform, form2 = filterform, all_notes = notes) #expect the notes.htm  l will be render when user navigate to /notes

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
    '''
    Render the timer html portion of the app when user navigate to /timer route or click timer link in the navigation bar at the top
    This functions will:
        1. Control forms: the timer form, add task form, change timer form, edit task form, and timer 
        2. Set up the timer accordingly to task timer or break timer based on the global variables
    
        Parameters
            global adding (bool)        a flag to tell if adding form is toggled on
            global autoBreak (bool)     a boolean that keep track of user's auto entering break timer setting when finished the timer
            global timerSetting (bool)  a flag to tell if customize timer setting form is on         
            global editing (bool)       a flag to tell if the editing form of a particular task is on when user click edit button under neath the task
            global editTaskID (int)     an integer to keep track the current task to be edit, only one task can be edit at a time
            global timerRemain (int)    an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly
            global timerType (str)      a string indicates which type of timer is chosen from the change timer form
            global timerMessage (str)   a string stored message regarding the timer

        Returns
                redirecting to itself
            or
                a template timer.html of the page corresponding to the route /timer
    '''
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
    global timerRemain

    u =  User.query.filter_by(username = current_user.username).first()
    tasks = u.tasks.filter_by(finished = False).all()
    if tasks:
        current_task = tasks[0]
    
    #more code about the timer are put here, this is Quang's section
    #initialize the timer with user's settings 
    if timerType == 'task timer':
        if timerRemain == -99: #to detect when 
            timerRemain = u.task_timer
        timer = Timer(u.task_timer) #1800s by default if not set
    else:
        if timerRemain == -99:
            timerRemain = u.break_timer
        timer = Timer(u.break_timer) #300s by default  
    autoBreak = u.auto_break #False by default
     #timer controller
    if timer_form.validate_on_submit():
        if timer_form.start_timer.data: #if user hit start timer
            timer.start()   
        elif timer_form.stop_timer.data and not timerStopped: #if user hit stop timer
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
    
    #add task controllers
        #add task toggle on or off
    if change_to_add.validate_on_submit() and change_to_add.submit.data:
        adding = True
        refreshTimerPage()
        #add task form controller
    if add_task_form.validate_on_submit() and adding:
        #add is clicked
        if add_task_form.add_task.data:
            t = Task(title = add_task_form.title.data,
                    note = add_task_form.note.data,
                    finished = False,
                    date_started = date.today())
            u =  User.query.filter_by(username = current_user.username).first()
            if u != None:
                if add_task_form.title.data != '':
                    u.tasks.append(t)
                    db.session.add(t)
                    db.session.commit()
                    adding= False
        # cancel clicked
        elif add_task_form.cancel.data:
            adding = False
            add_task_form.title = ''
            add_task_form.note = ''
        return redirect('/timer')    
        
    
    #edit task controller
    if edit_task_form.validate_on_submit() and editing:
        #if user click coonfirm
        if edit_task_form.confirm.data:
            u =  User.query.filter_by(username = current_user.username).first()
            if u != None:
                task = u.tasks.filter_by(id = editTaskID).first()
                if task:
                    if edit_task_form.title.data != '':
                        task.title = edit_task_form.title.data
                        task.note = edit_task_form.note.data
                        db.session.commit()
                        editing = False
                        editTaskID = 99999999
                        return redirect('/timer')
        #cancel is clicked
        elif edit_task_form.cancel.data:
            editing = False
            editTaskID = 99999999
            return redirect('/timer')
    
    #timer setting controller
    if timer_setting_form.validate_on_submit() and timerSetting:
        timerSetting = False
        #confirm field clicked
        if timer_setting_form.confirm.data:
            u =  User.query.filter_by(username = current_user.username).first()
            if u != None:
                u.task_timer = timer_setting_form.task_time.data
                u.break_timer = timer_setting_form.break_time.data
                u.auto_break = timer_setting_form.auto_break.data
                db.session.commit()
                if timerType == 'task timer':
                    timer.change_time(u.task_timer) 
                else:
                    timer.change_time(u.break_timer)
                autoBreak = u.auto_break 
                return redirect('/timer')
        #cancel field clicked
        elif timer_setting_form.cancel.data:
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
    '''
    function trigger when user click edit a task, will toggle edit form underneath the task based on its id when user click Edit

        Parameters:
            taskid (int):      a task id
            editing (boolean): a global variable to indicate if edit form is toggled on
            editTaskID (int):  a global varialbe to keep track the current task to be edited so proper form can be displayed according to task id
           
        Returns
            redirecting route back to the /timer 
    '''
    global editing
    global editTaskID
    editing = True
    editTaskID = int(taskid)
    return redirect('/timer')

@myapp_obj.route("/delete_task/<string:taskid>")
def delete_task(taskid):
    '''
    function trigger when user click delete task, will delete a task using its id 

        Parameters:
            taskid (int): a task id

        Returns
            redirecting route back to the /timer 
    '''
    Task.query.filter_by(id= taskid).delete()
    db.session.commit()
    u =  User.query.filter_by(username = current_user.username).first()
    return redirect('/timer')

@myapp_obj.route("/finish_task/<string:taskid>")
def finish_task(taskid):
    '''
    function trigger when user click finish task, will mark a particular task finished using its id in the user tasks
    also mark the finished date
        
        Parameters:
            taskid (int): a task id

        Returns
            redirecting route back to the /timer
    '''
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

        Parameters
            timerSetting (boolean) a global variable keep track if the setting form for timer is on

        Returns
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
