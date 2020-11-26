# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import json
import PySimpleGUI as sg

def getans(question):
    try:
        datas = {'q': question}
        url = 'https://www.shuakeya.com/daanan/api/web.php' # 接口网址
        r = requests.post(url, data=datas, timeout=5)
        ans = json.loads(r.text)['data']['answer'].replace('\n',' ').replace('<br>',' ')
        ques = json.loads(r.text)['data']['question'].replace('\n',' ').replace('<br>',' ')
        return ques,ans
    except:
        return None,None
sg.ChangeLookAndFeel('TealMono')
# Define the window's contents
layout = [[sg.Text("请输入题干信息",font='微软雅黑 11')],
          [sg.Multiline(size=(50,3),key='-INPUT-',font='微软雅黑 11')],
          [sg.Text("检索匹配题干（不一定完全相同）",font='微软雅黑 11')],
          [sg.Output(size=(50,5), key='-OUTPUT1-',font='微软雅黑 11')],
          [sg.Text("该题答案",font='微软雅黑 11')],
          [sg.Output(size=(50,5), key='-OUTPUT2-',font='微软雅黑 11')],
          [sg.Text("*注意，不要点查询过快，至少需要间隔一秒钟以上*",font='微软雅黑 11',text_color='red')],
          [sg.Button('开始查询',font='微软雅黑 11'), sg.Button('退出',font='微软雅黑 11')]]

# Create the window
sg.SetOptions(text_justification='left')

window = sg.Window('网课查答案', layout)
# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == '退出':
        break
    # Output a message to the window

    ques, ans = getans(values['-INPUT-'])
    if ques:
        window['-INPUT-'].update('')
        window['-OUTPUT1-'].update('>>> 最佳匹配题干 <<<\n' + ques)
        window['-OUTPUT2-'].update('>>> 答案为 <<<\n' + ans)
    else:
        window['-OUTPUT1-'].update('出现网络异常或其他问题')

# Finish up by removing from the screen
window.close()
