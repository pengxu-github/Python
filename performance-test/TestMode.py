#!/usr/bin/env python

from Logcat import Logout

APPS_LIST = []

PATHS = []

TABLET_OS = ['Freeme OS', '阿里', '酷赛']

TEST_LOAD_MODE = ['轻载', '重载']

APPS_FREEME = [['tessst', 'com.example.tessst/com.example.tessst.MainActivity', 'com.example.tessst', 0],
               ['计算器', 'com.android.calculator2/com.android.calculator2.Calculator', 'com.android.calculator2', 1],
               ['拨号', 'com.android.dialer/com.android.dialer.DialtactsActivity', 'com.android.dialer', 2],
               ['音乐', 'com.android.music/com.android.music.MusicBrowserActivity', 'com.android.music', 3],
               ['相机', 'com.mediatek.camera/com.android.camera.CameraLauncher', 'com.mediatek.camera', 4],
               ['文件管理', 'com.mediatek2.filemanager/com.mediatek2.filemanager.FileManagerOperationActivity',
                'com.mediatek2.filemanager', 5],
               ['天气', 'com.tianqi2345/com.tianqi2345.activity.CoveryActivity', 'com.tianqi2345', 6],
               ['微信', 'com.tencent.mm/.ui.LauncherUI', 'com.tencent.mm', 7],
               ['QQ', 'com.tencent.mobileqq/.activity.SplashActivity', 'com.tencent.mobileqq', 8],
               ['视频', 'com.tencent.qqlive/com.tencent.qqlive.ona.activity.WelcomeActivity', 'com.tencent.qqlive', 9],
               ['浏览器', 'com.android.browser/com.tencent.mtt.MainActivity', 'com.android.browser', 10],
               ['联系人', 'com.android.contacts/.activities.PeopleActivity', 'com.android.contacts', 11],
               ['信息', 'com.android.mms/.ui.ConversationList', 'com.android.mms', 12],
               ['日历', 'com.android.calendar/com.android.calendar.AllInOneActivity', 'com.android.calendar', 13],
               ['相册', ' com.freeme.gallery/.app.GalleryActivity', 'com.freeme.gallery', 14],
               ['FM', 'com.android.fmradio/com.android.fmradio.FmMainActivity', 'com.android.fmradio', 15],
               ['录音机', 'com.android.soundrecorder/.SoundRecorder', 'com.android.soundrecorder', 16],
               ['设置', 'com.android.settings/.Settings', 'com.android.settings', 17],
               ['安全中心', 'com.zhuoyi.security.lite/com.zhuoyi.security.base.LauncherActivity',
                'com.zhuoyi.security.lite', 18],
               ['健康中心', 'com.freeme.healthcenter/.HealthCenterActivity', 'com.freeme.healthcenter', 19],
               ['时钟', 'com.android.deskclock/com.android.deskclock.DeskClock', 'com.android.deskclock', 20],
               ['爱奇艺', 'com.qiyi.video/org.qiyi.android.video.MainActivity', 'com.qiyi.video', 21],
               ['语音助手', 'com.freeme.voiceassistant/.ManMachinePanel', 'com.freeme.voiceassistant', 22],
               ['卓易市场', 'com.zhuoyi.market/.Splash', 'com.zhuoyi.market', 23],
               ['美化中心', 'com.freeme.themeclub/.MainActivity', 'com.freeme.themeclub', 24],
               ['小影', 'com.freeme.os.home/com.freeme.os.home.activity.FragmentHolder', 'com.freeme.os.home', 25]
               ]

