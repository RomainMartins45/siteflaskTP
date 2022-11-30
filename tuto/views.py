import os
from .app import app, db
from flask import render_template, url_for, redirect
from .models import Author, Book, get_author, get_sample, get_sample2, AuthorForm
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired

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

