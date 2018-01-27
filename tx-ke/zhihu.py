import random
import time

import requests


class SendData:

    def __init__(self):
        self.url = 'https://www.zhihu.com/api/v4/message'
        self.cookie = {}  # 登录需要cookie
        # User-Agent 伪装成浏览器
        self.header = {
            'User-Agent',
            'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'
        }

    def send(self, data):
        self.html = requests.post(self.url, json=data, cookies=self.cookie, header=self.header)
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
            time.sleep(random.randint(15, 30))
            hash = hash.strip('\n')
            dat = {
                'type': 'common',
                'content': 'test',  # 发送的内容
                'receiver_hash': hash
            }
    send.send(dat)
    # SendData.Send(SendData())