APPS_ALI = [['tessst', 'com.example.tessst/com.example.tessst.MainActivity', 'com.example.tessst', 0],
            ['计算器', 'com.yunos.calculator/.Calculator', 'com.yunos.calculator', 1],
            ['拨号', 'com.yunos.alicontacts/.activities.PeopleActivity2', 'com.yunos.alicontacts', 2],
            ['音乐', 'fm.xiami.yunos/fm.xiami.bmamba.activity.StartActivity', 'fm.xiami.yunos', 3],
            ['相机', ' com.yunos.camera/.CameraActivity', 'com.yunos.camera', 4],
            ['文件管理', 'com.aliyunos.filemanager/.FileManagerAppFrame', 'com.freeme.filemanager', 5],
            ['天气', 'sina.mobile.tianqitongyunos/sina.mobile.tianqitong.yunos.ui.MainActivity',
             'sina.mobile.tianqitongyunos', 6],
            ['微信', 'com.tencent.mm/.ui.LauncherUI', 'com.tencent.mm', 7],
            ['QQ', 'com.tencent.mobileqq/.activity.SplashActivity', 'com.tencent.mobileqq', 8],
            ['视频', 'com.aliyun.video.youku/com.aliyun.video.VideoCenterActivity', 'com.aliyun.video.youku', 9],
            ['浏览器', 'com.UCMobile/com.uc.browser.InnerUCMobile', 'com.UCMobile', 10],
            ['设置', 'com.android.settings/.Settings', 'com.android.settings', 11]
            ]

APPS_KUSAI = [['tessst', 'com.example.tessst/com.example.tessst.MainActivity', 'com.example.tessst', 0],
              ['计算器', 'com.android.calculator2/.Calculator', 'com.android.calculator2', 1],
              ['拨号', 'com.android.dialer/com.android.dialer.DialtactsActivity', 'com.android.dialer', 2],
              ['音乐', 'com.android.music/com.android.music.MusicBrowserActivity', 'com.android.music', 3],
              ['相机', 'com.mediatek.camera/com.android.camera.CameraLauncher', 'com.mediatek.camera', 4],
              ['文件管理', 'com.mediatek2.filemanager/com.mediatek2.filemanager.FileManagerOperationActivity',
               'com.mediatek2.filemanager', 5],
              ['天气', 'com.tianqi2345/com.tianqi2345.activity.CoveryActivity', 'com.tianqi2345', 6],
              ['微信', 'com.tencent.mm/.ui.LauncherUI', 'com.tencent.mm', 7],
              ['QQ', 'com.tencent.mobileqq/.activity.SplashActivity', 'com.tencent.mobileqq', 8],
              ['视频', 'com.tencent.qqlive/com.tencent.qqlive.ona.activity.WelcomeActivity', 'com.tencent.qqlive', 9],
              ['浏览器', 'com.android.browser/com.tencent.mtt.MainActivity', 'com.android.browser', 10],
              ['设置', 'com.android.settings/.Settings', 'com.android.settings', 11]
              ]

# QQ, 微信，相机,浏览器，设置
PATH1_ALI = [APPS_ALI[8], APPS_ALI[7], APPS_ALI[4], APPS_ALI[10], APPS_ALI[11]]

# QQ, 微信，相机,浏览器,设置,音乐
PATH2_ALI = [APPS_ALI[8], APPS_ALI[7], APPS_ALI[4], APPS_ALI[10], APPS_ALI[11], APPS_ALI[3]]

# QQ, 微信，相机,浏览器,设置,音乐，视频
PATH3_ALI = [APPS_ALI[8], APPS_ALI[7], APPS_ALI[4], APPS_ALI[10], APPS_ALI[11], APPS_ALI[3], APPS_ALI[9]]

PATHS_ALI = [PATH1_ALI, PATH2_ALI, PATH3_ALI]

# QQ, 联系人，信息, 日历,相册，FM，录音机
PATH1_FREEME = [APPS_FREEME[11], APPS_FREEME[12], APPS_FREEME[13], APPS_FREEME[14], APPS_FREEME[15], APPS_FREEME[16]]
# QQ, 浏览器，视频,设置,安全中心,健康中心
PATH2_FREEME = [APPS_FREEME[10], APPS_FREEME[9], APPS_FREEME[17], APPS_FREEME[18], APPS_FREEME[19]]
# QQ, 时钟，爱奇艺,语音助手,卓易市场,信息，美化中心
PATH3_FREEME = [APPS_FREEME[20], APPS_FREEME[21], APPS_FREEME[22], APPS_FREEME[23], APPS_FREEME[12], APPS_FREEME[24]]

