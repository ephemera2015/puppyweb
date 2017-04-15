#-*-coding:utf-8-*-
import sqlite3#sqlite3是一种微型的关系型数据库，关系型数据库采用sql语言操作

def connect_db(db_name):#链接到数据库
    return sqlite3.connect(db_name)
    
def init_db():#初始化数据库，在数据库中创建模式（参见sql数据库的模式，其实就是schema.sql中定义的一些表）
    db=connect_db('./database.db')
    with open('schema.sql') as f:
        db.cursor().executescript(f.read())#关系型数据库编程中，有个非常重要的概念cursor(游标)
    db.commit()
    db.close()
    
if __name__=='__main__':
    init_db()
