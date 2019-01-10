import os, csv, time, sqlite3, json
from urllib.request import Request, urlopen

from flask import Flask, render_template, request,session,url_for,redirect,flash

import util

app = Flask(__name__)

app.secret_key = os.urandom(32) #key for session

@app.route('/')
def hello_world():
    if "logged_in" in session:
        return render_template("home.html")
    return render_template("landing.html", logged_in=False, recipes=api.get_recipes(""))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/adduser")
def adduser():
    user = request.args["username"].strip()
    password = request.args["password"]
    passwordc = request.args["confirm-password"]

    if(not user or not password or not passwordc):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(db.check_user(user)):
        flash("User already exists")
        return redirect(url_for("register"))

    if(password != passwordc):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    db.add_user(user, password)
    session["logged_in"] = request.args["username"]
    return redirect(url_for("profile"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
