import os, csv, time, sqlite3, json
from urllib.request import Request, urlopen

from flask import Flask, render_template, request,session,url_for,redirect,flash

import util.db as db

app = Flask(__name__)

app.secret_key = os.urandom(32) #key for session

@app.route('/')
def hello_world():
    if "logged_in" in session:
        return render_template("home.html")
    return render_template("landing.html")

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

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if request.form["submit"] == "login":
        x = request.form["username"]
        y = request.form["password"]
        print(x,y)
        var = db.login(x,y)
        if var == 0:
            session[x] = y
            flash("Logged in!")
            return render_template("home.html", category = "epic_win", flash = True)
        elif var == 1 :
            flash("Username not found!")

        else:
            flash("Incorrect password!")
        return render_template("login.html", category="epic_fail", flash=True)
    else:
        x = request.form["username"]
        y = request.form["password"]
        z = request.form["confirm-password"]
        val = db.register(x,y,z)
        errs = []
        if sum(val) == 0:
            session[x] = y
            flash("Registered and logged in!")
            return render_template("home.html", category="epic_win", flash=True)
        if val[0] == 1:
            errs.append("Username is blank")
        if val[1] == 1:
            errs.append("Password is blank")
        if val[2] == 1:
            errs.append("Confirm Password is blank")
        if val[3] == 1:
            errs.append("Username taken")
        if val[4] == 1:
            errs.append("Passwords don't match")
        flash("Please correct the following errors:")
        for x in errs:
            flash(x)
        return render_template("register.html", category="epic_fail", flash=True)



@app.route("/logout")
def logout():
    session.pop("logged_in")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
