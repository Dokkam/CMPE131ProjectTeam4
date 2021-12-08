import os, re, markdown
from myapp import myapp_obj, basedir
from myapp.forms import LoginForm, RegisterForm, FileForm, SearchForm, PasswordForm
from flask import Flask, render_template, flash, redirect, request, url_for
from myapp import db
from myapp.models import User, Note, todo_list
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

# User routes
@myapp_obj.route("/logout")
@login_required
def logout():
    '''
    User will be redirected to the splash page
    '''
    logout_user()
    return redirect('/')

@myapp_obj.route("/delete")
@login_required
def delete():
    '''
    User can delete their account when they are logged in
    '''
    user = User.query.filter_by(id=current_user.id).first()
    db.session.delete(user)
    db.session.commit()
    flash('Deleted account successfully')
    return redirect("/register")

@myapp_obj.route("/")
def index():
    '''
    Splash page for the website
    '''
    title = 'Studious HomePage'
    return render_template("index.html", title=title)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    '''
    User can login if they have an already existing account
    
    Parameters:
        String: username
        String: password
    
    Returns:
        User can now access locked features
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return render_template(
                "index.html", 
                title='Studious HomePage',
                user=user
            )
        else:
            flash('Username or password is wrong')

    return render_template("login.html", form=form)

@myapp_obj.route("/changepassword",methods=['GET','POST'])
@login_required
def changepassword():
    '''
    User is able to change their password
    
    Parameters:
        String: new password
    Returns:
        Message letting the user know their password has been changed
        User is redirected to the splash page
    '''
    title = "Change Password"
    form = PasswordForm()
    if request.method == "POST":
         if form.validate_on_submit():
            current_password = form.current_password.data
            if not current_user.check_password(current_password):
                flash('Current password is not correct')
                return render_template("changepassword.html", title=title, form=form)
            
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data
            if new_password != confirm_password:
                flash("New password and confirm password do not match")
                return render_template("changepassword.html", title=title, form=form)

            current_user.set_password(new_password)
            db.session.add(current_user)
            db.session.commit()
            flash("Password updated")
            return redirect("/changepassword")
            
    return render_template("changepassword.html", title=title, form=form)

@myapp_obj.route("/register" ,methods=['GET','POST'])
#Adds new users to table, saving their username and password for future sign in
def register():
    '''
    User enters a username and password for their account
    
    Parameters:
        String: username
        String: password
        
    Returns:
    User is redirected to sign-in page
    '''
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username is existed')
            return redirect("/register")
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.set_password(new_user.password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html",form=form)

# Todo List routes
@myapp_obj.route('/todolist')
def todolist():
    '''
    Sorts the todo items into uncompleted and completed lists
    '''
    title = 'To-Do List'
    complete = todo_list.query.filter_by(complete=True).all()
    incomplete = todo_list.query.filter_by(complete=False).all()
  
    return render_template('todolist.html', title = title,complete = complete, incomplete = incomplete)


@myapp_obj.route("/add", methods=['POST'])
def add():
    '''
    Adds user's inputed item into the uncompleted list
    
    Parameters:
        String: To-do item name
        
    Returns:
        Adds item into uncompleted list
    '''
    todo = todo_list(todo_item = request.form["todoitem"], complete = False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('todolist'))

@myapp_obj.route("/complete/<id>")
def complete(id):
    '''
    Adds the to-do item to the completed list
    '''
    todo = todo_list.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('todolist'))

# Note routes
@myapp_obj.route('/notes', methods=['GET', 'POST'])
def upload_note():
    '''
    User can render markdown files into notes
    
    Parameters:
    file: A markdown file to input (.md, .markdown)
    
    Returns:
    A link (in an unordered list) for user to view uploaded notes
    '''
    title='Note List:'

    form = FileForm()
    if form.validate_on_submit():
        f = form.file.data
        note = Note(content=f.read(), user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash('Uploaded note successfully')
        return redirect('/notes')

    db_notes = Note.query.all()
    notes = []
    for note in db_notes:
        note = note.__dict__
        note['content'] = markdown.markdown(note['content'].decode("utf-8"))
        notes.append(note)

    return render_template('notes.html', 
        form=form, 
        title=title, 
        notes=notes
    )

# Flash Card routes
@myapp_obj.route("/renderFlashCard", methods=['GET', 'POST'])
def markdownToFlashcard():
    '''
    User can render markdown files into flash cards
    
    Parameters:
    A markdown file to input (.md, .markdown)
    (Format of the md file has to be like
        Q:
        A:
    )
    
    Returns:
    A link (in an unordered list) for user to view uploaded flash cards
    
    '''
    title = 'Flash Cards'
    form = FileForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(basedir, 'flashcards', filename))
        flash('Uploaded Flash Cards Successfully!')

    filenames = os.listdir(os.path.join(basedir, 'flashcards'))
    flashCardTitles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    return render_template('flashcards.html', form=form, title=title, cardTitles=flashCardTitles)

@myapp_obj.route('/FlashCard/<title>')
def showFlashCards(title):
    '''
    Allows user to view the flash card after clicking its link
    '''
    filenames = os.listdir(os.path.join(basedir, 'flashcards'))
    flashCardTitles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    if title in flashCardTitles:
        with open(os.path.join(f"{basedir}/flashcards/{title}.md"), 'r') as f:
            text = f.read()
            return render_template('flashcard.html', flashcard=markdown.markdown(text), title=title)
    return redirect('/')   

# code for find text
@myapp_obj.route("/search", methods=['GET', 'POST'])
def search():
    '''
    User can search for specific keywords in their notes, rather than looking through the entire note
    
    Parameters:
        String: keyword to search for
        
    Returns:
        Returns a link to view the notes that contains the keyword
    '''
    search = SearchForm()
    if search.validate_on_submit():
        text = search.text.data

        db_notes = Note.query.all()
        results = []
        for note in db_notes:
            note = note.__dict__
            note['content'] = note['content'].decode("utf-8")
            if text in note['content']:
                note['content'] = note['content'].replace(text, f'<mark>{text}</mark>')
                note['content'] = markdown.markdown(note['content'])
                results.append(note)      
        
        print(results)
        return render_template('result.html', results=results)    
    return render_template('search.html', form=search)

@myapp_obj.route("/splash")
def splashpage():
   
    return render_template("splashpage.html")
