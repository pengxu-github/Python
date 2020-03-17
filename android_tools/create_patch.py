import argparse
import logging
import os
import os.path
import shutil

from git import Repo

ERROR_GIT_NOT_EXIST = 101
verbose = False
force = False
source = ''
dest = ''
git_user = ''
git_folders = []

diff_repository = {
    'build',
    'frameworks',
    'vendor',
}

diff_repository_info = {
    'build': ('cf0fe8f', '0001-android-build-mk.diff'),
    'frameworks': ('5c49b1fe', '0002-android-frameworks-all.diff'),
    'vendor': ('f37b7ad', '0003-android-vendor-anboxconfig.diff')
}

git_projects = [
    "Freeme/platforms/common/vendor/cmcc",
    "Freeme/platforms/common/apps/FreemeSystemUI",
    "Freeme/platforms/common/apps/FreemeSettings",
    "Freeme/platforms/common/apps/FreemeFileManager",
    "Freeme/platforms/common/apps/FreemeCalculator",
    "Freeme/platforms/common/apps/FreemeVideo",
    "Freeme/platforms/common/apps/FreemeScreenRecorder",
    "Freeme/platforms/common/apps/FreemeSuperShot",
    "Freeme/platforms/common/apps/FreemeSoundRecorder",
    "Freeme/platforms/common/apps/FreemeTTS",
    "Freeme/platforms/common/apps/FreemeMusic",
    "Freeme/platforms/common/apps/FreemeDeskClock",
    "Freeme/platforms/common/apps/FreemeGameMode",
    "Freeme/platforms/common/apps/FreemeOneHand",
    "Freeme/platforms/common/apps/FreemeAppLock",
    "Freeme/platforms/common/apps/FreemeGallery"
]

git_projects_dict = {
    "Freeme/platforms/common/vendor/cmcc": ("vendor/cmcc", "cmcc-7.1.1_publ"),
    "Freeme/platforms/common/apps/FreemeSystemUI":
        ("vendor/cmcc/packages/apps/CmccSystemUI", "cmcc-7.1.1_master-publ"),
    "Freeme/platforms/common/apps/FreemeSettings":
        ("vendor/cmcc/packages/apps/CmccSettings", "cmcc-7.1.1_master-release"),
    "Freeme/platforms/common/apps/FreemeFileManager":
        ("vendor/cmcc/packages/apps/CmccFileManager", "cmcc-7.1.1_publ",),
    "Freeme/platforms/common/apps/FreemeCalculator":
        ("vendor/cmcc/packages/apps/CmccCalculator", "cmcc-7.1.1_publ",),
    "Freeme/platforms/common/apps/FreemeVideo":
        ("vendor/cmcc/packages/apps/CmccVideo", "cmcc-7.1.1_publ",),
    "Freeme/platforms/common/apps/FreemeScreenRecorder":
        ("vendor/cmcc/packages/apps/CmccScreenRecorder", "cmcc-7.1.1_publ"),
    "Freeme/platforms/common/apps/FreemeSuperShot":
        ("vendor/cmcc/packages/apps/CmccSuperShot", "REL/cmcc-7.1.1_dev"),
    "Freeme/platforms/common/apps/FreemeSoundRecorder":
        ("vendor/cmcc/packages/apps/CmccSoundRecorder", "cmcc-7.1.1_publ"),
    "Freeme/platforms/common/apps/FreemeTTS": ("vendor/cmcc/packages/apps/CmccTTS", "REL/cmcc"),
    "Freeme/platforms/common/apps/FreemeMusic":
        ("vendor/cmcc/packages/apps/CmccMusic", "cmcc-7.1.1_publ"),
    "Freeme/platforms/common/apps/FreemeDeskClock":
        ("vendor/cmcc/packages/apps/CmccDeskClock", "cmcc-7.1.1_publ"),
    "Freeme/platforms/common/apps/FreemeGameMode":
        ("vendor/cmcc/packages/apps/CmccGameMode", "cmcc-7.1.1_release"),
    "Freeme/platforms/common/apps/FreemeOneHand":
        ("vendor/cmcc/packages/apps/CmccOneHand", "cmcc-7.1.1_release"),
    "Freeme/platforms/common/apps/FreemeAppLock":
        ("vendor/cmcc/packages/apps/CmccAppLock", "cmcc-7.1.1_release"),
    "Freeme/platforms/common/apps/FreemeGallery":
        ("vendor/cmcc/packages/apps/CmccGallery", "cmcc-release")
}


