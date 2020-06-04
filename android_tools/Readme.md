## 云手机代码 patch 生成脚本
[TOC]

自动生成 patch 的脚本基于 python3 实现，主要用到了 gitpython 库，使用之前需要将对应的库 install。`pip3 install gitpython`，如果出现库找不到的错误，使用 pip3 安装一下即可。

## 执行

```shell
python3 create_patch.py -f -d /mnt/freemeos-code/robox-cmcc/patch-test/ -u xupeng
```

各个参数的含义可以查看 help `python3 create_patch.py -h`

```
usage: create_patch.py [-h] [-v] [-l] [-f] -d dest_path -u git_user_name

create patch for cmcc branch

optional arguments:
  -h, --help            show this help message and exit
  -v                    verbose mode
  -l                    list patched repository
  -f                    force create patch even patch file exist
  -d dest_path, --dest dest_path
                        absolute path of repo repository
  -u git_user_name, --git_user git_user_name
                        absolute path of repo repository
```

在执行脚本前需要检查需要制作 patch 的仓库是否有变动，如果有的话需要同步修改脚本。

```python
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
```

## 脚本逻辑
脚本的主逻辑函数如下：

```pyhton
def main():
    # check destination path
    check_path()

    create_patch()

    # remove .git folder
    remove_folder(dest_out, ".git", '.gitignore')
```

可以看到，脚本分为三个部分，

- 根据输入的参数检查路径
- 生成脚本
    - 生成 xxx.diff
    - clone 仓库
- 删除 .git 和 .gitignore

这里主要介绍一下生成脚本的方案，代码如下：

```python
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
```

方案思路是通过识别 `git_projects_dict` 的 value 值的长度，需要 clone 的仓库只需要路径和分支两个参数，而需要制作 diff 的仓库需要额外初始节点和 patch 名字两个参数。两者结构如下所示：

```
diff:  repository_name: (patch, branch, origin_commit, patch_name)
clone: repository_name: (patch, branch）
```

diff 采用的方法：`git diff f8d3006c2c --binary > xxx.diff`
