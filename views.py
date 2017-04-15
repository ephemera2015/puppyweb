#-*-coding:utf-8-*-

from flask import request,session,g,redirect,url_for,abort,render_template,flash#request表示当前用户发来的请求
from puppy import app

@app.route('/')#注册应该函数index，对'/'请求进行响应，下同,'/'表示的是网站主页
def index():
    cur=g.db.execute('select id,title,text from entries order by id desc')#从数据库获取发布的所有entry，sql语法
    entries=[dict(id=row[0],title=row[1],text=row[2]) for row in cur.fetchall()]
    return render_template('index.html',entries=entries)#返回应该html文件，这个html文件是index.html模板根据entries填充得到的。
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
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
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
