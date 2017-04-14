#-*-coding:utf-8-*-
import os
from flask import Flask,g
from db import *

app=Flask(__name__)
app.config.from_pyfile('config.py')

@app.before_request
def get_db():
    g.db=connect_db(app.config['DATABASE'])
    
@app.teardown_request
def free_db(exception):
    g.db.close()
    
from views import *

if __name__=='__main__':
    app.run()

