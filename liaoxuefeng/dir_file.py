#!/usr/bin/env python
# coding=utf-8

import os

print("os.name = ", os.name)

#print(os.uname)

print(os.path.abspath('.'))

for x in os.listdir('/home/xupeng/code/python'):
    if os.path.isfile(x):
        print("file: ", x)
    elif os.path.isdir(x):
        print("dir: ", x)
    else:
        print("other: ", x)
