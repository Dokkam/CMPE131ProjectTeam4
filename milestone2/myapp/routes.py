from myapp import myapp_obj
from myapp.forms import LoginForm, RegisterForm
from flask import Flask, render_template, flash, redirect, request, url_for
from myapp import db
from myapp.models import User, Post, todo_list
from flask_login import current_user, login_user, logout_user, login_required


@myapp_obj.route("/loggedin")
@login_required
def log():
    return("You are logged in")

@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@myapp_obj.route("/")
def hello():
    name = 'Travis'
    people = {'Travis' : 25}
    title = 'Studious HomePage'
    return render_template("hello.html", name=name, people=people, title=title)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    getuser=User.query.all()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect('/loggedin')
    return render_template("login.html", form=form)


@myapp_obj.route("/notes", methods=['GET','POST'])
def flashcard():
    title='Note Taker:'
    return render_template("notes.html",title=title)

@myapp_obj.route("/register" ,methods=['GET','POST'])
def register():
    form = RegisterForm()
   # all_users = User.query.all()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html",form=form)

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