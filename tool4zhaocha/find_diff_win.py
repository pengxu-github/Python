# coding=utf-8
from pprint import pprint

__author__ = 'XuPeng'

__doc__ = '''
pythonwin中win32gui的用法
本文件演如何使用win32gui来遍历系统中所有的顶层窗口，
并遍历所有顶层窗口中的子窗口
'''

import win32gui
import win32process

debug = True
wnd_title = 'TIM图片20181017200431.png - Windows 照片查看器'
wnd_class = 'Photo_Lightweight_Viewer'


def gbk2utf8(s):
    return s.decode('gbk').encode('utf-8')


def show_window_attr(hWnd):
    """
    显示窗口的属性
    :return:
    """
    if not hWnd:
        return

    # 中文系统默认title是gb2312的编码
    title = win32gui.GetWindowText(hWnd)
    # title = gbk2utf8(title)
    clsname = win32gui.GetClassName(hWnd)
    if debug:
        print('-----------------------------')
        print('窗口句柄:%s ' % hWnd)
        print('窗口标题:%s' % title)
        print('窗口类名:%s' % clsname)


def show_windows(hWndList):
    for h in hWndList:
        show_window_attr(h)


'''
def demo_top_windows():
    """
    演示如何列出所有的顶级窗口
    :return:
    """
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    show_windows(hWndList)

    return hWndList
'''


def _MyCallback(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        windows = extra
        temp = []
        temp.append(hex(hwnd))
        temp.append(win32gui.GetClassName(hwnd))
        temp.append(win32gui.GetWindowText(hwnd))
        windows[hwnd] = temp


def get_hwnds():
    windows = {}
    win32gui.EnumWindows(_MyCallback, windows)
    print("Enumerated a total of  windows with %d classes".format(len(windows)))
    if debug:
        print('------------------------------')
        # print classes
        for item in windows:
            print(windows[item])
        print('-------------------------------')
    return windows


def demo_child_windows(parent):
    """
    演示如何列出所有的子窗口
    :return:
    """
    if not parent:
        return

    hWndChildList = []
    win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd), hWndChildList)
    show_windows(hWndChildList)
    return hWndChildList


def get_hwnds1(pid):
    """return a list of window handlers based on it process id"""

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def find_child_window(class_name, title_name):
    # 获取句柄
    hwnd = win32gui.FindWindow(class_name, title_name)
    # 获取窗口左上角和右下角坐标
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    if debug:
        print('find window from class name: %s, title name: %s, result: %d, %d, %d, %d'
              % (class_name, title_name, left, top, right, bottom))
    return left, top, right, bottom


hWndList = get_hwnds()
show_windows(hWndList)

l, t, r, b = find_child_window(wnd_class, wnd_title)
print('left, top, right, bottom: '.format(l, t, r, b))
