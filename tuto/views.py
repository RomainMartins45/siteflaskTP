import os
from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import Author, Book, get_author, get_sample, get_sample2, AuthorForm,Favorites
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired
from wtforms import PasswordField
from .models import User, is_favorite, user_existe
from hashlib import sha256
from flask_login import login_user, current_user,login_required,logout_user

app.config['SECRET_KEY'] = "7661d666-10ea-4157-9d59-70cf3502dc2e"

@app.route("/")

def home():
    return render_template("home.html",authors = get_sample2())

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
        return user if self.password.data == user.password else None

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

@app.route("/register", methods =("GET","POST",))
def register():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user is None:
            password = f.password.data
            name = f.username.data
            if not user_existe(name,password):
                user = User(username = name,password = password) 
                db.session.add(user)
                db.session.commit()
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("register.html",form=f)

@app.route("/register")
def go_to_register():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("register.html",form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/favorites/<username>")
def favorites(username):
    favoris = Favorites.query.filter(Favorites.user_username == username).all()
    books = list()
    for favori in favoris:
        book = Book.query.filter(Book.id == favori.book_id).first()
        books.append(book)
    return render_template("favoris.html",books=books)

@app.route("/books")
def books():
    return render_template("books.html",book=get_sample())

@app.route("/detail_book/<int:id>")
def detail_book(id):
    books = get_sample()
    for livre in books:
        if livre.get_id() == id:
            book = livre
    return render_template("detail_book.html",book=book)

@app.route("/favorites/<username>/<int:book_id>")
def add_favoris(username,book_id):
    if not is_favorite(username,book_id):
        favoris = Favorites(book_id = book_id,user_username= username)
        db.session.add(favoris)
        db.session.commit()
    return favorites(username)

@app.route("/favorites/<username><int:book_id>")
def sup_favoris(username,book_id):
    print(is_favorite(username,book_id))
    if is_favorite(username,book_id):
        Favorites.query.filter(Favorites.user_username == username , Favorites.book_id == book_id).delete()
        db.session.commit()
    return favorites(username)

@app.route("/books/<int:book_id>")
def sup_book(book_id):
    book = Book.query.filter(Book.id == book_id).first()
    db.session.delete(book)
    db.session.commit()
    return render_template("books.html",book=get_sample())  
