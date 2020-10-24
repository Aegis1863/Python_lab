# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 13:22:01 2020

@author: LiSunBowen
"""
def sendmail(txt,sd,rc,ht,un,pw，fn,rn):
    '''
    txt:邮件文本
    sd：发送者邮箱地址
    rc：接收者邮箱地址
    ht: host 服务器地址
    un: 用户名
    pw: 密码（口令）
    fn: 发件人称呼
    rn: 收件人称呼
    '''
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 第三方 SMTP 服务
    mail_host= ht  #设置服务器
    mail_user= un    #用户名
    mail_pass = pw # 口令

    sender = sd
    receivers = [rc]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(txt, 'plain', 'utf-8')
    message['From'] = Header(fn, 'utf-8')
    message['To'] =  Header(rn, 'utf-8')

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
