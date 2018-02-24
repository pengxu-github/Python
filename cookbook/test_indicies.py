#!/usr/bin/env python
# coding=utf-8

s = 'helloworld'
a = slice(2, 9, 2)
a.indices(len(s))
for i in range(*a.indices(len(s))):
    print(s[i])

