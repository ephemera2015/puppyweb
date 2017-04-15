#-*-coding:utf-8-*-
import os
from flask import Flask,g#Flask是应用程序类，是flask中最重要的类,g是全局对象，相当于c语言里的全局变量，可以在里面存储全局信息
from db import *

app=Flask(__name__)
app.config.from_pyfile('config.py')#从config.py读取本应用的配置。

@app.before_request#装饰器语法，before_request是说在每次响应请求之前，执行get_db函数，即连接到数据库
def get_db():
    g.db=connect_db(app.config['DATABASE'])#这里的app.config是上面的app.config.from_pyfile生成的
    
@app.teardown_request#同上，这里是说在每次结束应该请求的响应后，关闭数据库连接
def free_db(exception):
    g.db.close()
    
from views import *#在这里导入view.py中的所有函数，根据python解释器的特点，当一个模块被导入时，会执行那个模块里所有可以执行的语句。例如@app.route('/') def index(): ，根据装饰器语法，它相当于index=app.route('/')(index)。因此完成了index函数的注册，详见pdf


if __name__=='__main__':
    app.run()

