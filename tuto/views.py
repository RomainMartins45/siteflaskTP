from .app import app
from flask import render_template
import yaml , os.path
from yaml import Loader
@app.route("/")




def home():
    return render_template("home.html",title ="Hello World!",names =["Pierre", "Paul", "Corinne"]
                           ,data = yaml.load(open("tuto/static/data.yml"),Loader=Loader))