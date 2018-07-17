#!/usr/bin/env python
# coding=utf-8
import os

s = 'helloworld'
a = slice(2, 9, 2)
a.indices(len(s))
for i in range(*a.indices(len(s))):
    print(s[i])

t = ('hello', 'you', 'help')
print('id of t: {}'.format(id(t)))
t = t[:1] + tuple('can',) + t[1:]
print('id of t: {}'.format(id(t)))
t1 = tuple('can')
print(t1)
t2 = tuple('can',)
print(t2)
t3 = tuple(['can'])
print(t3)

t4 = tuple(x for x in 'can')
print(t4)

# print(os.get_terminal_size().columns)

