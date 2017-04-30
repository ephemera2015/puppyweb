#-*-coding:utf-8-*-

from flask import request,session,g,redirect,url_for,abort,render_template,flash,Response,jsonify
from puppy import app
from models import *
from functools import wraps

def save_file(file_name,file_obj):
    with open(file_name,'wb') as f:
        f.write(file_obj.read())

def logged_in_required(fun):
    @wraps(fun)
    def wrapper(*a,**b):
        if not session.get('logged_in',None):
            return jsonify(status=False)
        else:
            return fun(*a,**b)
    return wrapper
    
def user_check(name,pwd):
    return dbsession.query(User).filter(and_(User.name==name,User.pwd==pwd)).count()==1
    
def file_type(file_name):
    return file_name.split('.')[-1]
