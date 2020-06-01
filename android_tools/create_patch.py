import argparse
import logging
import os
import os.path
import shutil
import time

from git import Repo

verbose = False
force = False
dest = ''
dest_source = ''
"""
source code path for create diff patch
"""

dest_out = ''
"""
destination path for final patch
"""

default_git_revision = 'cmcc_dev'
release_git_revision = 'REL/cmcc_dev'

git_user = ''

git_projects_dict_test = {
    "Freeme/platforms/android-25/anbox/platform/external":
        ("external", default_git_revision, 'f8d3006c2c', '0006_android_external_sccontrol.diff'),
    "Freeme/platforms/android-25/anbox/platform/vendor/anbox":
        ('vendor/anbox', default_git_revision, 'db06c81', '0005_android_vendor_anbox_config.diff'),
    "Freeme/platforms/common/apps/FreemeContacts":
        ("vendor/cmcc/packages/apps/CmccContacts", release_git_revision)
}

git_projects_dict = {
    # repositories for diff
    "Freeme/platforms/android-25/anbox/platform/build":
        ('build', default_git_revision, 'b617dfd', '0001_android_build_mk.diff'),
    "Freeme/platforms/android-25/anbox/platform/external":
        ("external", default_git_revision, 'f8d3006c2c', '0006_android_external_sccontrol.diff'),
    "Freeme/platforms/android-25/anbox/platform/frameworks":
        ('frameworks', default_git_revision, 'daedb26', '0002_android_frameworks_all.diff'),
    "Freeme/platforms/android-25/anbox/platform/libcore":
        ('libcore', default_git_revision, 'b7ff0ee', '0003_android_libcore_cpu_adjust.diff'),
    "Freeme/platforms/android-25/anbox/platform/packages":
        ('packages', default_git_revision, '8da9f03', '0004_android_packages_all.diff'),
    "Freeme/platforms/android-25/anbox/platform/system":
        ('system', default_git_revision, 'a4947e5', '0005_android_system_all.diff'),
    # "Freeme/platforms/android-25/anbox/platform/vendor/anbox":
    #     ('vendor/anbox', default_git_revision, 'db06c81', '0005_android_vendor_anbox_config.diff'),

    # repositories for clone
    "Freeme/platforms/android-25/anbox/platform/vendor/cmcc": ("vendor/cmcc", default_git_revision),
    "Freeme/platforms/common/apps/FreemeSettings":
        ("vendor/cmcc/packages/apps/CmccSettings", release_git_revision),
    "Freeme/platforms/common/apps/FreemeSystemUI":
        ("vendor/cmcc/packages/apps/CmccSystemUI", release_git_revision),
    "Freeme/platforms/common/apps/FreemeFileManager":
        ("vendor/cmcc/packages/apps/CmccFileManager", release_git_revision),
    "Freeme/platforms/common/apps/FreemeCalculator":
        ("vendor/cmcc/packages/apps/CmccCalculator", release_git_revision),
    "Freeme/platforms/common/apps/FreemeVideo":
        ("vendor/cmcc/packages/apps/CmccVideo", release_git_revision),
    "Freeme/platforms/common/apps/FreemeScreenRecorder":
        ("vendor/cmcc/packages/apps/CmccScreenRecorder", release_git_revision),
    "Freeme/platforms/common/apps/FreemeSoundRecorder":
        ("vendor/cmcc/packages/apps/CmccSoundRecorder", release_git_revision),
    "Freeme/platforms/common/apps/FreemeMusic":
        ("vendor/cmcc/packages/apps/CmccMusic", release_git_revision),
    "Freeme/platforms/common/apps/FreemeDeskClock":
        ("vendor/cmcc/packages/apps/CmccDeskClock", release_git_revision),
    "Freeme/platforms/common/apps/FreemeSetupWizard":
        ("vendor/cmcc/packages/apps/CmccSetupWizard", release_git_revision),
    "Freeme/platforms/common/apps/FreemeWallpaperPicker":
        ("vendor/cmcc/packages/apps/CmccWallpaperPicker", release_git_revision),
    "Freeme/platforms/common/apps/FreemeContacts":
        ("vendor/cmcc/packages/apps/CmccContacts", release_git_revision),
    "Freeme/platforms/common/apps/FreemeMessaging":
        ("vendor/cmcc/packages/apps/CmccMessaging", release_git_revision),
    "Freeme/platforms/common/apps/FreemeDialer":
        ("vendor/cmcc/packages/apps/CmccDialer", release_git_revision),
    "Freeme/platforms/common/apps/FreemeGameMode":
        ("vendor/cmcc/packages/apps/CmccGameMode", release_git_revision),
    "Freeme/platforms/common/apps/FreemeAppLock":
        ("vendor/cmcc/packages/apps/CmccAppLock", release_git_revision),
    "Freeme/platforms/common/apps/FreemeOneHand":
        ("vendor/cmcc/packages/apps/CmccOneHand", release_git_revision),
    "Freeme/platforms/common/apps/FreemeYellowPageLite":
        ("vendor/cmcc/packages/apps/CmccYellowPageLite", release_git_revision),
    "Freeme/platforms/common/apps/FreemeGallery":
        ("vendor/cmcc/packages/apps/CmccGallery", "cmcc-release"),
    "Freeme/platforms/common/apps/FreemeMultiApp":
        ("vendor/cmcc/packages/apps/CmccMultiApp", release_git_revision),
    "Freeme/platforms/common/apps/FreemeTTS":
        ("vendor/cmcc/packages/apps/CmccTTS", release_git_revision),
    "Freeme/platforms/common/apps/FreemeSuperShot":
        ("vendor/cmcc/packages/apps/CmccSuperShot", release_git_revision),
    "Freeme/platforms/common/apps/FreemeLogger":
        ("vendor/cmcc/packages/apps/CmccLogger", release_git_revision),
    "Freeme/platforms/common/apps/FreemeVAssistant":
        ("vendor/cmcc/packages/apps/CmccVAssistant", "REL/main_cmcc"),
    "Freeme/platforms/common/3rd-apps/cmcc":
        ("vendor/cmcc/packages/3rd-apps", "release"),
    "FreemeLite/products/FreemeLite/apps":
        ("vendor/cmcc/packages/apps/freemelite", "cn_standard_cloud"),
    "Freeme/platforms/common/core/freeme-services":
        ("vendor/cmcc/frameworks/base/services/cmcc-services", "REL/cmcc")
}
"""
git repositories info.

key is repository name;

value is relative path, git revision, if repository for diff, 
commit id to diff and diff patch file name define.
"""


