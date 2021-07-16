# ！/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import re


class TranslateGoogle:
    def __init__(self):
        pass

    def translate(self, text, target_language):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/avif,image/webp,image/apng,*/*;q=0.8,application/"
                      "signed-exchange;v=b3;q=0.9",
            # "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                          "87.0.4280.66 Safari/537.36"
        }
        # request url
        url = "https://translate.google.com/_/TranslateWebserverUi/data/" \
              "batchexecute?rpcids=MkEWBc&f.sid=-2609060161424095358&bl=" \
              "boq_translate-webserver_20201203.07_p0&hl=zh-CN&soc-app=1&" \
              "soc-platform=1&soc-device=1&_reqid=359373&rt=c"
        # request data
        form_data = {
            "f.req": r"""[[["MkEWBc","[[\"{}\",\"auto\",\"{}\",true],[null]]",
        null,"generic"]]]""".format(
                text, target_language)
        }
        try:
            r = requests.post(url, headers=headers, data=form_data, timeout=60)
            if r.status_code == 200:
                # result = json.loads(r.text.split('\n')[3])
                # print("result: {}".format(result[0][2]))
                trans_results = re.findall(r',\[\[\\"(.*?)\\"', r.text)
                if trans_results:
                    trans_result = trans_results[0]
                else:
                    trans_result = ""
                return trans_result
        except Exception as e:
            print(e)
            return ""
