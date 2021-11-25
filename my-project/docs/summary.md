# Summary of classes and functions 

## Lists of classes and functions

#### **routes.py**
##### Classes:
* [Timer](#timer)
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
* [getNote()](#getnote)
* [flashcard()](#flashcard)
* [timer()](#timer)
* [edit_task()](#edit_task)
* [delete_task()](#delete_task)
* [finish_task()](#finish_task)
* [timer_setting()](#timer_setting)
* [home()](#home())
* [flashcard()](#flashcard)
* [share_flashcard()](#share_flashcard)
* [next_flashc()](#next_flashc)
* [prev_flashc()](#prev_flashc)
* [hide_flash()](#hide_flash)
* [reveal_flash()](#reveal_flash)
* [flash_md()](#flash_md)

#### **models.py**
##### Model Classes
* [User](#user)
    * [set_password()](#set_password)
    * [check_password()](#check_password)
* [Task](#task)
* [Flashcard](#flashcard)
* [Notes](#notes)
    * [set_password()](#notes_set_password)
    * [check_password()](#notes_check_password)
#### **forms.py**
##### Form Classes:
* [LoginForm](#loginform)
* [TimerForm](#timerform)
* [ChangeTimerForm](#addtaskform)
* [ChangeToTaskAddForm](#changetotaskaddform)
* [EditTaskForm](#edittaskform)
* [SignUpForm](#signupform)
* [TimerSettingForm](#timersettingform)
* [AddFlashcardForm](#addflashcardform)
* [AddNoteForm](#addnoteform)
* [filterNotesForm](#filternotesform)
* [ShareFlashcardForm](#shareflashcardform)
* [FlashcardToPDF](#flashcardtopdf)
* [ControlsBetweenFlashcardInViewForm](#controlsbetweenflashcardinviewform)
* [RenderMarkdownfileToFlashCardForm](#rendermarkdownfiletoflashcardform)
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
## **Model classes**
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
#### Functions
##### Notes_set_password
This function will help set password for the note using hash function

    Parameters:
        self (obj)          reference to this class instance
        password (string)   a string containing password
##### Notes_check_password
this function will check the password using hash function, return a boolean

    Parameters:
        self (obj)          reference to this class instance
        password (string)   a string containing password

    Returns:
        a boolean indicate if the password matches
### Flashcard
A model presents the flashcard added by the user in the flashcard feature

    Relationships with:
        User        Many-to-One
    
    Data Fields:
        id (int)            unique id integer of the flashcard
        title (str)         title string of the the flashcard
        description (str)   description string of the flashcard
        date_started (Date) a date when the flashcard was added
        user_id (int)       id of the user who owned the task
### **Form Classes**
### LoginForm
Controling login related feature fields

    Form fields:
        username (str)      a string field indicate username
        password (str)      a string field indicate password 
        remember_me (bool)  a boolean field to indicate if user want to remember the loged in session
        submit              a submit field when user click Sign in
        signup              a submit field when user click Sign up
### TimerForm
this form class control the timer buttons to start, stop, and reset the timer

    Form fields:
        start_timer         a submit field when user click Start timer
        stop_timer          a submit field when user click Stop timer
        reset_timer         a submit field when user click Reset timer
### ChangeTimerForm
this form class will control the toggle between break timer and task timer

    Form fields:
        task_timer           a submit field when user click Task timer
        break_timer          a submit field when user click Break timer
### AddTaskForm
this form class will control the add task form
    
    Form fields:
        title (str)         a string field indicate title of task
        note (str)          a string field indicates note of task
        add_task            a submit field triggered when user hit Add task
        cancel              a submit field triggered when user hit Cancel
### ChangeToTaskAddForm
this form class will toggle the add task form 

    Form fields:
        submit              a submit field triggered when user click Add new task
### EditTaskForm
this form class will control the edit task form, will be toggled when user click Edit

    Form fields:
        confirm             a submit field triggered when user click Confirm change
        cancel              a submit field triggered when user click Cancel
        title (str)         a string field indicates Task title
        note (str)          a string field indicates Task 's note
### SignUpForm
this form class will control the sign up form

    Form fields:
        username (str)      a string field indicate username
        password (str)      a string field indicate password
        email (str)         a string field indicate email     
        submit              a submit field triggered when user click Add me
        login              a submit field triggered when user click Take me back  
### TimerSettingForm
this form class will control the timer customize or setting form

    Form fields:
        task_time (int)     an integer field indicate task time amount
        break_time (int)    an integer field indicate break time amount
        auto_break (bool)   an boolean field to tell if user want to auto start the break time when the timer finished
        confirm             a submit field triggered when user click Confirm change
        cancel              a submit field triggered when user click Cancel
### AddFlashcardForm
this form class will control the add flashcard form
    
    Form fields:
        title (str)         a string field indicate title of flashcard
        descrition (str)    a string field indicates description of flashcard
        add                 a submit field triggered when user hit Add
        cancel              a submit field triggered when user hit Cancel
### ShareFlashcardForm
this form class will control the share flashcard form
    
    Form fields:
        username (str)      a string field indicate destination username to the flashcard with
        submit              a submit field triggered when user hit Share

### FlashcardToPDF
this form class will control the flashcard to PDF form
    
    Form fields:
        submit              a submit field triggered when user hit Output flashcards to PDF file
### ControlsBetweenFlashcardInViewForm
this form class will control the next and previous button the flashcard route
    
    Form fields:
        prev              a submit field triggered when user hit Previous
        next              a submit field triggered when user hit Next
### RenderMarkdownfileToFlashCardForm
this form class will control the form that take a fil
    
    Form fields:
        filename(str)   a string field for filename of the markdown file to be converted to flashcards
        submit          a submit field trigger when user click convert markdown to flashcards
### AddNoteForm
This class will allow the user to add a new note

    Form fields:
        title (str)         a string indicate of title
        password (str)      a string field indicate password
        body (str)          a string field indicate body of text
        submit              a submit field when user click Create
### filterNotesForm
This class will allow the user to filter their list of notes

    Form fields:
        filter (str)        a string indicate of desired filter
        submit              a submit field when user click Search
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
This function will:

1. add new notes for the user
2. allow user to view all of their notes
3. allow user to search for notes by keywords

This function render notes html portion of the app when user navigate to /notes route or click notes l>

    Parameters:
        global filtered(bool)                   a flag telling if the user has prompted for a filtered list of the notes
        global filterList(List<Notes>)  a global notes list used to store a list of filtered notes
    Returns:
            redirecting to itself
        or
            a template notes.html of the page corresponding to the route /notes
### getNote
This function will render open_note.html and pass the desired note into it. The end result is that it will display a note

    Parameters:
        noteid (int)        integer indicate id of a note

    Returns:
        a template open_note, displaying the desired note
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
### flashcard
This function will:

1. add new flashcard for the user
2. allow user to share a flash card with another user
3. allow user to convert markdown file to flashcards 
4. allow user to convert flashcards to PDF

This function render flashcards html portion of the app when user navigate to /flashcard route or click flashcard link in the navigation bar at the top
        
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
### share_flashcard
function trigger when user click sharing a flashcard, will toggle sharing form underneath the corresponding flashcard based on its id when user click Share this flashcard

    Parameters:
        flashcardid (int):      a flashcard id integer
        sharing (boolean):      a global variable to indicate if edit form is toggled on
        sharingID (int):        a global varialbe to keep track the current flashcard to be shared so proper form can be displayed according to task id
        
    Returns:
        redirecting route back to the /flashcard
### next_flashc
This function will move to the next flashcard in the list when user click "Next"

    Parameters:
        global flashcardsList(List<Flashcard>)  a global flashcards list used for the entire app
        global currentCard(Flashcard)           a global Flashcard storing the current flashcard so that app can move between the cards in the list with next and previous buttons
    
    Returns:
        redirecting to /flashcard route
### prev_flashc
This function will move to the previous flashcard in the list when user click "Previous"

    Parameters:
        global flashcardsList(List<Flashcard>)  a global flashcards list used for the entire app
        global currentCard(Flashcard)           a global Flashcard storing the current flashcard so that app can move between the cards in the list with next and previous buttons
    
    Returns:
        redirecting to /flashcard route
### hide_flash
This function will hide the description of the card when user click "Reveal description"

    Parameters:
        global revealedCard(bool)       a global boolean variable indicate if the card's description is revealed or not
    
    Returns:
        redirecting to /flashcard route
### reveal_flash
This function will reveal the description of the card when user click "Reveal description"

    Parameters:
        global revealedCard(bool)       a global boolean variable indicate if the card's description is revealed or not
    
    Returns:
        redirecting to /flashcard route
### flash_md
This function will return the flashcards_from_md.html when get to route /flashcards_from_md after use hit "Convert markdown to flashcards" 

It will read from the markdown files then convert them to flashcards, and control forms to move between the flashcards

    Parameters:
        global currentCardInView(Flashcard)     a global Flashcard storing the current flashcard used in the flashcards_from_md route
        filename(str)                           a string of filename passed via the link in flashcard route

    Returns:
        redirecting back to the current route

