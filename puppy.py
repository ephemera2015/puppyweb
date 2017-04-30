#-*-coding:utf-8-*-
import os
from flask import Flask,g

app=Flask(__name__)
app.config.from_pyfile('config.py')

from models import *

@app.before_request
def before_request():
    connectDataBase(app.config['DATABASE'])

@app.teardown_request
def teardown_request(rv):
    closeDataBase()
    
from views import *

if __name__=='__main__':
    app.run()