PATHS_FREEME = [PATH1_FREEME, PATH2_FREEME, PATH3_FREEME]

# QQ, 微信，相机,浏览器，设置
PATH1_KUSAI = [APPS_KUSAI[8], APPS_KUSAI[7], APPS_KUSAI[4], APPS_KUSAI[10], APPS_KUSAI[11]]
# QQ, 微信，相机,浏览器,设置,音乐
PATH2_KUSAI = [APPS_KUSAI[8], APPS_KUSAI[7], APPS_KUSAI[4], APPS_KUSAI[10], APPS_KUSAI[11], APPS_KUSAI[3]]
# QQ, 微信，相机,浏览器,设置,音乐，视频
PATH3_KUSAI = [APPS_KUSAI[8], APPS_KUSAI[7], APPS_KUSAI[4], APPS_KUSAI[10], APPS_KUSAI[11], APPS_KUSAI[3],
               APPS_KUSAI[9]]

PATHS_KUSAI = [PATH1_KUSAI, PATH2_KUSAI, PATH3_KUSAI]

overload = True


class TestMode:
    def __init__(self):
        self.tablet_os = 0
        self.load_mode = 0

    def get_os(self):

        while True:
            for i in range(len(TABLET_OS)):
                Logout.show_message(str(i + 1) + ' : ' + TABLET_OS[i] + '\n')

            tablet_os = input('请选择平台：')
            if tablet_os.isdigit():
                __int_tablet_os = int(tablet_os)
                if __int_tablet_os < 1 or __int_tablet_os > len(TABLET_OS):
                    Logout.show_message('输入无效，请重试！！！')
                    continue
                else:
                    self.tablet_os = __int_tablet_os
                    break
            else:
                Logout.show_message('输入无效，请重试！！！')
                continue

        while True:
            for i in range(len(TEST_LOAD_MODE)):
                Logout.show_message(str(i + 1) + ' : ' + TEST_LOAD_MODE[i] + '\n')

            load_mode = input('请选择测试模式：')
            if load_mode.isdigit():
                __int_load_mode = int(load_mode)
                if __int_load_mode < (len(TEST_LOAD_MODE) - 1) or __int_load_mode > len(TEST_LOAD_MODE):
                    Logout.show_message('输入无效，请重试！！！')
                    continue
                else:
                    self.load_mode = __int_load_mode
                    break

            else:
                Logout.show_message('输入无效，请重试！！！')
                continue

    def setTestMode(self):
        global overload
        global APPS_LIST
        global PATHS

        if self.tablet_os == 1:
            APPS_LIST = APPS_FREEME
            PATHS = PATHS_FREEME
        elif self.tablet_os == 2:
            APPS_LIST = APPS_ALI
            PATHS = PATHS_ALI
        elif self.tablet_os == 3:
            APPS_LIST = APPS_KUSAI
            PATHS = PATHS_KUSAI

        if self.load_mode == 1:
            overload = False
        elif self.load_mode == 2:
            overload = True


def init():
    testMode = TestMode()
    testMode.get_os()
    testMode.setTestMode()


def getOverLoadMode():
    global overload
    return overload


def getAllAppsList():
    global APPS_LIST
    return APPS_LIST


def getOverloadPaths():
    global PATHS
    return PATHS


if __name__ == "__main__":
    Logout.show_message('I am TestMode')
    init()
    Logout.show_message('---------------------')
    Logout.show_message('APPS_LIST：\n')
    Logout.show_message(APPS_LIST)
    Logout.show_message('PATHS\n')
    Logout.show_message(PATHS)
    Logout.show_message('---------------------')
    Logout.show_message('OverLoad: ' + str(overload))
