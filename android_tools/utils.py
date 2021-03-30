import datetime
import logging
import multiprocessing
import os
import shutil
import time


# 模拟点按
def tap(x0, y0):
    cmdTap = 'adb shell input tap {x1} {y1}'.format(x1=x0, y1=y0)
    print(datetime.datetime.now(), cmdTap)
    os.system(cmdTap)


def tap_delay(x0, y0, delay, times):
    """
    tap (x0, y0) ${times} with delay ${delay}s
    """
    while times > 0:
        tap(x0, y0)
        times = times - 1
        print(times, " ", delay)
        time.sleep(delay)


def tap_cycle(x0, y0):
    """
    tap (x0, y0) use 10 process
    """
    for i in range(10):
        p = multiprocessing.Process(target=tap, args=(x0, y0))
        p.start()


# 模拟滑动
def swipe(x0, y0, x1, y1, delay0):
    cmdSwipe = 'adb shell input swipe {x2} {y2} {x3} {y3} {delay1}'.format(
        x2=x0,
        y2=y0,
        x3=x1,
        y3=y1,
        delay1=delay0
    )
    print(cmdSwipe)
    os.system(cmdSwipe)


# 截图并返回图片
def screenshot():
    os.system('adb shell screencap -p /sdcard/sh.png')
    os.system('adb pull /sdcard/sh.png .')
    return "sh.png"


def remove_folder(dest_path, folder_name, file_name):
    for root, dirs, files in os.walk(dest_path):
        for dir_n in dirs:
            if dir_n == folder_name:
                logging.debug("remove: {}".format(os.path.join(root, dir_n)))
                shutil.rmtree(os.path.join(root, dir_n))
        for file in files:
            if file == file_name:
                logging.debug("remove {}".format(os.path.join(root, file)))
                os.remove(os.path.join(root, file))
    return True


def create_path(path: str, force: bool):
    """
    create the destination folder of patch
    """
    if os.path.exists(path):
        if force:
            logging.info("delete {}".format(path))
            shutil.rmtree(path)
    os.makedirs(path, 0o777, True)
    logging.info("path {} created".format(path))
