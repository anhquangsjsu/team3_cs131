from myapp import myapp_obj
import pdfkit
from myapp.forms import RenderMarkdownfileToFlashCardForm,ControlsBetweenFlashcardInViewForm, FlashcardToPDF,ShareFlashcardForm, AddNoteForm, filterNotesForm, TimerSettingForm,AddFlashcardForm, EditTaskForm, ChangeTimerForm, LoginForm, TimerForm, AddTaskForm, ChangeToTaskAddForm, SignUpForm
from flask import send_from_directory, request, render_template, flash, redirect
from datetime import date
import time
from myapp import db
from myapp.models import User, Task, Flashcard, Notes
from flask_login import current_user, login_user, logout_user, login_required
import os
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
    #flashcard global variables 
sharing = False 
sharingID = 999999999
revealedCard = False
flashcardsList = []
currentCard = None
currentCardInView = None
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
            
            Parameters:
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

        Returns:
            a string message to inform user their loged in status
    '''
    return "Hi you are loged in"

@myapp_obj.route("/logout")
def logout():
    '''
    will log out the current user and redirect back to the login page
         
         Returns:
                redirecting back to the page
    '''
    logout_user()
    return redirect('/login')

@myapp_obj.route("/login", methods=['GET','POST'])
def login():
    '''
    returns the sign in page when navigating to /login and controls the log in form, 
    The log in page will be initially displayed when user starts the app 

        Returns:
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

        Returns:
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

        Returns:
            a html to notify that user succesfully signed up
    '''
    return render_template('signedup.html',user = user)

#Notes features
@myapp_obj.route("/notes", methods=["GET", "POST"])
def notes():
    '''
    This function render notes html portion of the app when user navigate to /notes route or click notes l>    This function will:
        1. add new notes for the user
        2. allow user to view all of their notes
        3. allow user to search for notes by keywords

        Parameters:
            global filtered(bool)                   a flag telling if the user has prompted for a filtered list of the notes
            global filterList(List<Notes>)  a global notes list used to store a list of filtered notes
        Returns:
                redirecting to itself
            or
                a template notes.html of the page corresponding to the route /notes
    '''
    #more code about notes are put here, this section is for Jason
    global filterList
    global filtered
    nots = []
    addnoteform = AddNoteForm()
    filterform = filterNotesForm()
    u = User.query.filter_by(username = current_user.username).first()
    if u != None: 
        if filtered: 
            nots = filterList
            filtered = False
        else:
            nots = u.notes.all()
        

    if filterform.validate_on_submit():
        if filterform.filter.data != "":
            filtered = True
            filterList.clear()
            for n in nots:
                if filterform.filter.data in n.title:
                    filterList.append(n)

            return redirect("/notes")
    if addnoteform.validate_on_submit():
        if addnoteform.submit.data:
            if addnoteform.title.data != "":
                n = Notes(user_id = u.id, title = addnoteform.title.data, body = addnoteform.body.data, password = addnoteform.password.data)
                db.session.add(n)
                db.session.commit()
                flash(f'The note {addnoteform.title.data} has been added')
                return redirect("/notes")
            else:
                flash("Your note needs a title in order to be created")
                return redirect("/notes")
    return render_template("notes.html", form = addnoteform, form2 = filterform, all_notes = nots) #expect the notes.htm  l will be render when user navigate to /notes

@myapp_obj.route("/open_note/<string:noteid>")
def getNote(noteid):
    """
    This function will render open_note.html and pass the desired note into it. The end result is that it will display a note
    
        Parameters:
            noteid (int)        integer indicate id of a note

        Returns:
            a template open_note, displaying the desired note
    """
    n = Notes.query.filter_by(id = noteid).first()
    return render_template("open_note.html", aNote = n) 

#Flashcards features
@myapp_obj.route("/flashcard", methods=["GET", "POST"])
def flashcard():
    '''
    This function render flashcards html portion of the app when user navigate to /flashcard route or click flashcard link in the navigation bar at the top
    This function will:
        1. add new flashcard for the user
        2. allow user to share a flash card with another user
        3. allow user to convert markdown file to flashcards 
        4. allow user to convert flashcards to PDF
    
        Parameters:
            global sharing(bool)                    a flag telling if the user opened the sharing flashcard form
            global flashcardsList(List<Flashcard>)  a global flashcards list used for the entire app
            global currentCard(Flashcard)           a global Flashcard storing the current flashcard so that app can move between the cards in the list with next and previous buttons
            global currentCardInView(Flashcard)     a global Flashcard storing the current flashcard used in the flashcards_from_md route
        Returns:
                redirecting to itself
            or
                a template flashcard.html of the page corresponding to the route /flashcard
            or
                redirecting to route /flashcards_from_md 
    '''
    global sharing
    global flashcardsList 
    global currentCard
    global currentCardInView
    #forms 
    pdf_flash_form = FlashcardToPDF()
    md_flash_form = RenderMarkdownfileToFlashCardForm()
    form = AddFlashcardForm()
    share_flashcard_form = ShareFlashcardForm()
    u = User.query.filter_by(username = current_user.username).first() 
    if u != None:
        flashcards = u.flashcards.all()
        flashcardsList = flashcards
        if currentCard == None:
            currentCard = flashcardsList[-1]
    #add flashcard features
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

    #share flashcard features
    if share_flashcard_form.validate_on_submit() and sharing:
        #share is clicked
        if share_flashcard_form.submit.data:
            u = User.query.filter_by(username = share_flashcard_form.username.data).first()
            f = Flashcard.query.filter_by(id = sharingID).first()
            if u != None:
                if share_flashcard_form.username.data !='':
                    newf = Flashcard(title = f.title, description = f.description)
                    u.flashcards.append(newf)
                    db.session.add(newf)
                    db.session.commit()
                    sharing = False
        #cancel is clicked
        elif share_flashcard_form.cancel.data:
            sharing = False
            share_flashcard_form.username = ''
        return redirect ('/flashcard')
    #Input a markdown file and convert to flashcard
    if md_flash_form.validate_on_submit() and md_flash_form.submit.data:
        filename = md_flash_form.filename.data
        currentCardInView = None
        return redirect('/flashcards_from_md/' + filename)
    #Out put flashcard to PDF
    if pdf_flash_form.validate_on_submit() and pdf_flash_form.submit.data:
        workingdir = os.path.abspath(os.getcwd())
        filepath = workingdir
        html = '<h1>' + u.username + '\'s flashcards </h1>'
        for f in flashcards:
            html += '<h3>' + f.title + '</h3>'
            html += '<p>' + f.description + '</p>'
        pdfkit.from_string(html, 'myflashcards.pdf')
        return send_from_directory(filepath, 'myflashcards.pdf')
    #more code about flashcard are put here, this section is for Kim 
    return render_template("flashcard.html", md_flash_form = md_flash_form, pdf_flash_form = pdf_flash_form,revealedCard = revealedCard ,currentCard = currentCard, sharingID = sharingID, sharing = sharing, form=form, flashcards=flashcards, share_flashcard_form=share_flashcard_form) #expect the flashcard.html will be render when user navigate to /notes

#podomorotimer features
@myapp_obj.route("/timer", methods=["GET", "POST"])
def timer():
    '''
    Render the timer html portion of the app when user navigate to /timer route or click timer link in the navigation bar at the top
    This function will:
        1. Control forms: the timer form, add task form, change timer form, edit task form, and timer 
        2. Set up the timer accordingly to task timer or break timer based on the global variables
    
        Parameters:
            global adding (bool)        a flag to tell if adding form is toggled on
            global autoBreak (bool)     a boolean that keep track of user's auto entering break timer setting when finished the timer
            global timerSetting (bool)  a flag to tell if customize timer setting form is on         
            global editing (bool)       a flag to tell if the editing form of a particular task is on when user click edit button under neath the task
            global editTaskID (int)     an integer to keep track the current task to be edit, only one task can be edit at a time
            global timerRemain (int)    an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly
            global timerType (str)      a string indicates which type of timer is chosen from the change timer form
            global timerMessage (str)   a string stored message regarding the timer

        Returns:
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
           
        Returns:
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

        Returns:
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

        Returns:
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

        Parameters:
            timerSetting (boolean) a global variable keep track if the setting form for timer is on

        Returns:
            redirecting route back to the /timer route 
    '''
    global timerSetting 
    timerSetting = True
    return redirect('/timer')

@myapp_obj.route("/")
def home():
    '''
    renders the home page of the app after the user logged in or sends the user to login page when they did not sign in

        Returns:
                html to home page if user logged in
            Or
                html to login page otherwise
    '''
    if current_user.is_authenticated:
        return render_template('home.html', username = current_user.username)
    else: 
        return redirect('/login')

@myapp_obj.route("/share_flashcard/<string:flashcardid>")
def share_flashcard(flashcardid):
    '''
    function trigger when user click sharing a flashcard, will toggle sharing form underneath the corresponding flashcard based on its id when user click Share this flashcard

        Parameters:
            flashcardid (int):      a flashcard id integer
            sharing (boolean):      a global variable to indicate if edit form is toggled on
            sharingID (int):        a global varialbe to keep track the current flashcard to be shared so proper form can be displayed according to task id
           
        Returns:
            redirecting route back to the /flashcard
    '''
    global sharing
    global sharingID
    sharing = True
    sharingID = int(flashcardid)
    return redirect('/flashcard')

@myapp_obj.route("/next_flashc")
def next_flashc():
    '''
    This function will move to the next flashcard in the list when user click "Next"
    
        Parameters:
            global flashcardsList(List<Flashcard>)  a global flashcards list used for the entire app
            global currentCard(Flashcard)           a global Flashcard storing the current flashcard so that app can move between the cards in the list with next and previous buttons
        
        Returns:
            redirecting to /flashcard route
    '''
    global currentCard
    global flashcardsList
    current_index = 0
    u = User.query.filter_by(username = current_user.username).first()
    u = User.query.filter_by(username = current_user.username).first()
    flashcards = u.flashcards.all()
    for i in range(1,len(flashcards)):
        if currentCard.title == flashcards[i].title and currentCard.description == flashcards[i].description:
            current_index = i

    current_index = current_index + 1
    if (current_index >= len(flashcardsList)):
        current_index = 0
    currentCard = flashcardsList[current_index]
    return redirect('/flashcard')

@myapp_obj.route("/prev_flashc")
def prev_flashc():
    '''
    This function will move to the previous flashcard in the list when user click "Previous"
    
        Parameters:
            global flashcardsList(List<Flashcard>)  a global flashcards list used for the entire app
            global currentCard(Flashcard)           a global Flashcard storing the current flashcard so that app can move between the cards in the list with next and previous buttons
        
        Returns:
            redirecting to /flashcard route
    '''
    global currentCard
    global flashcardsList
    current_index = 0
    u = User.query.filter_by(username = current_user.username).first()
    flashcards = u.flashcards.all()
    for i in range(1,len(flashcards)):
        if currentCard.title == flashcards[i].title and currentCard.description == flashcards[i].description:
            current_index = i

    current_index = current_index - 1
    if (current_index < 0):
        current_index = len(flashcards) - 1
    currentCard = flashcards[current_index]
    return redirect('/flashcard')

@myapp_obj.route("/hide_flash")
def hide_flash():
    '''
    This function will hide the description of the card when user click "Reveal description"
    
        Parameters:
            global revealedCard(bool)       a global boolean variable indicate if the card's description is revealed or not
        
        Returns:
            redirecting to /flashcard route
    '''
    global revealedCard
    revealedCard = False
    return redirect('/flashcard')

@myapp_obj.route("/reveal_flash")
def reveal_flash():
    '''
    This function will reveal the description of the card when user click "Reveal description"
    
        Parameters:
            global revealedCard(bool)       a global boolean variable indicate if the card's description is revealed or not
        
        Returns:
            redirecting to /flashcard route
    '''
    global revealedCard
    revealedCard = True
    return redirect('/flashcard')

@myapp_obj.route("/flashcards_from_md/<string:filename>", methods=['POST', 'GET'])
def flash_md(filename):
    '''
    This function will return the flashcards_from_md.html when get to route /flashcards_from_md after use hit "Convert markdown to flashcards" "

    It will read from the markdown files then convert them to flashcards, and control forms to move between the flashcards

        Parameters:
            global currentCardInView(Flashcard)     a global Flashcard storing the current flashcard used in the flashcards_from_md route
            filename(str)                           a string of filename passed via the link in flashcard route

        Returns:
            redirecting back to the current route
    '''
    global currentCardInView
    #for the file of md to be converted correctly, the file format should have a ## for title, follow by a paragraph in new line for the flashcard description, the input file should be put in the myapp/mdfiles
    form = ControlsBetweenFlashcardInViewForm()
    #file readers
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir
    flashcards = []
    flashcardtTitles = []
    flashcardDesscription = []
    #open the markdown file
    with open(filepath+'/myapp/mdfiles/' + filename, 'r') as f:
        #store each line in coresponding section i.e. title or description
        for x in f:
            if (x.find('##') == 0):
                a = x.replace('## ', '')
                b = a.strip()
                print(b)
                flashcardtTitles.append(b)
            else:
                a = x.strip()
                print(a)
                flashcardDesscription.append(a)
    #store the cards to a new list
    for i in range (0, len(flashcardtTitles)):
        flashcard = {'title': '', 'description': ''}
        flashcard['title'] = flashcardtTitles[i]
        flashcard['description'] = flashcardDesscription[i]
        flashcards.append(flashcard)
    if currentCardInView == None:
        currentCardInView = flashcards[0]
      #switch between cards form
    if form.validate_on_submit():
        i = 0
        for c in flashcards:
            if c['title'] == currentCardInView['title'] and c['description'] == currentCardInView['description']:
                break
            i += 1
        if form.prev.data:
            i -= 1
            if i < 0:
                i = len(flashcards) - 1
        elif form.next.data:
            i += 1
            if i >= len(flashcards):
                i = 0
        currentCardInView = flashcards[i]
    return render_template("flashcards_from_md.html",card = currentCardInView, form = form)


