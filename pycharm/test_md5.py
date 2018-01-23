#!/usr/bin/env python
# coding=utf-8

import hmac, hashlib, random

use_normal_md5_check = False
db_reg_nor = {}
db_reg_hmac = {}

def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def hmac_md5(key, s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()

class User(object):
    def __init__(self, username, password):
        self.username = username
        #self.salt = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.salt = ''.join(self.username)
        self.password = password

    def toString(self):
        return ('User(username: %s, password: %s, salt: %s)' % (self.username, self.password, self. salt))

db = {
    'michael' : User('michael', '123456'),
    'bob' : User('bob', 'abc999'),
    'alice' : User('alice', 'alice2008')
}

def register_normal_md5(username, password):
    if username not in db_reg_nor:
        db_reg_nor[username] = User(username, get_md5(password))
    print('register_normal_md5[%s : %s]' % (username, db_reg_nor[username].toString()))
    return db_reg_nor[username]

def register_hmac_md5(username, password):
    if username not in db_reg_hmac:
        db_reg_hmac[username] = User(username, hmac_md5(username, password))
    print('register_hmac_md5[%s : %s]' % (username, db_reg_hmac[username].toString()))
    return db_reg_hmac[username]

def login(username, password):
    #user = db[username]
    result = False
    if use_normal_md5_check:
        user = register_normal_md5(username, password)
        md5_check = user.password == get_md5(password)
        result = md5_check
    else:
        user = register_hmac_md5(username, password)
        hmac_md5_check = user.password == hmac_md5(user.salt, password)
        result = hmac_md5_check
    #print('username: %s, password: %s, salt: %s' % (user.username, user.password, user.salt))
    return result

# 测试:
#login('michael', '123456')
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')


