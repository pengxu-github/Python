# ！/usr/bin/python3
# -*- coding: utf-8 -*-

from android_tools.translate_tool.google_translate import TranslateGoogle

if __name__ == '__main__':
    trans = TranslateGoogle()
    for lang in ['en', 'zh', 'fr', 'ja', 'de']:
        response = trans.translate("who are you", lang)
        print("{}: {}".format(lang, response))