class GitProjectInfo:
    """
    describe a git repository, contains git repository name, revision,
    and where to clone to.

    diff id name diff file name requires if for diff patch.
    """

    def __init__(self, path, git_name, git_revision, user_name, diff_id=None, diff_name=None):
        """
        Args:
            path: git repository cloned to
            git_name: git repository name
            git_revision: git revision
            diff_id: create diff with this id
            diff_name: create diff patch with this name
        """
        self._path = path
        self._git_ssh = 'ssh://'
        self._git_user = user_name
        self._git_ip = '@10.20.40.21:29418/'
        self._git_url_prefix = ''.join([self._git_ssh, self._git_user, self._git_ip])
        self._url = self._git_url_prefix + git_name
        self._revision = git_revision
        self._diff_id = diff_id
        self._diff_name = diff_name

    def __str__(self):
        return "git clone {}, " \
               "to {}, " \
               "with revision {}, " \
               "diff id {}, " \
               "diff file name {}." \
            .format(self._url, self._path, self._revision, self._diff_id, self._diff_name)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._path = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._url = value

    @property
    def revision(self):
        return self._revision

    @revision.setter
    def revision(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._revision = value

    @property
    def user_name(self):
        return self._git_user

    @user_name.setter
    def user_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._git_user = value

    @property
    def diff_id(self):
        return self._diff_id

    @diff_id.setter
    def diff_id(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._diff_id = value

    @property
    def diff_name(self):
        return self._diff_name

    @diff_name.setter
    def diff_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._diff_name = value


def parse_args():
    parser = argparse.ArgumentParser(description='create patch for cmcc branch')
    parser.add_argument('-v', dest='verbose', action='store_true', help='verbose mode')
    parser.add_argument('-f', dest='force', action='store_true',
                        help='force create patch even patch file exist')
    # parser.add_argument('-s', '--source', metavar='source_path', required=True,
    #                     dest='source_path', action='store',
    #                     help='absolute path of repo repository')
    parser.add_argument('-d', '--dest', metavar='dest_path', required=True,
                        dest='dest_path', action='store',
                        help='absolute path of repo repository')
    parser.add_argument('-u', '--git_user', metavar='git_user_name', required=True,
                        dest='git_user', action='store',
                        help='absolute path of repo repository')
    return parser.parse_args()


def show_choose(notice):
    """
    show message for user to choose continue or exits

    Args:
        notice: message to show

    Returns:
        True if user input y or Y, else False
    """
    if isinstance(notice, str):
        logging.info(notice)
        choose = input("\nplease check, \"y or Y\" to ignore and continue, others to exit: ")
        if choose == "y" or choose == "Y":
            return True
        else:
            return False
    else:
        logging.error("please input path, it is string")
        return False


def create_diff(git_pro):
    if not isinstance(git_pro, GitProjectInfo):
        logging.error("%s is not GitProjects class".format(git_pro))
    else:
        logging.debug("create diff, git project: {}".format(git_pro))
        path = git_pro.path
        repo = Repo(path)
        commit_last = repo.commit(git_pro.diff_id)
        patch_file = git_pro.diff_name
        logging.info("write diff to patch file: {}".format(patch_file))
        with open(patch_file, 'wt') as f:
            f.write(repo.git.diff(commit_last.hexsha, '--binary'))
            f.write("\n\n")


def git_clone(git_pro):
    """
    clone git projects
    Args:
        git_pro: git repository info
    """
    if not isinstance(git_pro, GitProjectInfo):
        logging.error("%s is not GitProjects class".format(git_pro))
        return False
    else:
        path = git_pro.path
        # if not verbose, the patch folder have been deleted when check_path()
        if verbose and os.path.exists(path):
            logging.debug("debug mode, and git repository exists, no clone")
        else:
            logging.info("git clone: {}".format(git_pro))
            Repo.clone_from(git_pro.url, path, branch=git_pro.revision,
                            multi_options=['--single-branch'])
        return True


def remove_folder(dest_path, folder_name):
    for root, dirs, files in os.walk(dest_path):
        for dir_n in dirs:
            if dir_n == folder_name:
                logging.debug("remove: {}".format(os.path.join(root, dir_n)))
                shutil.rmtree(os.path.join(root, dir_n))
    return True


def create_patch():
    items = git_projects_dict.items()
    if verbose:
        items = git_projects_dict_test.items()
    for repository_name, git_info in items:
        dest_folder = os.path.normpath(os.path.join(os.path.abspath(dest_out), git_info[0]))
        if len(git_info) > 2:
            # if git_info length > 2, this repository need create diff patch.
            source_folder = os.path.normpath(os.path.join(os.path.abspath(dest_source), git_info[0]))
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder, 0o777, True)
            diff_file = os.path.normpath(os.path.join(os.path.abspath(dest_folder), git_info[3]))
            git_project_info = GitProjectInfo(source_folder, repository_name, git_info[1], git_user,
                                              git_info[2], diff_file)
            if git_clone(git_project_info):
                create_diff(git_project_info)
            else:
                logging.error("clone {} failed".format(repository_name))
        else:
            git_project_info = GitProjectInfo(dest_folder, repository_name, git_info[1], git_user)
            if not git_clone(git_project_info):
                logging.error("clone failed")


def check_path():
    """
    create the destination folder of patch
    """
    global dest_source, dest_out
    dest_source = os.path.normpath(os.path.join(os.path.abspath(dest), "source"))
    dest_out = os.path.normpath(os.path.join(os.path.abspath(dest), "out"))
    if os.path.exists(dest):
        if not verbose:
            if force or show_choose("override patch folder {}?".format(dest)):
                logging.info("delete {}".format(dest))
                shutil.rmtree(dest)
        else:
            logging.debug("just test, do not delete folder")
    os.makedirs(dest_source, 0o777, True)
    os.makedirs(dest_out, 0o777, True)
    logging.info("create patch to {}".format(dest_out))


def main():
    # check destination path
    check_path()

    create_patch()

    # remove .git folder
    remove_folder(dest_out, ".git")


if __name__ == '__main__':
    args = parse_args()
    dest = args.dest_path
    verbose = args.verbose
    force = args.force
    git_user = args.git_user
    logging.basicConfig(
        # filename="create_patch.log",
        # filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    )
    if verbose:
        logging.getLogger().level = logging.DEBUG

    start_time = time.time()
    main()
    end_time = time.time()
    logging.info("create patch use time {}ms".format(end_time - start_time))
