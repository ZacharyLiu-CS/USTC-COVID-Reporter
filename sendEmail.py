# -*- coding: UTF-8 -*-
import smtplib
import sys
from email.mime.text import MIMEText
from email.header import Header

class SendMessage:
    def __init__(self ) -> None:
        return
    def send(self, to_msg :str, to_add :str, mail_user :str, mail_pass :str) ->bool:
        mail_host = "mail.ustc.edu.cn"
        mail_user = mail_user
        mail_pass = mail_pass
        sender = mail_user
        receivers = [to_add]
        conten = to_msg
        message = MIMEText(conten, 'plain', 'utf-8')
        message['From'] = sender
        message['To'] = to_add
        subject = 'COVID-19'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            return True
        except smtplib.SMTPException as e:
            return False
