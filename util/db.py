import os
import sqlite3

# CREATE TABLE users( username TEXT primary key, pw text);
# CREATE TABLE quiz( id integer primary key, name text, owner text);
# CREATE TABLE content( term text, definition text);
# CREATE TABLE folders( owner text, name text, id integer primary key, quizzes text);


def login(user_check, pw_check):
    '''Verifies username matches with pw'''
    x = os.path.abspath("data/database.db")
    print(x)
    db = sqlite3.connect("data/database.db")
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
    db = sqlite3.connect("data/database.db")
    cursor = db.cursor()
    errs = [0,0,0,0,0]
    for x,y in enumerate([user,pw,cpw]):
        if len(y.strip()) == 0:
            errs[x] = 1
    command = "SELECT username FROM users"
    cursor.execute(command)
    temp = cursor.fetchall()
    print(temp)
    users = [x[0] for x in temp]
    print(users)
    if user in users:
        #case that username is taken -> 0
        errs[3] = 1
    if pw != cpw:
        #case that pw's dont match
        errs[4] = 1
    print(errs)
    if sum(errs)==0:
        cmd = "INSERT INTO users VALUES(?, ?)"
        params = (user.strip(), pw)
        cursor.execute(cmd, params)

        #cmd = "SELECT * FROM users"
        #a = cursor.execute(cmd);
        #for i in a:
        #    print(i)

        db.commit()
        db.close()
    return errs

def make_quiz(quiz_name, owner):
    '''Create quiz'''
    # Contents table has quizid as table name
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()

    #-----------get quiz id------------------
    cmd = "SELECT id FROM quiz"
    id_list = cursor.execute(cmd).fetchall()
    print(len(id_list))
    new_id = len(id_list)

    #---------- insert new quiz -------------
    cmd = "INSERT INTO quiz VALUES(?, ?, ?)"
    params = (new_id, quiz_name, owner)
    cursor.execute(cmd, params)

    cmd = "SELECT * FROM quiz"
    a = cursor.execute(cmd);
    for i in a:
        print(i)

    db.commit()
    db.close()

    make_content( new_id )

    return new_id 

def make_content( quiz_id ):
    '''Creates table of quiz contents for each quiz'''
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()

    quiz_id = "q" + str(quiz_id)

    cmd = "CREATE TABLE IF NOT EXISTS {q} (term STRING, def STRING)".format(q=quiz_id)
    #params = (quiz_id)
    cursor.execute(cmd)

    db.commit()
    db.close()

def get_content( quiz_id ):
    '''get contents of a quiz (table name is quiz_id)'''
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()

    quiz_id = "q" + str(quiz_id)

    cmd = "SELECT * FROM {q}".format(q=quiz_id)
    data = cursor.execute(cmd).fetchall()
    db.close()

    print(data)

#get_content( 3 )
#make_content( 0 )
#make_quiz('bquiz', 'b')
#register('c','c')
#print(login('test', '123'))
