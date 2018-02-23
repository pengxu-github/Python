import re

import os
import requests

domain = 'http://www.sjtxt.la'
debug = False


def get_novel_sort_list():
    response = requests.get('http://www.sjtxt.la/soft/1/Soft_001_1.html')
    result = response.text
    reg = r'<a href="([^=]*?)"><img src=".*?">(.*?)</a?'
    novel_url_list = re.findall(reg, result)
    if debug:
        print('get_novel_sort_list, {}'.format(novel_url_list))
        print('list number: %d' % len(novel_url_list))
    return novel_url_list


def get_novel_content(url):
    url = '{}{}'.format(domain, url)
    if debug:
        print('get_novel_content, url = {}'.format(url))
    response = requests.get(url)
    response.encoding = 'urf-8'
    result = response.text
    reg = r'''<a class="downButton" href='(.*?)' title'''
    chapter_url_content = re.findall(reg, result)
    if debug:
        print('get_novel_content, chapter_url_content = {}'.format(chapter_url_content[0]))
    return chapter_url_content[0]


def get_chapter_list(url):
    url = '{}{}'.format(domain, url)
    if debug:
        print(url)
    response = requests.get(url)
    response.encoding = 'utf-8'
    result = response.text
    reg = r'<li><a href="(.*?\.html)">(.*?)</a></li>'
    chapter_url_list = re.findall(reg, result)
    # print('get_chapter_list, {}'.format(chapter_url_list))
    return chapter_url_list


def get_chapter_content(url):
    url = '{}{}'.format(domain, url)
    if debug:
        print('get_chapter_content, url = {}'.format(url))
    response = requests.get(url)
    response.encoding = 'utf-8'
    result = response.text
    reg = r'id="content1">(.*?)<script type="text/javascript">read_bot'
    chapter_content = re.findall(reg, result, re.S)[0]
    return chapter_content


for novel_url, novel_name in get_novel_sort_list():
    # print(novel_name, novel_url)
    path = os.path.join('novel', novel_name)
    if not os.path.exists(path):
        os.mkdir(path)
        print('mkdir success ---- {}'.format(novel_name))
    else:
        print('{} ---- dir exist, pass'.format(novel_name))
    chapter_url_cont = get_novel_content(novel_url)
    if debug:
        print('chapter_url_content = {}'.format(chapter_url_cont))
    for chapter_url, chapter_name in get_chapter_list(chapter_url_cont):
        # print('{}, {}'.format(chapter_url, chapter_name))
        chapter_content = get_chapter_content(chapter_url_cont + chapter_url)
        tmppath = os.path.join(path, chapter_name + '.html')
        if debug:
            print('tmppath = {}'.format(tmppath))
        if not os.path.exists(tmppath):
            with open(tmppath, 'w') as fn:
                fn.write(chapter_content)
                print('{} -----save success'.format(chapter_name))
        else:
            print('{} ---- exist, pass'.format(tmppath))
        break
    break
