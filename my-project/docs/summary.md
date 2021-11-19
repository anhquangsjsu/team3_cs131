# Summary of classes and functions 

## Lists of classes and functions

#### **routes.py**
##### Classes:
* [Timer](#Timer)
    * [\_\_init\_\_()](#__init__)
    * [start()](#start)
    * [reset()](#reset)
    * [stop()](#stop)
    * [change_time()](#change_time)
##### Functions:
* [log()](#log)
* [logout()](#logout)
* [login()](#login)
* [signup()](#signup)
* [signedup()](#signedup)
* [notes()](#notes)
* [flashcard()](#flashcard)
* [timer()](#timer)
* [edit_task()](#edit_task)
* [delete_task()](#delete_task)
* [finish_task()](#finish_task)
* [timer_setting()](#timer_setting)
* [home()](#home())
#### **models.py**
##### Model Classes
* [User](#User)
    * [set_password()](#set_password)
    * [check_password()](#check_password)
* [Task](#Task)
* [Flashcard](#Flashcard)
* [Notes](#Notes)
#### **forms.py**
##### Form Classes:
* [LoginForm](#LoginForm)
* [TimerForm](#TimerForm)
* [ChangeTimerForm](#AddTaskForm)
* [ChangeToTaskAddForm](#ChangeToTaskAddForm)
* [EditTaskForm](#EditTaskForm)
* [SignUpForm](#SignUpForm)
* [TimerSettingForm](#TimerSettingForm)
* [AddFlashcardForm](#AddFlashcardForm)
* [AddNoteForm](#AddNoteForm)
* [filterNotesForm](#filterNotesForm)
## Details description
### **Classes**
<hr>
### Timer

##### Functions
##### \_\_init\_\_
The constructor, take in self and a time amount in seconds, will initialize the instance's max
            
    Parameters:
        self (obj) refererence to the obj instance
        m (int)    max amount of time set for the timer 

##### start
The functions will start the timer and countdown every 1 second, when timer reached 0, notify the user that timer is stopped, and switch to break timer if the user has the auto break setting on

    Parameters:
        self (obj)                  a reference to this object instance
        global autoBreak (bool)     a boolean that keep track of user's auto entering break timer setting when finished the timer     
        global timerStopped(bool)   a boolean to indicate when the timer is stopped, used to stop the while loop
        global timerRemain (int)    an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly
        global timerType (str)      a string indicates which type of timer is chosen from the change timer form
        global timerMessage (str)   a string stored message regarding the timer        
##### reset
reset the timer countdown to max time
    
    Parameters:
        self (obj)                  a reference to this object instance
        global timerRemain (int)    an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly
##### stop
stops the timer by signaling with timerStopped flag and notifies the user with a message

    Parameters:
        self (obj)                  a reference to this object instance
        global timerStopped(bool)   a boolean to indicate when the timer is stopped, used to stop the while loop
        global timerType (str)      a string indicates which type of timer is chosen from the change timer form
        global timerMessage (str)   a string stored message regarding the timer    
##### change_time
change the max time of timer and the remaining time

    Parameters:
        self (obj)                      a reference to this object instance
        time (int)                      an integer presents amount of time in seconds
        global timerRemain (int)        an integer used to display the timer numbers in the template, javascript will read this in the data-time attribute, then display the format properly

### User
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
##### Functions
##### set_password
This function will help set password for user using hash function
    
    Parameters:
        self (obj)          reference to this class instance
        password (string)   a string containing password
##### check_password
this function will check the password using hash function, return a boolean

    Parameters:
        self (obj)          reference to this class instance
        password (string)   a string containing password

    Returns:
        a boolean indicate if the password matches
### Task
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
### Notes

### Flashcard


### **Functions**
<hr>

### log
to notify the user that they logged in

    Returns:
        a string message to inform user their logged in status
### logout
will log out the current user and redirect back to the login page
        
    Returns:
        redirecting back to the page
### login
returns the sign in page when navigating to /login and controls the log in form, 
The log in page will be initially displayed when user starts the app 

    Returns:
            redirecting back to the page
        or
            a html corresponding to the login page that holds form for user to sign in
### signup
returns the sign up user page when navigating to /signup and controls the sign up form 

    Returns:
            redirecting back to the page
        or
            a html corresponding to the sign up page that holds form for user to register new user
### signedup
returns the signedup.html to notify user successful sign up and give them option to sign in later

    Returns:
        a html to notify that user succesfully signed up
### notes
### flashcard
### timer
This function will

1. Control forms: the timer form, add task form, change timer form, edit taskform, and timer 
2. Set up the timer accordingly to task timer or break timer based on the global variables

Besides, it will render the timer html portion of the app when user navigate to /timer route or click timer link in the navigation bar at the top

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
### edit_task
function trigger when user click edit a task, will toggle edit form underneath the task based on its id when user click Edit

    Parameters:
        taskid (int):      a task id
        editing (boolean): a global variable to indicate if edit form is toggled on
        editTaskID (int):  a global varialbe to keep track the current task to be edited so proper form can be displayed according to task id
        
    Returns:
        redirecting route back to the /timer 
### delete_task
function trigger when user click delete task, will delete a task using its id 

    Parameters:
        taskid (int): a task id

    Returns:
        redirecting route back to the /timer 
### finish_task
function trigger when user click finish task, will mark a particular task finished using its id in the user tasks
also mark the finished date
    
    Parameters:
        taskid (int): a task id

    Returns:
        redirecting route back to the /timer
### timer_setting
function trigger when user click "Customize timer", set the global
variable timerSetting to true to toggle on the timer setting form

    Parameters:
        timerSetting (boolean) a global variable keep track if the setting form for timer is on

    Returns:
        redirecting route back to the /timer route
### home
renders the home page of the app after the user logged in or sends the user to login page when they did not sign in

    Returns:
            html to home page if user logged in
        Or
            html to login page otherwise 