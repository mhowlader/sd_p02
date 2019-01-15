import os, csv, time, sqlite3, json
from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

import util.db as db

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session


@app.route('/')
def hello_world():
    if len(session) != 0:
        return render_template("home.html", logged=True)
    return render_template("landing.html")


@app.route("/register")
def register():
    if len(session) != 0:
        return render_template("home.html", logged=True)
    return render_template("register.html")


@app.route("/login")
def login():
    if len(session) != 0:
        return render_template("home.html", logged=True)
    return render_template("login.html")


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    try:
        print("~~~~~~~~~~~~~~LOGGING IN~~~~~~~~~~~~~~")
        print(request)
        print(request.form)
        if request.form["submit"] == "login":
            x = request.form["username"]
            y = request.form["password"]
            print(x, y)
            var = db.login(x, y)
            if var == 0:
                session[x] = y
                flash("Logged in!")
                user=x
                return render_template("home.html", category="epic_win", flash=True, logged=True)
            elif var == 1:
                flash("Username not found!")
            else:
                flash("Incorrect password!")
            return render_template("login.html", category="epic_fail", flash=True)
        else:
            x = request.form["username"]
            y = request.form["password"]
            z = request.form["confirm-password"]
            val = db.register(x, y, z)
            errs = []
            if sum(val) == 0:
                session[x] = y
                flash("Registered and logged in!")
                return render_template("home.html", category="epic_win", flash=True, logged=True)
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
    except:
        if len(session) != 0:
            return render_template("home.html", logged=True)
        return render_template("landing.html")


@app.route('/signout')
def signout():
    if len(session) != 0:
        session.clear()
        flash("Logged out!")
        return render_template("landing.html", category="epic_logout", flash=True)
    return render_template("landing.html")


@app.route('/public_sets')
def public_sets():
    if len(session) != 0:
        return render_template("public_sets.html", logged=True)
    return render_template("public_sets.html")


@app.route('/create')
def create():
    if len(session) != 0:
        return render_template("create.html", logged=True)
    return render_template("landing.html")

@app.route('/contact')
def contact():
    if len(session) != 0:
        return render_template("contact.html", logged=True)
    return render_template("contact.html")

@app.route("/create_auth", methods=['GET', 'POST'])
def create_auth():
    try:
        print("~~~~~~~~~~~~~~~~~ADDING A SET~~~~~~~~~~~")
        # print(list(session.items()))
        user = list(session.items())[0][0]
        # print(user)
        # print(request)
        # print(request.form)
        title = request.form["title"]
        count = request.form["count"]
        terms = []
        defs = []
        # print(title)
        # print(count)
        quizid = db.make_quiz(title, user)
        print("QUIZID: " + str(quizid))
        for x in range(int(count)):
            term = request.form["term" + str(x)]
            definition = request.form["def" + str(x)]
            db.add_term(quizid, term, definition)
        flash ("Successfully added!")
        return render_template("view.html", info = db.get_content(quizid), logged = True, category = "epic_win", flash = True)
    except:
        if len(session) != 0:
            flash("Something bad happened...")
            return render_template("create.html", logged=True, category = "epic_fail", flash = True)
        return render_template("landing.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
