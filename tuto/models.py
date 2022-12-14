from .app import db
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms . validators import DataRequired
from flask_login import UserMixin
from .app import login_manager

class Author(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self) -> str:
        return "<Author (%d) %s>" % (self.id, self.name)

class Book(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(200))
    img = db.Column(db.String(200))
    author_id = db.Column(db.Integer , db.ForeignKey("author.id"))
    author = db.relationship("Author",backref=db.backref("books", lazy="dynamic"))

    def __repr__(self) -> str:
        return "<Book (%d) %s>" % (self.id, self.title)
    
class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom",validators =[DataRequired()])

class User(db.Model,UserMixin):
    username = db.Column(db.String(50) ,primary_key = True)
    password = db.Column(db.String(64))
    # book_id = db.Column(db.Integer , db.ForeignKey("book.id"))
    # book = db.relationship("Book",backref=db.backref("users", lazy="dynamic"))

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def get_sample():
    return Book.query.limit(10).all()

def get_sample2():
    return Author.query.limit(10).all()

def get_author(id):
    return Author.query.filter(Author.id == id).first()