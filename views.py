#-*-coding:utf-8-*-

import os
from werkzeug import secure_filename
from flask import request,session,g,redirect,url_for,abort,render_template,flash,Response
from puppy import app

@app.route('/image/<file_name>')
def getImage(file_name):
    try:
        file=open('images/{}'.format(file_name))
        return Response(file,mimetype='image/jpeg')
    finally:
        pass

@app.route('/')
def index():
    cur=g.db.execute('select id,title,text,images from entries order by id desc')
    entries=[dict(id=row[0],title=row[1],text=row[2],images=row[3]) for row in cur.fetchall()]
    return render_template('index.html',entries=entries)
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    file=request.files['images']
    file_name=''
    if file:
        file_name=secure_filename(file.filename)
        file.save(os.path.join(app.config['IMAGE_FOLRDER'],file_name))
    g.db.execute('insert into entries (title,text,images) values (?,?,?)',
                 [request.form['title'],request.form['text'],file_name])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/del', methods=['POST'])
def del_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('delete from entries where id = (?)',(request.form['id'],))
    g.db.commit()
    flash('entry was deleted successfully')
    return redirect(url_for('index'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Welcome Home')
            return render_template('admin.html')
    if request.method== 'GET':
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))
