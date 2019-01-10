import sqlite3

# CREATE TABLE users( username TEXT primary key, pw text);
# CREATE TABLE quiz( id integer primary key, name text, owner text);
# CREATE TABLE content( term text, definition text);
# CREATE TABLE folders( owner text, name text, id integer primary key, quizzes text);


def login(user_check, pw_check):
    '''Verifies username matches with pw'''
    db = sqlite3.connect('../data/database.db')
    cursor = db.cursor()

    cmd = "SELECT pw FROM users WHERE users.username = ?"
    params = (user_check,)
    cursor.execute(cmd, params)
    check = cursor.fetchone()

    db.commit()
    db.close()

    if check == None:
        # username doesnt exist
        print("usrname dont exist")
        return False
    return check[0] == pw_check

    


def register(user, pw):
    '''Add user to db'''
    db = sqlite3.connect('../data/database.db')
    cursor = db.cursor()

    cmd = "INSERT INTO users VALUES(?, ?)"
    params = (user, pw)
    cursor.execute(cmd, params)
    cmd = "SELECT * FROM users"

    #a = cursor.execute(cmd);
    #for i in a:
    #    print(i)

    db.commit()
    db.close()


#register('c','c')
#print(login('test', '123'))
