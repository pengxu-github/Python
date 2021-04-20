import argparse
import logging
import os
import shutil
import time

from git import Repo

from android_tools.git_project_info import GitProjectInfo
import android_tools.utils

verbose = False
git_revision = "freeme-11.0.0_master"
git_revision_app = "freeme-11.0.0_master-sprd"
statistics_dict = {}
rm_files = ("so", "jar", "jpg", "png", "zip", "gz", "ogg", "bat",
            "db", "lic", "apk", "ttf", "pdf", "mp3", "mp4", "tflite",
            "pk8", "pem", "txt", "remove_me", "dummy", "dummy_files",
            "presets_dummy", "gradlew", "jks")
rm_folders = (".git", "BaiduLocation", "SprdSignApks")
remove_paths = ("vendor/freeme/packages/apps/FreemeOTA/external",)

git_projects_dict = {
    # 11.0
    "Freeme/platforms/common/vendor/freeme":
        ("vendor/freeme", "freeme-11.0.0_master-t610"),
    "Freeme/platforms/android-30/SPRD-R0-CY-T610/platform/device_droi":
        ("vendor/freeme/device/droi", git_revision),
    "Freeme/platforms/common/apps/FreemeAppLock":
        ("vendor/freeme/packages/apps/FreemeAppLock", git_revision),
    "Freeme/platforms/common/apps/FreemeOneHand":
        ("vendor/freeme/packages/apps/FreemeOneHand", git_revision),
    "Freeme/platforms/common/apps/FreemeFileManager":
        ("vendor/freeme/packages/apps/FreemeFileManager", git_revision_app),
    "Freeme/platforms/common/apps/FreemeMusic":
        ("vendor/freeme/packages/apps/FreemeMusic", git_revision),
    "Freeme/platforms/common/apps/FreemeVideo":
        ("vendor/freeme/packages/apps/FreemeVideo", git_revision),
    "Freeme/platforms/common/apps/FreemeHongbaoAssistant":
        ("vendor/freeme/packages/apps/FreemeHongbaoAssistant", git_revision),
    "Freeme/platforms/common/apps/FreemeSuperPowerSaver":
        ("vendor/freeme/packages/apps/FreemeSuperPowerSaver", git_revision_app),
    "Freeme/platforms/common/apps/FreemeSoundRecorder":
        ("vendor/freeme/packages/apps/FreemeSoundRecorder", git_revision),
    "Freeme/platforms/common/apps/FreemeGameMode":
        ("vendor/freeme/packages/apps/FreemeGameMode", git_revision),
    "Freeme/platforms/common/core/soul":
        ("vendor/freeme/external/soul", "android-27"),
    "Freeme/platforms/common/apps/FreemeMultiApp":
        ("vendor/freeme/packages/apps/FreemeMultiApp", "main-R"),
    "Freeme/platforms/common/apps/FreemeAgingTool":
        ("vendor/freeme/packages/apps/FreemeAgingTool", "REL/main-30"),
    # "Freeme/platforms/common/apps/FreemeGallery":
    #     ("vendor/freeme/packages/apps/FreemeGallery", "all-master"),
    # "Freeme/platforms/common/apps/FreemeVAssistant":
    #     ("vendor/freeme/packages/apps/FreemeVAssistant", "all-master"),
    "Freeme/platforms/common/apps/FreemeCalculator":
        ("vendor/freeme/packages/apps/FreemeCalculator", "freeme11"),
    "Freeme/platforms/common/apps/FreemeSuperShot":
        ("vendor/freeme/packages/apps/FreemeSuperShot", "freeme11"),
    "Freeme/platforms/common/apps/FreemeSetupWizard":
        ("vendor/freeme/packages/apps/FreemeSetupWizard", git_revision),
    "Freeme/platforms/common/core/freeme-services":
        ("vendor/freeme/frameworks/base/services/cmcc-services", "android-30"),
    "Freeme/platforms/common/apps/FreemeOTA":
        ("vendor/freeme/packages/apps/FreemeOTA", "develop-30"),
    "Freeme/platforms/common/apps/FreemeManager":
        ("vendor/freeme/packages/apps/FreemeManager", "android-30"),
    "Freeme/platforms/common/apps/FreemeConfigProvider":
        ("vendor/freeme/packages/providers/FreemeConfigProvider", "main"),
    "Freeme/platforms/common/apps/FreemeFaceService":
        ("vendor/freeme/packages/apps/FreemeFaceService", "sensetime"),
    "Freeme/platforms/common/apps/FreemeMultiWindow":
        ("vendor/freeme/packages/apps/FreemeMultiWindow", "main"),
    "Freeme/platforms/common/apps/FreemeYellowPageLite":
        ("vendor/freeme/packages/apps/FreemeYellowPageLite", "REL/main"),
    "Freeme/platforms/common/apps/FreemeMagnification":
        ("vendor/freeme/packages/apps/FreemeMagnification", "REL/freeme11"),
    "Freeme/platforms/common/apps/FreemeMsa":
        ("vendor/freeme/packages/apps/FreemeMsa", "REL/main"),
    # care
    # "Freeme/platforms/common/apps/FreemeHealthAssistant":
    #     ("vendor/freeme/packages/apps/FreemeHealthAssistant", "main"),
    # vmic
    "Freeme/platforms/common/manbox/vmic": ("vendor/freeme/system/vmic", "cmcc_dev"),
    "Freeme/FreemeDEV/products/RemoteOperation":
        ("vendor/freeme/packages/apps/VmicRemoteOperation", "main")
}
"""
git repositories info.

key is repository name;

value is relative path, git revision.
"""


