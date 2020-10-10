# -*- coding: utf-8 -*-
"""
Spyder Editor

Writed by LiSunbowen.
"""

import requests
import json
print('## 由LiSunBowen 编写 ##')
print('## 按Ctrl+c可中止程序 ##\n')
while True:
    question = input('题干信息：') # 输入问题
    url = 'https://www.shuakeya.com/daanan/api/web.php' # 接口网址
    header = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Connection': 'keep-alive', 'Content-Length': '5', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'UM_distinctid=172b305a75344e-067bf99ff86e8a-5f351240-144000-172b305a754a47; CNZZDATA1278702864=912698011-1592141392-null%7C1592141392; _aihecong_chat_visitorId=5ee626517df6366a94f27bbe; _aihecong_chat_last=%7B%22time%22%3A1602319610725%2C%22source%22%3A%22DirectEntry%22%2C%22entranceUrl%22%3A%22https%3A%2F%2Fwww.shuakeya.com%2Fdaanan%2F%22%2C%22entranceTitle%22%3A%22%E7%AD%94%E6%A1%88%E4%B8%80%E7%82%B9%E9%80%9A%22%7D; _aihecong_chat_address=%7B%22country%22%3A%22%E4%B8%AD%E5%9B%BD%22%2C%22region%22%3A%22%E6%B9%96%E5%8C%97%22%2C%22city%22%3A%22%E6%AD%A6%E6%B1%89%22%7D; _aihecong_chat_visibility=true'}
    datas = {'q': question} # 表单数据 储存问题
    r = requests.post(url, data=datas, headers=header, timeout=5) # 向接口提交表单数据
    if r.status_code == 200:
        ans = json.loads(r.text)['data']['answer'].replace('\n',' ').replace('<br>',' ')
        ques = json.loads(r.text)['data']['question'].replace('\n',' ').replace('<br>',' ')
        print('\n>> 最佳匹配题干为：%s\n'%ques)
        print('>> 对应答案：%s\n'%ans)
    else:
        print('网络异常\n')
