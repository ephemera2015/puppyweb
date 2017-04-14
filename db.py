#-*-coding:utf-8-*-
import sqlite3

def connect_db(db_name):
    return sqlite3.connect(db_name)
    
def init_db():
    db=connect_db('./database.db')
    with open('schema.sql') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    
if __name__=='__main__':
    init_db()
