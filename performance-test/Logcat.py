#!/usr/bin/env python

import os
import sys

DEBUG = False


class Logout:
    '''Logout'''
    FILE_NAME = 'calc_time.xls'
    ERROR_FILE = 'error_log.txt'
    OUTPUT_FILE = 'calc_time.txt'

    @staticmethod
    def show_message(msg):
        print(msg)

    @staticmethod
    def delete_file(file_name):
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
                return 0
            else:
                return 0
        except:
            Logout.show_message('delete file failed: ' + file_name)

        return -1

    @staticmethod
    def log_info(out_file, msg):
        if DEBUG:
            Logout.show_message('saving cache in ' + out_file + '...')
        file = open(out_file, 'a')
        try:
            file.write(msg + '\n')
        finally:
            file.close()

    @staticmethod
    def log_error(msg):
        Logout.log_info(Logout.ERROR_FILE, msg)

    @staticmethod
    def log_error(file, msg):
        Logout.log_info(file, msg)

    @staticmethod
    def log_temp(msg):
        Logout.log_info(Logout.OUTPUT_FILE, msg)

    @staticmethod
    def log_temp(file, msg):
        Logout.log_info(file, msg)

    @staticmethod
    def clearn_logout(app_item):
        '''
            清理缓存文件
        '''
        result = 0
        status = Logout.delete_file(app_item[0] + '_' + Logout.OUTPUT_FILE)
        if status != 0:
            result = -1

        status = Logout.delete_file(app_item[0] + '_' + Logout.ERROR_FILE)
        if status != 0:
            result = -1

        return result


if __name__ == "__main__":
    Logout.show_message('I am Logout module!!!')
    Logout.show_message(dir(Logout))
