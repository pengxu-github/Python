import queue
import time
import tkinter
from queue import Queue
from threading import Thread
from urllib.parse import parse_qs

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.wait import WebDriverWait

# 额外抽取的授权模块
from utils import auth

chrome_driver = "D:\software\python\Lib\site-packages\chromedriver_py\chromedriver_win32.exe"


class Collect(object):
    """借助券妈妈平台褥京东京豆"""

    def __init__(self, sleep=3, months=None, days=None):
        self.timeout, self.months, self.days = sleep, None, None
        # 爬取规则
        if months:
            month_interval = months.split('-')
            start_month, end_month = int(month_interval[0]), int(
                month_interval[-1])
            self.months = list(map(lambda m: '{}月'.format(m),
                range(start_month, end_month + 1)))
        if days:
            day_interval = days.split('-')
            start_day, end_day = int(day_interval[0]), int(day_interval[-1])
            self.days = list(
                map(lambda d: '{}日'.format(d), range(start_day, end_day + 1)))
        # 手机店铺(用作提醒输出，可复制链接到手机端领取)
        self.m_shop = []
        # 统计京豆总数
        self.jing_dou = 0
        self._thread_running = False

        print('begin init root')
        self.root = tkinter.Tk()
        self.root.title('领京豆')
        self.root['width'] = 500
        self.root['height'] = 300
        self.text_value = tkinter.StringVar()
        notify_text = tkinter.Label(self.root, text='京豆领取进展:')
        notify_text.place(x=20, y=20, width=100, height=20)
        text_detail = tkinter.Label(self.root, textvariable=self.text_value)
        text_detail.place(x=20, y=50, width=460, height=160)
        self.log_text = text_detail
        bt_start = tkinter.Button(self.root, text='开始', command=self._run())
        bt_start.place(x=20, y=220, width=200, height=60)
        self.start_bt = bt_start
        bt_end = tkinter.Button(self.root, text='结束', command=self._terminate())
        bt_end.place(x=240, y=220, width=200, height=60)
        self.end_bt = bt_end

        # used to communicate between main thread (UI) and worker thread
        self.thread_queue = queue.Queue()

    def show(self):
        self._dump()
        self.root.mainloop()

    def _run(self):
        _thread_running = True

        print('begin collect with thread')
        new_thread = Thread(target=self._start())
        new_thread.start()
        # schedule a time-task to check UI
        # it's in main thread, because it's called by self.root
        self.root.after(100, self.listen_for_result)

    def listen_for_result(self):
        """
        Check if there is something in the queue.
        Must be invoked by self.root to be sure it's running in main thread
        """
        try:
            txt = self.thread_queue.get(False)
            print('listen_for_result: {}'.format(txt))
            self.text_value = txt
        except queue.Empty:  # must exist to avoid trace-back
            pass
        finally:
            print('listen_for_result finally')
            # if self.progress.get() < self.progressbar['maximum']:
            #     self.root.after(100, self.listen_for_result)
            # else:
            #     self.btn.config(state=tkinter.NORMAL)

    def _crawl_url(self):
        """ 抓取京豆更新页, 获得店铺京豆领取地址"""

        # 日期更新页
        qmm_collect = 'http://www.quanmama.com/zhidemai/2459063.html'
        bs = BeautifulSoup(requests.get(qmm_collect).text, 'html.parser')
        for link in bs.tbody.find_all('a'):
            text = link.text
            if self.months:
                if not list(filter(lambda m: m in text, self.months)): continue
            if self.days:
                if not list(filter(lambda d: d in text, self.days)): continue

            qmm_detail = link.get('href')

            # 店铺领取页
            resp = requests.get(qmm_detail)
            bs = BeautifulSoup(resp.text, 'html.parser')
            for body in bs.find_all('tbody'):
                for mall in body.find_all('a'):
                    url = self._parse_url(mall.get('href'))
                    if 'shop.m.jd.com' in url:
                        self.m_shop.append(url)
                    else:
                        yield url

    @staticmethod
    def _parse_url(url):
        """提取URL中的url参数"""

        mall_url = parse_qs(url).get('url')
        return mall_url.pop() if mall_url else url

    def _start(self):
        """ 登录京东，领取店铺羊毛"""

        malls = set(self._crawl_url())
        print('共有 %d 个可褥羊毛PC端店铺页面' % len(malls))

        m_malls = self.m_shop
        print('共有 %d 个可褥羊毛手机端店铺页面' % len(m_malls))
        for m_mall in m_malls:
            print(m_mall)

        if malls:
            # 登陆京东(Chrome、PhantomJS or FireFox)
            # driver = webdriver.PhantomJS()
            driver = webdriver.Chrome(chrome_driver)
            jd_login = 'https://passport.jd.com/new/login.aspx'
            driver.get(jd_login)

            # 窗口最大化
            driver.maximize_window()

            # QQ授权登录
            driver.find_element_by_xpath(
                '//*[@id="kbCoagent"]/ul/li[1]/a').click()
            auth.qq(driver)
            time.sleep(self.timeout)

            # 开始褥羊毛
            for i, detail in enumerate(malls):
                if not self._thread_running:
                    return
                driver.get(detail)
                txt = '%d.店铺: %s'.format((i + 1, detail), end='')
                print(txt)
                self.thread_queue.put(txt)
                try:
                    # 查找"领取"按钮
                    btn = WebDriverWait(driver, self.timeout).until(
                        lambda d: d.find_element_by_css_selector(
                            "[class='J_drawGift d-btn']"))
                except TimeoutException:
                    # 失败大多数情况下是无羊毛可褥(券妈妈平台只是简单汇总但不一定就有羊毛)
                    print(' 领取失败, TimeoutException ')
                else:
                    try:
                        # 输出羊毛战绩
                        items = WebDriverWait(driver, self.timeout).until(
                            lambda d: d.find_elements_by_css_selector(
                                "[class='d-item']"))
                        for item in items:
                            item_type = item.find_element_by_css_selector(
                                "[class='d-type']").text
                            item_num = item.find_element_by_css_selector(
                                "[class='d-num']").text
                            if item_type == '京豆': self.jing_dou += item_num
                            print(' {}{} '.format(item_type, item_num), end='')
                    except:
                        # 此处异常不太重要, 忽略
                        pass
                    finally:
                        btn.click()
                        print(' 领取成功')

            # 以下附加功能可选
            self._print_jing_dou()
            self._un_subscribe(driver)
            self._finance_sign(driver)

    def _terminate(self):
        self._thread_running = False

    def _print_jing_dou(self):
        print('O(∩_∩)O哈哈~, 共褥到了{}个京豆，相当于RMB{}元', self.jing_dou,
            self.jing_dou / 100)

    def _un_subscribe(self, driver):
        """批量取消店铺关注"""

        # 进入关注店铺
        subscribe_shop = 'https://t.jd.com/vender/followVenderList.action'
        driver.get(subscribe_shop)

        try:
            # 批量操作
            batch_btn = WebDriverWait(driver, self.timeout).until(
                lambda d: d.find_element_by_xpath(
                    '//*[@id="main"]/div/div[2]/div[1]/div[2]/div[2]/div/a'))
            batch_btn.click()
            # 全选店铺
            all_btn = WebDriverWait(driver, self.timeout).until(
                lambda d: d.find_element_by_xpath(
                    '//*[@id="main"]/div/div[2]/div[1]/div[2]/div[2]/div/div/span[1]'))
            all_btn.click()
            # 取消关注
            cancel_btn = WebDriverWait(driver, self.timeout).until(
                lambda d: d.find_element_by_xpath(
                    '//*[@id="main"]/div/div[2]/div[1]/div[2]/div[2]/div/div/span[2]'))
            cancel_btn.click()
            # 弹框确认
            confirm_btn = WebDriverWait(driver, self.timeout).until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[7]/div[3]/a[1]"))
        except TimeoutException:
            print(' 批量取关店铺失败, TimeoutException ')
        else:
            confirm_btn.click()
            print(' 已批量取消关注店铺')

    def _finance_sign(self, driver):
        """京东金融签到领钢镚"""

        # 进入京东金融
        jr_login = 'https://jr.jd.com/'
        driver.get(jr_login)

        try:
            # 点击签到按钮
            sign_btn = WebDriverWait(driver, self.timeout).until(
                lambda d: d.find_element_by_xpath(
                    '//*[@id="primeWrap"]/div[1]/div[3]/div[1]/a'))
        except TimeoutException:
            print(' 京东金融签到失败, TimeoutException ')
        else:
            sign_btn.click()
            print(' 京东金融签到成功')

    def _dump(self):
        print('all parameters:'
              '\n\tself.timeout = {}\n\tself.months = {}\n\tself.days = {}'
              '\n\tself.m_shop = {}\n\tself.jing_dou = {}'
            .format(self.timeout, self.months, self.days, self.m_shop, self.jing_dou))


if __name__ == '__main__':
    collect = Collect(sleep=3, months='3-4', days='1-31')
    collect.show()
