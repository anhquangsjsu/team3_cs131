# Welcome to Unforgettable documentation

## How to run the app
1. Clone the project from git repo at [Github](https://github.com/anhquangsjsu/team3_cs131).
2. From team3_cs131 folder, run the command  `python3 run.py`
3. The login page will appear, either login using your own account or create account by signup
4. When signed in, user will be able to use the 3 services offered by Unforgettable: 
    * Flash cards to study terms
    * Notes to memorize important information
    * Pomodoro timer to help focus in doing tasks 
## Commands

* `python3 run.py` - To run the program

## Project layout
    README.md
    Specification.md        # markdown file store the usecase descriptions and requirements of the project
    run.py                  # to run the app
    myapp/
        __init.py__         # initialization code.
        app.db              # database for the app
        forms.py            # forms container
        models.py           # table definition for the database
        routes.py           # route to navigate through the app
        template/
            base.html       # starting page for other pages to extend
            flashcard.html  # flashcard page of the app
            home.html       # user will be send to here after loged in
            login.html      # where user will login and sign up account
            notes.html      # notes page of the app
            signedup.html   # Page notify if user successfully signed up 
            signup.html     # Page for user to sign up
            timer.html      # timer feature page of the app

