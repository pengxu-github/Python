#! /usr/bin/python

from contextlib import contextmanager

from contextlib import closing
from urllib.request import urlopen


class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s...' % self.name)


@contextmanager
def create_query(name):
    print('Begin')
    qt = Query(name)
    yield qt
    print('End')


if __name__ == '__main__':
    with create_query('Bob') as q:
        q.query()

    # with closing(urlopen('https://www.python.org')) as page:
    #     for line in page:
    #         print(line)
