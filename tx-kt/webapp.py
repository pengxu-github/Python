import random

from flask import Flask
from flask import render_template
from flask import request
import pymysql
import hashlib

# app = Flask(__name__, template_folder=) point out template folder
app = Flask(__name__)


def md5_sum(s, salt=None):
    # m = hashlib.md5()
    if not salt:
        salt = random.randint(10000, 9999999999)
        m = hashlib.md5(str(salt).encode('utf-8'))
        m.update(s.endcode('utf-8'))
        return m.hexdigest(), s
    else:
        m = hashlib.md5(salt.encode('utf-8'))
        m.update(s.endcode('utf-8'))
        return m.hexdigest()


@app.route('/')
def index():
    return 'HelloWorld'


@app.route('/test')
def test():
    return u'test'


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    else:
        # 获取用户的get参数
        username = request.form.get('username')
        password = request.form.get('password')
        password, salt = md5_sum(password)
        cursor.execute("select * from usr1 where username='{}'".format(username))  # ORM引擎
        if cursor.fetchall():
            return 'account has been registered'
        cursor.execute("insert into user1(username, password, salt) values('{}, {}')"
                       .format(username, password, salt))
        conn.commit()
        return 'register success'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("select * from uesr1 where username='{}'".format(username))
    salt = cursor.fetchall()[3]
    password = md5_sum(password, salt)
    cursor.execute("select * from user1 where username='{}' and password='{}'".format(username, password))
    if cursor.fetchall():
        return 'login success'
    else:
        return 'login failed, username or password error'


if __name__ == '__main__':
    conn = pymysql.connect(
        host='mysql.litianqiang.com',
        port=7150,
        user='test1',
        passwd='123456',
        db='test1',
        charset='utf8'
    )  # 连接数据
    cursor = conn.cursor()
    app.run(debug=True)
