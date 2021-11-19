from myapp import myapp_obj
from myapp.forms import LoginForm, RegisterForm
from flask import render_template, flash, redirect,request
from myapp import db
from myapp.models import User, Post
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
