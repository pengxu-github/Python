import requests
import time
import random


class SendData:

    def __init__(self):
        self.url = 'https://www.zhihu.com/api/v4/message'
        self.cookie = {}  # 登录需要cookie
        self.header = {}  # useragent 伪装成浏览器

    def send(self, dat):
        self.html = requests.post(self.url, json=dat, cookies=self.cookie, header=self.header)
        print(self.html.status_code)
        print(self.html.text)


if __name__ == "__main__":
    send = SendData()  # 隐身 实例化
    '''
    dat = {
        'type': 'common',
        'content': 'test',  # 发送的内容
        'receiver_hash': '242d11e5457cf199787f3ddb1d3e76e9'
    }
    '''
    with open('filepath') as f:
        for hash in f:
            time.sleep(random.randint(15,30))
            hash = hash.strip('\n')
            dat = {
                'type': 'common',
                'content': 'test',  # 发送的内容
                'receiver_hash': hash
            }
    send.send(dat)
    # SendData.Send(SendData())