class GitProjects:
    """
    describe a git repository, contains git repository name, revision,
    and where to clone to.
    """

    def __init__(self, path, git_name, git_revision, user_name):
        """
        Args:
            path: git repository cloned to
            git_name: git repository name
            git_revision: git revision
        """
        self._path = path
        self._git_ssh = 'ssh://'
        self._git_user = user_name
        self._git_ip = '@10.20.40.21:29418/'
        self._git_url_prefix = ''.join([self._git_ssh, self._git_user, self._git_ip])
        self._name = self._git_url_prefix + git_name
        self._revision = git_revision

    def __str__(self):
        return "git url: {}, " \
               "revision: {}, " \
               "clone to: {}".format(self._name, self._revision, self._path)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._path = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

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


def parse_args():
    parser = argparse.ArgumentParser(description='create patch for cmcc branch')
    parser.add_argument('-v', dest='verbose', action='store_true', help='verbose mode')
    parser.add_argument('-f', dest='force', action='store_true',
                        help='force create patch even patch file exist')
    parser.add_argument('-s', '--source', metavar='source path', required=True,
                        dest='source_path', action='store',
                        help='absolute path of repo repository')
    parser.add_argument('-d', '--dest', metavar='dest path', required=True,
                        dest='dest_path', action='store',
                        help='absolute path of repo repository')
    parser.add_argument('-u', '--git_user', metavar='git user name', required=True,
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


def create_patch():
    for git_folder in diff_repository:
        patch_need_create_path = os.path.normpath(os.path.join(os.path.abspath(source), git_folder))
        logging.debug("patch_need_create_path: %s" % patch_need_create_path)
        if not os.path.exists(patch_need_create_path):
            logging.error("%s in %s not exist, please check." % (git_folder, source))
            exit(ERROR_GIT_NOT_EXIST)
        repo = Repo(patch_need_create_path)
        create = True
        if repo.is_dirty():
            create = show_choose("dirty git repository")
        if create:
            commit_last = repo.commit(diff_repository_info[git_folder][0])
            patch_file = os.path.join(dest, git_folder, diff_repository_info[git_folder][1])
            logging.debug("write to patch file: {}".format(patch_file))

            if os.path.exists(patch_file):
                if not force:
                    create = show_choose("override patch file: {}".format(patch_file))
            if create:
                with open(patch_file, 'wt') as f:
                    f.write(repo.git.diff(commit_last.hexsha))
            else:
                logging.info("{} already exist, and user choose not overwrite".format(patch_file))
        else:
            return False
    return True


def check_path():
    """
    create the destination folder of patch
    """
    dest_folds = []
    for git_folder in diff_repository:
        # check dest path, if not exist, create it.
        dest_patch_path = os.path.normpath(os.path.join(os.path.abspath(dest), git_folder))
        logging.debug("dest_patch_path = %s" % dest_patch_path)
        if not os.path.exists(dest_patch_path):
            os.makedirs(dest_patch_path, 0o777, True)
            dest_folds.append(dest_patch_path)
    return dest_folds


def create_diff(source_path, dest_path):
    if os.path.exists(source_path):
        check_path()
        create_success = create_patch()
        if create_success:
            logging.info("create patch success, patch has been saved to %s" % dest_path)
        else:
            logging.error("create patch, please check")


def git_clone(git_pro):
    if not isinstance(git_pro, GitProjects):
        logging.error("%s is not GitProjects class".format(git_pro))
    else:
        logging.debug(git_pro)
        path = git_pro.path
        choose = True
        if os.path.exists(path):
            if not force:
                choose = show_choose("{} is exits".format(path))
            if choose:
                shutil.rmtree(path)
        if choose:
            Repo.clone_from(git_pro.name, path, branch=git_pro.revision,
                            multi_options=['--single-branch'])
        else:
            return False
        return True


def clone_proj(dest_path):
    """
    clone git projects to dest_path
    Args:
        dest_path: path to place git projects
    """
    for proj in git_projects:
        git_list = git_projects_dict[proj]
        dest_folder = os.path.normpath(os.path.join(os.path.abspath(dest_path), git_list[0]))
        logging.debug("{} dest folder: {}, revision: {}".format(proj, dest_folder, git_list[1]))
        git_clone(GitProjects(dest_folder, proj, git_list[1], git_user))


def remove_folder(dest_path, folder_name):
    for root, dirs, files in os.walk(dest_path):
        for dir_n in dirs:
            if dir_n == folder_name:
                logging.debug("remove: {}".format(os.path.join(root, dir_n)))
                shutil.rmtree(os.path.join(root, dir_n))
    return True


def main(source_path, dest_path):
    # create patch file
    create_diff(source_path, dest_path)

    # clone project
    clone_proj(dest_path)

    # remove .git folder
    remove_folder(dest_path, ".git")


if __name__ == '__main__':
    args = parse_args()
    source = args.source_path
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
    logging.debug("create patch for {}, save to {}".format(source, dest))
    logging.debug("git repository: ")
    logging.debug(diff_repository)

    main(source, dest)
