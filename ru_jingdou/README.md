# 修改和使用说明
[TOC]

## 1. 修改
### 1.1 chromedriver path 问题
具体错误：
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.
```
- 安装
进入如下界面：File -> settings -> Project: pycharm-workspace
点击右上角的`+`，进入 available packages 界面，搜索`chromedriver-py`，撰写本文时的版本号是 2.45.3。
- 代码修改
```python
from selenium import webdriver
...
+ chromedriver = "D:\software\python\Lib\site-packages\chromedriver_py\chromedriver_win32.exe"
...
- driver = webdriver.Chrome()
+ driver = webdriver.Chrome(chromedriver)
```

## 2. 使用
- 需要登录 QQ；
- QQ 账号需要已经绑定了京东账号。