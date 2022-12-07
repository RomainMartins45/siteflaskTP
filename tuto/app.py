from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path

app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

def mkpath(p):
    return os.path.normpath(
    os.path.join(
    os.path.dirname(__file__),
    p))
    
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+ mkpath("../tuto.db"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)