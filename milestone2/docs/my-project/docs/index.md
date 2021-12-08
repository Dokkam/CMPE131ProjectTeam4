## Install
* `brew install python3` - Install Python itself
* `pip3 install flask` - Install Flask
* `pip3 install sqlalchemy` - Install Sqlalchemy
* `pip3 install -U Flask-WTF` - Install WTF Forms
* `pip3 install Flask-Markdown` - Install Markdown
* `pip3 install Flask-Login` - Install Flask Login Extension

## Start
* Open project directory and type `python3 run.py`
* Open `http://127.0.0.1:5000/` in the browser

## Project layout
Studious/
  StudiousDocs/
    docs/
      index.md  		    # The documentation homepage
      routes.md	        # Lists classes/functions in each file
      mkdocs.yml
  myapp/
    templates/ 		      # Contains all the html pages
    flashcards/         # Flashcard Directory
    notes/              # Notes Directory       
    app.db         		  # Database
    __init__.py    		  # Configuration of projects
    forms.py       		  # Class forms for implementation UI
    models.py      		  # Class models for database
    routes.py      		  # routers
  .gitignore
  run.py             		# Python file to run the website
  Specifications.md  		# Use cases markdown file