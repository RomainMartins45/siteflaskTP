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
    
    def get_id(self):
        return self.id
    
class AuthorForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Nom",validators =[DataRequired()])

class SearchForm(FlaskForm):
    nomAuteur = StringField("Poids",validators =[DataRequired()])

class User(db.Model,UserMixin):
    username = db.Column(db.String(50) ,primary_key = True)
    password = db.Column(db.String(64))
    
    def get_id(self):
           return (self.username)

class Favorites(db.Model):
    book_id = db.Column(db.Integer , db.ForeignKey("book.id"),primary_key = True)
    user_username = db.Column(db.String(50) , db.ForeignKey("user.username"),primary_key = True)

    def get_user(self):
        return self.user_username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def get_sample():
    return Book.query.all()

def get_sample2():
    return Author.query.limit(10).all()

def get_author(id):
    return Author.query.filter(Author.id == id).first()

def is_favorite(username,book_id):
    favori = Favorites.query.filter(Favorites.user_username == username, Favorites.book_id == book_id).all()
    if favori == []:
        return False
    else:
        return True

def user_existe(username):
    user = User.query.filter(User.username == username).all()
    return user != []

def get_book_from_author(id):
    book = Book.query.filter(Book.author_id == id).all()
    return book

    