#-*-coding:utf-8-*-

import os
from werkzeug import secure_filename
from flask import request,session,g
from flask import redirect,url_for,abort,render_template
from flask import jsonify,flash,Response
from puppy import app
from models import *
from ultils import *
from datetime import datetime

post_mapping={}
get_mapping={}

def register_post(endpoint):
    def foo(fun):
        global post_mapping
        post_mapping[endpoint]=fun
        return fun
    return foo
    
def register_get(endpoint):
    def foo(fun):
        global get_mapping
        get_mapping[endpoint]=fun
        return fun
    return foo
    
@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/index.htm')
def index():
    entries=User.join(Entry).all()
    for entry in entries:
        if entry.eimgs:
            entry.eimgs=entry.eimgs.split('#')
    return render_template('index.html',entries=entries)

@app.route('/get/<cls>/<name>')
def get(cls,name):
    return get_mapping[cls](name)

@app.route('/post/<cls>',methods=['POST',])
def post(cls):
    return post_mapping[cls]()
    
@register_get('image')
def get_image(name):
    image=file(os.path.join(app.config['IMAGE_FOLRDER'],name))
    return Response(image,mimetype='image/jpeg')

@register_get('music')
def get_music(name):
    music=file(os.path.join(app.config['MUSIC_FOLRDER'],name))
    return Response(music,mimetype="audio/mpeg")
    
@register_post('entry')
def addEntry():
    if session.get('name',None):
        uid=User.query(Eq(User.uname,session['name']))[0].uid
    else:
        uid=User.query(Eq(User.uname,u'佚名'))[0].uid
    content=request.form['content']
    title=request.form['title']
    img_cnt=int(request.form['cnt'])
    imgs=[]
    for i in range(img_cnt):
        f=request.files[str(i)]
        fname=str(datetime.now())+'_'+secure_filename(f.filename)
        imgs.append(fname)
        save_file(os.path.join(app.config['IMAGE_FOLRDER'],fname),f)
    return jsonify(status=Entry.insert(uid=uid,econtent=content,etitle=title,eimgs='#'.join((imgs))))
    
@register_post('login')
def login():
    name = request.form['name']
    pwd = request.form['pwd']
    if User.exists( And( Eq(User.uname,name), Eq(User.upwd,pwd) ) ):
        session['logged_in']=True
        session['name']=name
        return jsonify(status=True)
    return jsonify(status=False)

@register_post('logout')
@logged_in_required
def logout():
    session.pop('logged_in',None)
    session.pop('name',None)
    return jsonify(status=True)
    
@register_post('enroll')
def enroll():
    name,pwd=request.form['name'],request.form['pwd']
    avatar=request.files['avatar']
    if not User.exists(Eq(User.uname,name)):
        avatar_filename=str(datetime.now())+'_'+secure_filename(avatar.filename)
        save_file(os.path.join(app.config['IMAGE_FOLRDER'],avatar_filename),avatar)
        return jsonify(status=User.insert(uname=name,upwd=pwd,uavatar=avatar_filename))
    return jsonify(status=False)
