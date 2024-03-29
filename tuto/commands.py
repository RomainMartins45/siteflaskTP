import click
from .app import app , db
from .models import User
from hashlib import sha256
@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data. '''
    # création de toutes les tables
    db.create_all()
    # chargement de notre jeu de données
    import yaml
    books = yaml.load(open(filename),Loader=yaml.Loader)
    # import des modèles
    from .models import Author, Book
    # première passe : création de tous les auteurs
    authors = {}
    for b in books :
        a = b["author"]
        if a not in authors:
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()
    # deuxième passe : création de tous les livres
    for b in books :
        a = authors[b["author"]]
        o = Book(price = b["price"],
        title = b["title"],
        url = b["url"] ,
        img = b["img"] ,
        author_id = a.id)
        db.session.add(o)
    db.session.commit()

@app.cli.command()
def syncdb():
    """Creates all missing tables ."""
    db.create_all()

@app.cli.command()
@click.argument("username")
@click.argument("password")
def newuser(username ,password):
    """Adds a new user."""
    u = User(username =username, password =password)
    db.session.add(u)
    db.session.commit()