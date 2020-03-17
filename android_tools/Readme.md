## 云手机代码 patch 生成脚本

## 脚本逻辑

自动生成 patch 的脚本基于 python3 实现，主要用到了 gitpython 库，使用之前需要将对应的库 install。`pip3 install gitpython`，如果出现库找不到的错误，使用 pip3 安装一下即可。

脚本分为两个部分，一是需要生成 xxx.diff 的仓库，另一个是直接整个目录 clone 即可的仓库。

### 生成 xxx.diff

- 根据 -g 参数传入的仓库名字以及 -s 传入的 source path，使用 ` git diff` 命令生成。因此在使用此脚本之前需要本地下载好源码仓库，比如  `android-25/ROBOX/cmcc-7.1.1_dev.xml` 源码。
- 如果有新的仓库需要生成 diff patch，那么需要在脚本中增加已经定义的目录的

```python
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
```



### 整个仓库 clone

- 需要整个仓库 clone 的仓库已经定义在脚本中，如果有新增，那么需要同步修改脚本中的定义。

```python
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
```





## 执行方式

```shell
python3 create_patch.py -f -v -s /mnt/freemeos-code/robox-cmcc/dev/ -d /mnt/freemeos-code/robox-cmcc/patch-test/ -g build -g frameworks -g vendor -u xupeng
```

各个参数的含义可以查看 help `python3 create_patch.py -h`

```
usage: create_patch.py [-h] [-v] [-f] -s source path -d dest path -u git user
                       name -g git repository name

create patch for cmcc branch

optional arguments:
  -h, --help            show this help message and exit
  -v                    verbose mode
  -f                    forec create patch even patch file exist
  -s source path, --source source path
                        absolute path of repo repository
  -d dest path, --dest dest path
                        absolute path of repo repository
  -u git user name, --git_user git user name
                        absolute path of repo repository
  -g git repository name
                        folder name of git repository
```
