# Welcome to Unforgettable documentation

## How to run the app
1. Clone the project from git repo at [Github](https://github.com/anhquangsjsu/team3_cs131).
2. From ubuntu terminal, run command `pip install pdfkit`
3. then run command `sudo apt-get install wkhtmltopdf`
4. From team3_cs131 folder, run the command  `python3 run.py`
5. The login page will appear, either login using your own account or create account by signup
6. When signed in, user will be able to use the 3 services offered by Unforgettable: 
    * Flash cards to study terms
    * Notes to memorize important information
    * Pomodoro timer to help focus in doing tasks 

## Dependencies

* pdfkit
* wkhtmltopdf

## Project layout
    README.md               # a read me file, some instruction is listed there
    Specification.md        # markdown file store the usecase descriptions and 
    requirements of the project
    run.py                  # to run the app
    myflashcards.pdf        # the output file after user convert their flashcards to PDF
    gantt.xlsx              # excel file containing the gantt chart of the team
    myapp/                  # my app 
        __init.py__         # initialization code.
        app.db              # database for the app
        forms.py            # forms container
        models.py           # table definition for the database
        routes.py           # route to navigate through the app
        template/               #place to store the html templates
            flashcards_from_md.html     # Page to display flashcards after user input a markdown file
            base.html                   # starting page for other pages to extend
            flashcard.html              # flashcard page of the app
            home.html                   # user will be send to here after loged in
            login.html                  # where user will login and sign up account
            notes.html                  # notes page of the app
            open_note.html              # page link to a note when user choose to display a note from a list
            signedup.html               # Page notify if user successfully signed up 
            signup.html                 # Page for user to sign up
            timer.html                  # timer feature page of the app
        mdfiles/                #place to store the testing markdown files used to convert to flashcards
            test.md                     # a test file to be converted from .md to flashcards
            test2.md                    # a test file to be converted from .md to flashcards
    my-project/             # the mkdocs files resigned here
        mkdocs.yml          # mkdocts configurations are here
        docs/                   # the pages of the documentation website
            index.md                    # the home page
            summary.md                  # the summary page