import re
import os
import subprocess

DEBUG = True


def logd(msg, fo=None):
    if DEBUG:
        print(msg.format(fo))


def loge(msg, fo=None):
    print(msg.format(fo))


def run(project_dir, date_from, date_to, search_key, filename):
    bug_dic = {}
    try:
        os.chdir(project_dir)
    except Exception as e:
        raise e
    branches_list = get_branches()
    for branch in branches_list:
        bug_branch_dic = deal_branch(date_from, date_to, branch, search_key)
        for item in bug_branch_dic:
            if item not in bug_dic:
                bug_dic[item] = bug_branch_dic[item]
            else:
                bug_dic[item] += bug_branch_dic[item]
    log_output(filename, bug_dic)


# abstract log of one branch
def deal_branch(date_from, date_to, branch, search_key):
    try:
        os.system('git checkout ' + branch)
        os.system('git pull ')
    except Exception as error:
        print(error)
    cmd_git_log = ["git", "log", "--stat", "--no-merges", "-m", "--after=" + date_from, "--before=" + date_to]
    proc = subprocess.Popen(cmd_git_log, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    bug_branch_dic = deal_lines(date_from, date_to, search_key, stdout)
    return bug_branch_dic


# write commits log to file
def log_output(filename, bug_dic):
    fi = open(filename, 'w')
    for item in bug_dic:
        m1 = '--' * 5 + 'BUG:' + item + '--' * 20 + '\n'
        fi.write(m1)
        for commit in bug_dic[item]:
            fi.write(commit)
    fi.close()


# analyze log
def deal_lines(date_from, date_to, search_key, stdout):
    bug_dic = {}
    for line in stdout.split('commit '):
        if re.search('Bug:? \d+ ', line) is not None and re.search(search_key, line) is not None:
            match = re.search('Bug:? \d+ ', line).group()
            try:
                bug_id = match.split('Bug: ')[1].split('\n')[0]
            except Exception as e:
                bug_id = match.split('Bug ')[1].split(' ')[0]
            if bug_id not in bug_dic:
                bug_dic[bug_id] = [line]
            else:
                bug_dic[bug_id] += [line]
    return bug_dic


# get all branches of a project
def get_branches():
    branch_list = []
    try:
        cmd_git_remote = 'git branch -vva'
        proc = subprocess.Popen(cmd_git_remote.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if isinstance(stdout, bytes):
            raw_branch = bytes.decode(stdout)
        elif isinstance(stdout, type('')):
            raw_branch = stdout
        else:
            loge('stdout is error type: {}', type(stdout))
            return ''
        raw_branch = re.split(r'\n', raw_branch)
        for raw in raw_branch:
            logd('origin raw: {}', raw)
            raw = raw.strip().split(' ')[0].strip()
            logd('modified raw: {}', raw)
            if raw.startswith('remotes'):
                branch = raw.split('/')[2]
                logd('modified raw: {}', branch)
                if not branch == 'HEAD':
                    branch_list.append(branch)
    except Exception as error:
        if branch_list == []:
            loge('Can not get any branch!')
    return branch_list


if __name__ == '__main__':
    # path of the .git project. example: "/home/username/projects/jekyll_vincent"
    project_dir = "D:\source-code\pycharm-workspace"
    date_from = "2018-11-01"
    date_to = "2018-12-01"
    # only search 'Bug: \d+' for default
    search_key = ""
    # name of output file. example:"/home/username/jekyll_0125_0226.log"
    filename = ""
    run(project_dir, date_from, date_to, search_key, filename)