def parse_args():
    parser = argparse.ArgumentParser(description='create patch for cmcc branch')
    parser.add_argument('-v', dest='verbose', action='store_true', help='verbose mode')
    parser.add_argument('-l', dest='list', action='store_true',
                        help='list cloned repository')
    parser.add_argument('-f', dest='force', action='store_true',
                        help='force remove code folder if exist')
    parser.add_argument('-d', '--dest', metavar='dest_path', required=True,
                        dest='dest_path', action='store',
                        help='absolute path of repo repository')
    parser.add_argument('-u', '--git_user', metavar='git_user_name', required=True,
                        dest='git_user', action='store',
                        help='user name of git')
    return parser.parse_args()


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
            # logging.info("git clone: {}".format(git_pro))
            Repo.clone_from(git_pro.url, path, branch=git_pro.revision,
                            multi_options=['--single-branch'])
        return True


def do_clone():
    items = git_projects_dict.items()
    for repository_name, git_info in items:
        dest_folder = os.path.normpath(os.path.join(os.path.abspath(dest), git_info[0]))
        git_project_info = GitProjectInfo(dest_folder, repository_name, git_info[1], git_user)
        if not git_clone(git_project_info):
            logging.error("clone failed")


def deal_others():
    plus_codes = os.path.join(dest, "../plus_codes/")
    for plus in os.listdir(plus_codes):
        dest_path = os.path.join(dest, "vendor/freeme/packages/apps", plus)
        if not os.path.exists(dest_path):
            shutil.copytree(os.path.join(plus_codes, plus), dest_path)

    for remove_path in remove_paths:
        abs_remove_path = os.path.join(dest, remove_path)
        if os.path.exists(abs_remove_path):
            logging.debug("remove {}".format(abs_remove_path))
            shutil.rmtree(abs_remove_path)


def do_statistics():
    logging.debug("do statistics of {}".format(dest))
    for root, dirs, files in os.walk(dest):
        for file in files:
            file_splits = file.split(".")
            file_suffix = file_splits[-1]
            if file_suffix in rm_files:
                os.remove(os.path.join(root, file))
            else:
                abs_file_path = os.path.normpath(os.path.join(root, file))
                count = statistics_dict.get(file_suffix, [0, 0, []])
                count[2].append(abs_file_path)
                statistics_dict[file_suffix] = [count[0] + 1,
                                                count[1] + os.path.getsize(abs_file_path),
                                                count[2]]
        for dir_name in dirs:
            abs_path = os.path.join(root, dir_name)
            if dir_name in rm_folders or not os.listdir(abs_path):
                shutil.rmtree(abs_path)
        if not os.listdir(root):
            logging.debug("remove {}".format(root))
            os.rmdir(root)


if __name__ == '__main__':
    args = parse_args()
    dest = args.dest_path
    verbose = args.verbose
    force = args.force
    git_user = args.git_user
    list_repo = args.list
    logging.basicConfig(
        # filename="create_patch.log",
        # filemode='a',
        level=logging.INFO,
        # format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    )
    if verbose:
        logging.getLogger().level = logging.DEBUG
    if list_repo:
        android_tools.utils.list_repository(git_projects_dict)
        exit(1)

    start_time = time.time()
    android_tools.utils.create_path(dest, force)
    do_clone()
    deal_others()
    collect_time = time.time()
    logging.debug("collect code use {}s".format(collect_time - start_time))
    do_statistics()
    statistics_time = time.time()
    logging.debug("statistic use {}s".format(statistics_time - collect_time))

    total_size = 0
    statistics_file = os.path.normpath(os.path.join(os.path.abspath(dest), "statistics.txt"))
    statistics_fd = open(statistics_file, "w")
    for key in statistics_dict.keys():
        logging.debug("{} file appears {} times, total size {:.2f}kb"
                      .format(key, statistics_dict[key][0], statistics_dict[key][1] / 1024))
        summary = "{} file appears {} times, total size {:.2f}MB:" \
            .format(key, statistics_dict[key][0], statistics_dict[key][1] / 1024)
        total_size += statistics_dict[key][1] / (1024 * 1024)
        statistics_fd.writelines(summary)
        statistics_fd.writelines("\n")
        for appear in statistics_dict[key][2]:
            statistics_fd.write("\t")
            statistics_fd.write(appear)
            statistics_fd.write("\n")
    statistics_fd.close()
    write_time = time.time()
    logging.debug("total_size: {:.2}kb, statistics use {}s"
                  .format(total_size, write_time - statistics_time))
    logging.debug("statistics use {}s".format(write_time - statistics_time))
