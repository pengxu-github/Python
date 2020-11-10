import argparse
import logging
import os
import time
import re


def parse_args():
    parser = argparse.ArgumentParser(description='help to ')
    parser.add_argument('-v', dest='verbose', action='store_true', help='verbose mode')
    parser.add_argument('-u', '--unblock_log', metavar='unblocked_screen_on',
                        dest='unblocked_screen_on', action='store',
                        help='log file of Unblocked screen on')
    return parser.parse_args()


def trim_space(s):
    if s.startswith(' ') or s.endswith(' '):
        return re.sub(r"^(\s+)|(\s+)$", "", s)
    return s


def parse_line(line):
    after_index = line.index('after')
    if after_index > 0:
        time_use = trim_space(line[after_index + 5:])
        logging.debug("time use: {}".format(time_use))
        return trim_space(time_use.split(' ')[0])
    else:
        return 0


def parse_unblock_screen_on():
    if os.path.exists(unblocked_file):
        log_file = open(unblocked_file, "r")
        index = -1
        flags = []
        items = []
        time_totals = []
        while 1:
            line = log_file.readline()
            if line:
                if not line.isspace():
                    if line.startswith('#'):
                        flags.append(trim_space(line[1:]))
                        items.append(0)
                        time_totals.append(0)
                        index += 1
                    else:
                        items[index] += 1
                        time_totals[index] += int(parse_line(line))
            else:
                break
        index = 0
        while index < len(flags):
            logging.info("{} average time {}".format(
                flags[index], time_totals[index] / items[index]))
            index += 1
        log_file.close()
    else:
        logging.debug("{} not exist".format(unblocked_file))


if __name__ == '__main__':
    args = parse_args()
    verbose = args.verbose
    unblocked_file = args.unblocked_screen_on
    logging.basicConfig(
        # filename="fingerprint_unlock.log",
        # filemode='a',
        level=logging.INFO,
        # format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        format='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s'
    )
    if verbose:
        logging.getLogger().level = logging.DEBUG

    action = ""
    start_time = time.time()
    if unblocked_file:
        parse_unblock_screen_on()
        action = "parse unblocked screen on"
    else:
        logging.error("no parameter, do nothing")
        exit(-1)
    end_time = time.time()
    logging.info("{} use time {}ms".format(action, end_time - start_time))
