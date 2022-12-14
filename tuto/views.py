import os
from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import Author, Book, get_author, get_sample, get_sample2, AuthorForm
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired
from wtforms import PasswordField
from .models import User
from hashlib import sha256
from flask_login import login_user, current_user,login_required,logout_user

app.config['SECRET_KEY'] = "7661d666-10ea-4157-9d59-70cf3502dc2e"

@app.route("/")

def home():
    return render_template("home.html",title ="Hello World!",names =["Pierre", "Paul", "Corinne"]
                           ,authors = get_sample2())

@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id = a.id,name=a.name)
    return render_template("edit_author.html",author=a,form=f)

@app.route("/detail/<int:id>")
@login_required
def detail(id):
    books = Book.query.filter(Book.author_id == id).all()
    return render_template("detail.html",book=books)

@app.route("/save/author/",methods =["POST"])
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    a = get_author(int(f.id.data))
    return render_template("edit_author.html",author =a, form=f)

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    next = HiddenField()
    
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/login/", methods =("GET","POST",))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("login.html",form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/favorites/<String:username>")
def favorites(user):
    return None