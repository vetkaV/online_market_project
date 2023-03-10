import sqlite3

db_name = 'usersInfo.sqlite'

conn=None
cursor=None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    
    do('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY not null, 
            login VARCHAR not null,
            password VARCHAR not null, 
            email VARCHAR not null,
            phone INTEGER not null)'''
       )
    
    do('''INSERT INTO users (login, password, email, phone) values ('admin', 'admin', 'admin@corp.ru', '87775553535')''')

def get_succes_auth(login, pass_w):
    open()
    cursor.execute('''select * from users where login == (?)''', [login])
    result = cursor.fetchone()
    close()
    print(result)
    if result != None:
        return str(result[1]) == login and str(result[2]) == pass_w
    else:
        return False
def check_login_email(login, email):
    open()
    cursor.execute('''select * from users where login == (?) or email == (?)''', [login, email])
    result = cursor.fetchall()
    close()
    if result != None and len(result) > 0:
        return False
    else:
        return True
def create_user(login, pass_w, email, phone):
    if check_login_email(login, email):
        open()
        cursor.execute('''insert into users (login, password, email, phone) values (?, ?, ?, ?)''', [login, pass_w, email, phone])
        print('succesful')
        conn.commit()
        close()
        return True
    else:
        return False


def main():
    #pass
    create()

if __name__ == "__main__":
    main()