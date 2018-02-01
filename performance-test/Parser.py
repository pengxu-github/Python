#!/usr/bin/env python

from Logcat import Logout

DEBUG = True


class Parser:
    '''Parse the command result'''

    def __init__(self, app, data_List, status):
        self.data_List = data_List
        self.status = status
        self.app = app
        self.thisTime = "0"
        self.totalTime = "0"
        self.waitTime = "0"
        Logout.show_message('Parser init data_list: ' + self.data_List)

    def pre_parse(self):
        Logout.show_message('----------------pre_parese---------------------')
        output_str = ''.join(self.data_List)
        if output_str.find("Error:") != -1:
            Logout.show_message("execute command Error: " + self.data_List)
            Logout.log_error(self.app + '_' + Logout.ERROR_FILE, ''.join(self.data_List))
            Logout.log_error(self.app + '_' + Logout.ERROR_FILE, '---------------------------')
            return -1
        elif self.status == 0:
            self.data_List = self.data_List.replace(" ", "")
            self.data_List = self.data_List.strip('\n\n')
            self.data_List = self.data_List.splitlines()
        Logout.show_message(self.data_List)
        return 0

    def parse(self):
        if DEBUG:
            Logout.show_message('start parse command result...')
        try:
            for i in range(len(self.data_List)):
                item = self.data_List[i]
                if DEBUG:
                    Logout.show_message("parse output item : " + item)

                if item.find('ThisTime') != -1:
                    itemTime = item.split(':')
                    self.thisTime = str(itemTime[1])
                    Logout.show_message('parse thisTime = ' + self.thisTime)
                    continue
                elif item.find('TotalTime') != -1:
                    itemTime = item.split(':')
                    self.totalTime = str(itemTime[1])
                    Logout.show_message('parse totalTime = ' + self.totalTime)
                    continue
                elif item.find('WaitTime') != -1:
                    itemTime = item.split(':')
                    self.waitTime = str(itemTime[1])
                    Logout.show_message('parse waitTime = ' + self.waitTime)
                    continue
        except:
            Logout.show_message("Exception in get_item_time")
            print(sys.exc_info()[0], sys.exc_info()[1])

    def getParseResult(self):
        return (self.thisTime, self.totalTime, self.waitTime)

    def __del__(self):
        Logout.show_message("pase output finished...")
