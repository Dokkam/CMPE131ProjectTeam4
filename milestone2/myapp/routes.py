import os, re, markdown
from myapp import myapp_obj, basedir
from myapp.forms import LoginForm, RegisterForm, FileForm, uploadForm, SearchForm
from flask import Flask, render_template, flash, redirect, request, url_for
from myapp import db
from myapp.models import User, Note, todo_list
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

@myapp_obj.route("/loggedin")
@login_required
def log():
    return("You are logged in")

@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/') #link is pressed and will redirect user to home page

@myapp_obj.route("/")
def index():
    title = 'Studious HomePage'
    return render_template("index.html", title=title)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
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

@myapp_obj.route("/register" ,methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username is existed')
            return redirect("/register")
        new_user = User(username=form.username.data, password=form.password.data) #records input of username and password
        new_user.set_password(new_user.password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html",form=form)

@myapp_obj.route("/delete")
@login_required
def delete():
    user = User.query.filter_by(id=1).delete() #should delte first user from user table
    db.session.commit()
    return redirect("/register")

# code for To-Do list
@myapp_obj.route('/todolist')
def todolist():
    title = 'To-Do List'
    complete = todo_list.query.filter_by(complete=True).all()
    incomplete = todo_list.query.filter_by(complete=False).all()
  
    return render_template('todolist.html', title = title,complete = complete, incomplete = incomplete)


@myapp_obj.route("/add", methods=['POST'])
def add():
    todo = todo_list(todo_item = request.form["todoitem"], complete = False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('todolist'))

@myapp_obj.route("/complete/<id>")
def complete(id):
    todo = todo_list.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('todolist'))

# code for upload
@myapp_obj.route('/notes', methods=['GET', 'POST'])
def upload_note():
    title='Note List:'

    form = FileForm()
    if form.validate_on_submit():
        f = form.file.data

        filename = secure_filename(f.filename)
        f.save(os.path.join(
            basedir, 'notes', filename
        ))
        flash('Uploaded note successfully')

    filenames = os.listdir(os.path.join(basedir, 'notes'))
    note_titles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    return render_template('notes.html', 
        form=form, 
        title=title, 
        note_titles=note_titles
    )

@myapp_obj.route('/note/<title>')
def show_note(title):
    filenames = os.listdir(os.path.join(basedir, 'notes'))
    note_titles = list(sorted(re.sub(r"\.md$", "", filename)
        for filename in filenames if filename.endswith(".md")))

    if title in note_titles:
        with open(os.path.join(f"{basedir}/notes/{title}.md"), 'r') as f:
            text = f.read()
            return render_template('note.html',
                note=markdown.markdown(text),
                title=title)
    return redirect('/')

    # Code to render markdown files into flash cards
@myapp_obj.route("/renderFlashCard", methods=['GET', 'POST'])
def markdownToFlashcard():
    title = 'Flash Cards'
    form = uploadForm()
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
    search = SearchForm()
    if search.validate_on_submit():
        result = search.result.data

        # Navigate note handler
        if result.startswith('[[') and result.endswith(']]'):
            title = re.search('\[\[(.*?)\]\]', result).group(1)
            return redirect(url_for('show_note', title=title))

        filenames = os.listdir(os.path.join(basedir, 'notes'))
        results = []
        for filename in filenames:
            note = os.path.join(f"{basedir}/notes/{filename}")
            with open(note, 'r') as f:
                content = f.read()
                if result in content:
                    content = content.replace(result, f'<mark>{result}</mark>')
                    note = {
                        'title': filename,
                        'content': markdown.markdown(content)
                    }
                    results.append(note)
                    
        
        return render_template('result.html', results = results)    
    return render_template('search.html', form = search)
