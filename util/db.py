import os
import sqlite3

# CREATE TABLE users( username TEXT primary key, pw text);
# CREATE TABLE quiz( id integer primary key, name text, owner text);
# CREATE TABLE content( term text, definition text);
# CREATE TABLE folders( owner text, name text, id integer primary key, quizzes text);

db_path = "data/database.db"


def login(user_check, pw_check):
    '''Verifies username matches with pw'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    command = "SELECT username, pw FROM users"
    cursor.execute(command)
    temp = cursor.fetchall()
    users = dict(temp)
    print(users)
    if user_check not in users:
        return 1

    if users[user_check] != pw_check:
        return 2
    return 0
    # cmd = "SELECT pw FROM users WHERE users.username = ?"
    # params = (user_check,)
    # cursor.execute(cmd, params)
    # check = cursor.fetchone()
    #
    # db.commit()
    # db.close()
    #
    # if check == None:
    #     # username doesnt exist
    #     print("usrname dont exist")
    #     return 1
    # return 0


def register(user, pw, cpw):
    '''Add user to db'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    errs = [0, 0, 0, 0, 0]
    for x, y in enumerate([user, pw, cpw]):
        if len(y.strip()) == 0:
            errs[x] = 1
    command = "SELECT username FROM users"
    cursor.execute(command)
    temp = cursor.fetchall()
    print(temp)
    users = [x[0] for x in temp]
    print(users)
    if user in users:
        # case that username is taken -> 0
        errs[3] = 1
    if pw != cpw:
        # case that pw's dont match
        errs[4] = 1
    print(errs)
    if sum(errs) == 0:
        cmd = "INSERT INTO users VALUES(?, ?)"
        params = (user.strip(), pw)
        cursor.execute(cmd, params)

        # cmd = "SELECT * FROM users"
        # a = cursor.execute(cmd);
        # for i in a:
        #    print(i)

        db.commit()
        db.close()
    return errs


# CREATE TABLE quiz( id integer primary key, name text, owner text);
# CREATE TABLE content( term text, definition text);

def get_user_quiz(user):
    '''
        Get a list of all of a users quizzes
        for home page
    '''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    cmd = "SELECT name FROM quiz WHERE owner='{u}'".format(u=user)
    # print(cmd)
    data = cursor.execute(cmd).fetchall()
    for i in data:
        i = i[0]
        # print(i)
    db.commit()
    db.close()
    return data

def get_user_quizid(user):
    '''
        Get a list of all of a users quizzesids
        for home page
    '''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    cmd = "SELECT id FROM quiz WHERE owner='{u}'".format(u=user)
    # print(cmd)
    data = cursor.execute(cmd).fetchall()
    # for i in data:
    #     i = i[0]
    #     # print(i)
    db.commit()
    db.close()
    return data


def make_quiz(quiz_name, owner):
    '''Create quiz'''
    # Contents table has quizid as table name
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    # -----------get quiz id------------------
    cmd = "SELECT id FROM quiz"
    id_list = cursor.execute(cmd).fetchall()
    print(len(id_list))
    new_id = len(id_list)

    # ---------- insert new quiz -------------
    cmd = "INSERT INTO quiz VALUES(?, ?, ?)"
    params = (new_id, quiz_name, owner)
    cursor.execute(cmd, params)

    cmd = "SELECT * FROM quiz"
    a = cursor.execute(cmd);
    for i in a:
        print(i)

    db.commit()
    db.close()

    make_content(new_id)

    return new_id

def delete_quiz(quizid):
    '''delete quiz'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    cmd = "DELETE FROM quiz WHERE id={q}".format(q=quizid)
    cursor.execute(cmd)
    cmd = "SELECT * FROM quiz"
    a = cursor.execute(cmd).fetchall()
    for i in a:
        print(i)
    cmd = "DROP TABLE {qlist}".format(qlist='q' + str(quizid))
    cursor.execute(cmd)

    db.commit()
    db.close()


def make_content(quiz_id):
    '''Creates table of quiz contents for each quiz'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    quiz_id = "q" + str(quiz_id)

    cmd = "CREATE TABLE IF NOT EXISTS {q} (term STRING, def STRING)".format(q=quiz_id)
    # params = (quiz_id)
    cursor.execute(cmd)

    db.commit()
    db.close()


# CREATE TABLE quiz( id integer primary key, name text, owner text);
# CREATE TABLE content( term text, definition text);

def get_content(quiz_id):
    '''get contents of a quiz (table name is quiz_id)'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    quiz_id = "q" + str(quiz_id)

    cmd = "SELECT * FROM {q}".format(q=quiz_id)
    data = cursor.execute(cmd).fetchall()

    db.commit()
    db.close()

    return data


def add_term(quiz_id, term, definition):
    '''Add a term and definition to a quiz'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    qid = "q" + str(quiz_id)

    cmd = "INSERT INTO {table} VALUES('{term}','{defin}')".format(table = qid, term = term, defin = definition )
    print(cmd)
    data = cursor.execute(cmd)

    db.commit()
    db.close()
    return term


def delete_term(quiz_id, term, definition):
    '''Delete a term from a quiz'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    qid = "q" + str(quiz_id)
    cmd = "DELETE FROM {table} WHERE term='{term}' AND def='{defn}'".format(table = qid, term = term, defn=definition);
    cursor.execute(cmd)
    #cmd = "SELECT * FROM {table}".format(table = qid)
    #data = cursor.execute(cmd).fetchall()
    #print(data)

    db.commit()
    db.close()

def get_quizname( quizid ):
    ''' return quiz name given quiz id'''
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    qid = quizid
    cmd = "SELECT name FROm quiz WHERE id={q}".format(q=qid)
    name = cursor.execute(cmd).fetchall()[0][0]
    db.close()
    
    return name

#get_quizname( 10 )
# delete_term('48', 'aaa', 'bbb');
# get_user_quiz('a')
# get_content( 3 )
# make_content( 0 )
# make_quiz('testquiz', 'a')
# register('jay','sen', 'sen')
# print(login('test', '123'))
