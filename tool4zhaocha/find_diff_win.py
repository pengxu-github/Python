# coding=utf-8
import time

import numpy
import win32gui
import matplotlib.pyplot as plt
from PIL import ImageGrab, ImageChops

from tool4zhaocha.mouse_position import start_get_mouse_click_pos, get_grab_pos

__author__ = 'XuPeng'

__doc__ = '''
pythonwin中win32gui的用法
本文件演如何使用win32gui来遍历系统中所有的顶层窗口，
并遍历所有顶层窗口中的子窗口
'''

debug = True
wnd_title = 'TIM图片20181017200431.png - Windows 照片查看器'
wnd_class = 'Photo_Lightweight_Viewer'
img_left_bound = 640
img_top_bound = 275
img_right_bound = 1280
img_bottom_bound = 685

limg_right_bound = 310
rimg_left_bound = 330


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


def find_child_window(class_name, title_name):
    # 获取句柄
    hwnd = win32gui.FindWindow(class_name, title_name)
    # 获取窗口左上角和右下角坐标
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    if debug:
        print('find window from class name: %s, title name: %s, result: %d, %d, %d, %d'
              % (class_name, title_name, left, top, right, bottom))
    return hwnd, left, top, right, bottom


def compare(image_a, image_b):
    """
    返回两图的差异值
    返回两图红绿蓝差值万分比之和
    """
    histogram_a = image_a.histogram()
    histogram_b = image_b.histogram()
    if len(histogram_a) != 768 or len(histogram_b) != 768: return None
    red_a = 0
    red_b = 0
    for i in range(0, 256):
        red_a += histogram_a[i + 0] * i
        red_b += histogram_b[i + 0] * i
    diff_red = 0
    if red_a + red_b > 0:
        diff_red = abs(red_a - red_b) * 10000 / max(red_a, red_b)

    green_a = 0
    green_b = 0
    for i in range(0, 256):
        green_a += histogram_a[i + 256] * i
        green_b += histogram_b[i + 256] * i
    diff_green = 0
    if green_a + green_b > 0:
        diff_green = abs(green_a - green_b) * 10000 / max(green_a, green_b)

    blue_a = 0
    blue_b = 0
    for i in range(0, 256):
        blue_a += histogram_a[i + 512] * i
        blue_b += histogram_b[i + 512] * i
    diff_blue = 0
    if blue_a + blue_b > 0:
        diff_blue = abs(blue_a - blue_b) * 10000 / max(blue_a, blue_b)
    return diff_red, diff_green, diff_blue


def find_diff(left_l=img_left_bound, left_t=img_top_bound, right_r=img_right_bound,
              right_b=img_bottom_bound, left_width=limg_right_bound, right_l=rimg_left_bound):
    """
    :param left_l: left of left picture, in the window
    :param left_t: top of left picture, in the window
    :param right_r: right of right picture, in the window
    :param right_b: bottom of right picture, in the window
    :param left_width: width of left picture
    :param right_l: begin of right picture, in the picture grabbed
    :return: NULL
    """
    hWndList = get_hwnds()
    show_windows(hWndList)

    wnd_id, l, t, r, b = find_child_window(wnd_class, wnd_title)
    print('windows id, left, top, right, bottom: %d, %d, %d, %d, %d' % (wnd_id, l, t, r, b))
    # full windows display
    # win32gui.ShowWindow(wnd_id, win32con.SW_MAXIMIZE)
    # bring window to foreground
    win32gui.SetForegroundWindow(wnd_id)

    time.sleep(3)
    src_image = ImageGrab.grab((left_l, left_t, right_r, right_b))
    # do not use src_image.show() here,
    # because show this picture will influence left img and right img cut
    width, height = src_image.size
    # cut left img and right img
    left_box = (0, 1, left_width, height)
    right_box = (right_l, 0, width, height)
    image_left = src_image.crop(left_box)
    image_right = src_image.crop(right_box)
    # image_left.show()
    # image_right.show()

    plt.figure(num='image diff', figsize=(10, 7))
    plt.suptitle('image diff')
    plt.subplot(1, 3, 1), plt.title('image_left')
    plt.imshow(image_left)

    plt.subplot(1, 3, 2), plt.title('image_right')
    plt.imshow(image_right)

    diff = ImageChops.difference(image_left, image_right)
    img_diff = numpy.array(diff)
    plt.subplot(1, 3, 3), plt.title('image_diff')
    plt.imshow(img_diff)
    plt.show()


def start_grab():
    print("please click upper left corner of the left diff picture")
    start_get_mouse_click_pos()
    left_l, left_t, left_r, left_b = get_grab_pos()
    print("l, t, r, b: %d, %d, %d, %d" % (left_l, left_t, left_r, left_b))
    print("please click upper left corner of the right diff picture")
    start_get_mouse_click_pos()
    right_l, right_t, right_r, right_b = get_grab_pos()

    find_diff(left_l, left_t, right_r, right_b, left_r - left_l, right_l - left_r)


if __name__ == "__main__":
    start_grab()
