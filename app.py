import os, csv, time, sqlite3, json
from random import shuffle


from urllib.request import Request, urlopen

from flask import Flask, render_template, request, session, url_for, redirect, flash

import util.db as db

app = Flask(__name__)

app.secret_key = os.urandom(32)  # key for session

#recencrt, quizid
d = {"recentcrt": False, "quizid": -1}

@app.route('/')
def hello_world():
    if len(session) != 0:
        return render_template("home.html", logged=True, user=list(session.items())[0][0])
    return render_template("landing.html")


@app.route("/register")
def register():
    if len(session) != 0:
        return render_template("home.html", logged=True, user=list(session.items())[0][0])
    return render_template("register.html")


@app.route("/login")
def login():
    if len(session) != 0:
        return render_template("home.html", logged=True, user=list(session.items())[0][0])
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
                return render_template("home.html", category="epic_logout", flash=True, logged=True,user=list(session.items())[0][0])
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
                return render_template("home.html", category="epic_logout", flash=True, logged=True,user=list(session.items())[0][0])
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
            return render_template("home.html", logged=True,user=list(session.items())[0][0])
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
    user = "admin"
    quizzes = db.get_user_quiz(user)
    print(quizzes)
    quizids = db.get_user_quizid(user)
    print(quizids)
    user_sets = {}
    for x in range(len(quizzes)):
        user_sets[quizzes[x][0]] = quizids[x][0]
    print("Hello")
    print(user_sets)
    if len(session) != 0:
        return render_template("public_sets.html", pubquizzes = user_sets.items(), logged=True,user=list(session.items())[0][0])
    return render_template("public_sets.html",pubquizzes = user_sets.items())


@app.route('/create')
def create():
    if len(session) != 0:
        return render_template("create.html", logged=True,user=list(session.items())[0][0])
    return render_template("landing.html")

@app.route('/contact')
def contact():
    if len(session) != 0:
        return render_template("contact.html", logged=True,user=list(session.items())[0][0])
    return render_template("contact.html")


#info = db.get_content(quizid), logged = True, category = "epic_win", flash = True
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
        d["recentcrt"] = True
        d["quizid"] = quizid
        print("REDIRECTING YOIU TO VIEW QUID ID :" + str(quizid))
        print("VIEW_STORY IS " + str(d["quizid"]))
        return redirect(url_for("view", quizid = quizid))
    except:
        if len(session) != 0:
            flash("Something bad happened...")
            return render_template("create.html", logged=True, category = "epic_fail", flash = True,user=list(session.items())[0][0])
        return render_template("landing.html")

@app.route('/view')
def baseview():
    user = list(session.items())[0][0]
    quizzes = db.get_user_quiz(user)
    print(quizzes)
    quizids = db.get_user_quizid(user)
    print(quizids)
    user_sets = {}
    for x in range(len(quizzes)):
        user_sets[quizzes[x][0]] = quizids[x][0]
    print("hello dude")
    print(user_sets)
    if len(session) != 0:
        return render_template("viewold.html",quizlist = user_sets.items(), logged=True, user=user)
    flash("Log in to access your sets.")
    return render_template("landing.html",category = "epic_fail", flash = True)

def refactor(x):
    return [k[0] for k in x]

@app.route('/view/<quizid>')
def view(quizid):
    print("VIEWING SOME STORY NOW")
    pubquiz = db.get_user_quizid("admin")
    pubquiz = refactor(pubquiz)
    my_quiz = db.get_quizname(quizid)
    print(pubquiz)
    print(int(quizid) in pubquiz)
    if int(quizid) in pubquiz:
        if len(session) != 0:
            return render_template("viewset.html", quizname = db.get_quizname(quizid), info=db.get_content(quizid), logged=True, user=list(session.items())[0][0])
        return render_template("viewset.html", quizname = db.get_quizname(quizid), info=db.get_content(quizid))
    if len(session) != 0:
        flashit = False
        #later add to see if you can actually access that quiz.
        user = list(session.items())[0][0]
        myquizzes = refactor(db.get_user_quizid(user))
        if int(quizid) not in myquizzes:
            flash("Not your quiz, buddy...")
            return render_template("home.html", flash=True, category="epic_fail", logged = True,user=list(session.items())[0][0])
        if d["recentcrt"]:
            flashit, d["recentcrt"] = d["recentcrt"], False
            flash("Successfully updated!")
        return render_template("viewset.html", quizname = db.get_quizname(quizid), info=db.get_content(quizid), logged=True, category="epic_win", flash=flashit,user=list(session.items())[0][0])
    flash("Log in to access your sets.")
    return render_template("landing.html", flash = True, category = "epic_fail")

