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


def list_repository(git_projects_dict):
    diff_repos = []
    clone_repos = []
    items = git_projects_dict.items()
    for repository_name, git_info in items:
        if len(git_info) > 2:
            diff_repos.append(repository_name)
        else:
            clone_repos.append(repository_name)
    logging.info("diff repositories:")
    for diff in diff_repos:
        logging.info("    {}".format(diff))
    logging.info("clone repositories:")
    for clone in clone_repos:
        logging.info("    {}".format(clone))


def do_statistics(dest: str, rm_files: tuple, rm_folders: tuple, rm_relative_paths: tuple):
    """
    do statistics for the folder dest, remove files in rm_files,
    and folders in rm_folders

    Args:
        dest: target folder for statistics
        rm_files: files tuple to remove
        rm_folders: folders tuple to remove
        rm_relative_paths: relative path of dest to remove

    Returns:a dict with the file extension as key, and a list contains file count,
            file total size, and files path list as value

    """
    for remove_path in rm_relative_paths:
        abs_remove_path = os.path.join(dest, remove_path)
        if os.path.exists(abs_remove_path):
            logging.debug("remove requested folder {}".format(abs_remove_path))
            shutil.rmtree(abs_remove_path)

    statistics_dict = {}
    logging.debug("do statistics for {}".format(dest))
    for root, dirs, files in os.walk(dest):
        for dir_name in dirs:
            abs_path = os.path.join(root, dir_name)
            if dir_name in rm_folders or not os.listdir(abs_path):
                shutil.rmtree(abs_path)
        for file in files:
            file_splits = file.split(".")
            file_suffix = file_splits[-1]
            if len(file_splits) == 1 or file_suffix in rm_files:
                os.remove(os.path.join(root, file))
            else:
                abs_file_path = os.path.normpath(os.path.join(root, file))
                count = statistics_dict.get(file_suffix, [0, 0, []])
                count[2].append(abs_file_path)
                statistics_dict[file_suffix] = [count[0] + 1,
                                                count[1] + os.path.getsize(abs_file_path),
                                                count[2]]
        if not os.listdir(root):
            logging.debug("remove empty folder {}".format(root))
            os.rmdir(root)

    return statistics_dict
