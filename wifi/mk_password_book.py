# coding:utf-8
import datetime
import itertools as its
import string

import os

password_file = "password.txt"


def mk_pas():
    # 迭代器
    digits = string.digits
    alpha = string.ascii_letters
    words = digits + alpha
    print(words)
    # 生成密码本的位数，五位数，repeat=5
    r = its.product(words, repeat=6)
    time = datetime.datetime.now()
    new_file = "password-" + time.strftime('%Y%m%d%H%M%S') + ".txt"
    print(new_file)
    if os.path.exists(password_file):
        os.rename(password_file, new_file)
    print("begin make password book")
    with open(password_file, "wt") as f:
        # i是元组
        for i in r:
            # jion空格链接
            f.write("".join(i))
            f.write("".join("\n"))
            # print(i)
    delta_time = datetime.datetime.now() - time
    print("make password book success, use %sms" % delta_time)


if __name__ == "__main__":
    mk_pas()