@app.route("/edit/<quizid>")
def edit(quizid):
    print("editing story")

    pubquiz = db.get_user_quizid("admin")
    pubquiz = refactor(pubquiz)
    my_quiz = db.get_quizname(quizid)
    if int(quizid) in pubquiz:
        admin_name = db.get_quizname(quizid)
        if len(session) != 0:
            return render_template("editset.html",lenset = len(db.get_content(quizid)), quizname = db.get_quizname(quizid), qname=admin_name, qid=quizid, info=dbtodict(db.get_content(quizid)), logged=True, user=list(session.items())[0][0])
        return render_template("viewset.html",  quizname = db.get_quizname(quizid), qid=my_quiz,info=dbtodict(db.get_content(quizid)))
    if len(session) != 0:
        flashit = False
        #later add to see if you can actually access that quiz.
        user = list(session.items())[0][0]
        myquizzes = refactor(db.get_user_quizid(user))
        if int(quizid) not in myquizzes:
            flash("Not your quiz, buddy...")
            return render_template("home.html", flash=True, category="epic_fail", logged = True,user=list(session.items())[0][0])
        # if d["recentcrt"]:
        #     flashit, d["recentcrt"] = d["recentcrt"], False flash("Successfully added!")
        return render_template("editset.html",lenset = len(db.get_content(quizid)),quizname = db.get_quizname(quizid), qname=my_quiz, qid=quizid, info=dbtodict(db.get_content(quizid)), logged=True, category="epic_win", flash=flashit,user=list(session.items())[0][0])
    flash("Log in to edit your quiz.")
    return render_template("landing.html", flash = True, category = "epic_fail")

@app.route("/edit_auth", methods=['GET', 'POST'])
def edit_auth():
    try:
        print("~~~~~~~~~~~~~~~~~Editing A SET~~~~~~~~~~~")
        # print(list(session.items()))
        user = list(session.items())[0][0]
        # print(user)
        # print(request)
        # print(request.form)
        title = request.form["title"]
        count = request.form["count"]
        print(count)
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
        d["recentcrt"] = True
        d["quizid"] = quizid
        print("REDIRECTING YOIU TO VIEW QUID ID :" + str(quizid))
        print("VIEW_STORY IS " + str(d["quizid"]))
        return redirect(url_for("view", quizid = quizid))
    except:
        if len(session) != 0:
            flash("Something bad happened...")
            return render_template("create.html", logged=True, category = "epic_fail", flash = True,user=list(session.items())[0][0])
        return render_template("landing.html")


@app.route("/delete/<quizid>", methods=["POST"])
def delete(quizid):
    print("DEL METHOD")
    print("quiz id = " + quizid)
    data = request.form['delete'].split('%|%')
    term = data[0]
    defin = data[1]
    print("term = " + term)
    print("def = " + defin)
    db.delete_term(quizid, term, defin)
    return redirect(url_for('edit', quizid = quizid))

@app.route("/test/<quizid>", methods=["GET", "POST"])
def take_test(quizid):
    # return redirect(url_for("view", quizid = quizid))
    print("VIEWING SOME STORY NOW")
    pubquiz = db.get_user_quizid("admin")
    pubquiz = refactor(pubquiz)
    my_quiz = db.get_quizname(quizid)
    print("tooof")
    dictlib=db.get_content(quizid)
    doop = [x[1] for x in dictlib]
    print(doop)
    shuffle(doop)
    print(doop)
    if int(quizid) in pubquiz:
        print("Yes")
        if len(session) != 0:
            lisdefs=[x[1] for x in db.get_content(quizid)]
            shuffle(lisdefs)
            return render_template("take_test.html", quizid=quizid, deflist=lisdefs, termlist=[x[0] for x in db.get_content(quizid)],logged=True, user=list(session.items())[0][0])
        flash("Log in to take a test")
        return render_template("landing.html", flash = True, category = "epic_fail")
    print("no")
    if len(session) != 0:
        flashit = False
        #later add to see if you can actually access that quiz.
        user = list(session.items())[0][0]
        myquizzes = refactor(db.get_user_quizid(user))
        if int(quizid) not in myquizzes:
            flash("Not your quiz, buddy...")
            return render_template("home.html", flash=True, category="epic_fail", logged = True,user=list(session.items())[0][0])
        if d["recentcrt"]:
            flashit, d["recentcrt"] = d["recentcrt"], False
            flash("Successfully added!")
        lisdefs=[x[1] for x in db.get_content(quizid)]
        shuffle(lisdefs)
        print(lisdefs)
        return render_template("take_test.html", qid=my_quiz, quizid=quizid, deflist=lisdefs, termlist=[x[0] for x in db.get_content(quizid)], logged=True, category="epic_win", flash=flashit,user=list(session.items())[0][0])
    flash("Log in to access your sets.")
    return render_template("landing.html", flash = True, category = "epic_fail")

@app.route("/grade_test", methods=["POST"])
def grade():
    print ("ya")
    quizid= request.form['quizid']
    count=request.form['count']
    icount=int(count) -1 # real count of sellist
    print(icount)
    print(quizid)
    print("count" + count)
    content=db.get_content(quizid)
    qdict=dict(content)
    cor = 0 # num correct

    for i in range(1,icount + 1):
        term = request.form['sellist' + str(i)]
        print("term" + term)
        if term in qdict:
            print ("yaaa")
            print (qdict[term])
            print (request.form['def' + str(i)])
            if request.form['def' + str(i)]  ==  qdict[term]:
                print ("yaa")
                cor= cor + 1

    fins = str(cor) +  "/" + str(icount)

    return render_template("grade.html", grad = fins )


def dbtodict(info):
    dic = dict()
    for x in info:
        dic[str(x[0])] = str(x[1])
    return dic

@app.route('/study/<quizid>')
def study(quizid):
    print("STUDY SOME STORY NOW")
    pubquiz = db.get_user_quizid("admin")
    pubquiz = refactor(pubquiz)
    my_quiz = db.get_quizname(quizid)
    print(pubquiz)
    print(int(quizid) in pubquiz)
    if int(quizid) in pubquiz:
        if len(session) != 0:
            return render_template("study.html",quizname = db.get_quizname(quizid),  qid=my_quiz,info=dbtodict(db.get_content(quizid)), logged=True, user=list(session.items())[0][0])
        return render_template("study.html",quizname = db.get_quizname(quizid),  qid=my_quiz,info=dbtodict(db.get_content(quizid)))
    if len(session) != 0:
        flashit = False
        #later add to see if you can actually access that quiz.
        user = list(session.items())[0][0]
        myquizzes = refactor(db.get_user_quizid(user))
        if int(quizid) not in myquizzes:
            flash("Not your quiz, buddy...")
            return render_template("home.html", flash=True, category="epic_fail", logged = True,user=list(session.items())[0][0])
        if d["recentcrt"]:
            flashit, d["recentcrt"] = d["recentcrt"], False
            flash("Successfully added!")
        return render_template("study.html",quizname = db.get_quizname(quizid), qid=my_quiz, info=dbtodict(db.get_content(quizid)), logged=True, category="epic_win", flash=flashit,user=list(session.items())[0][0])
    flash("Log in to access your sets.")
    return render_template("landing.html", flash = True, category = "epic_fail")



if __name__ == "__main__":
    app.debug = True
    app.run()
