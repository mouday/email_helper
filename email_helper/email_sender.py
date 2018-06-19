# -*- coding: utf-8 -*-

# @File    : email_helper.py
# @Date    : 2018-06-15
# @Author  : Peng Shiyu

# 邮件发送助手

# email负责构造邮件，smtplib负责发送邮件

from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import os

import smtplib

class EmailSender(object):

    def __init__(self, from_addr, password, server="smtp.163.com", port=25):
        # 发信人账号密码
        self.from_addr = from_addr
        self.password = password
        # 收件人地址
        self.to_addrs = []
        # SMTP服务器地址
        self.smtp_server = server
        self.smtp_port = port
        self.msg =self._get_email()
        self._add_sender(self.from_addr)

    # 添加标题
    def set_header(self, text):
        self.msg['Subject'] = Header(text, 'utf-8').encode()
        
    # 添加文本
    def add_text(self, text):
        self._add_content(text, "plain")

    # 添加邮件（优先）
    def add_html(self, html):
        self._add_content(html, "html")

    # 增加邮件地址
    def add_receiver(self, address):
        # msg['To'] 接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可
        self.to_addrs.append(address)

    # 增加多个邮件地址
    def add_receivers(self, addresses):
        self.to_addrs.extend(addresses)

    # 添加附件
    def add_attach(self, fullname):
        # 加上一个MIMEBase，从本地读取一个图片:
        filename = os.path.basename(fullname)
        with open(fullname, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            name, ext = os.path.splitext(filename)
            ext = ext.strip(".")
            mime = MIMEBase('image', ext, filename=filename)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            self.msg.attach(mime)

    # 发送
    def send(self):
        self._add_receivers()

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)  # SMTP协议默认端口是25
        # server.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, self.to_addrs, self.msg.as_string())
        server.quit()

    # 邮件对象添加内容
    def _add_content(self, text, text_type):
        # 'plain'表示纯文本, 'html'表示html文本，utf-8编码保证多语言兼容性
        self.msg.attach(MIMEText(text, text_type, 'utf-8'))

    # 格式化一个邮件地址
    def _format_addr(self, s):
        # 如果包含中文，需要通过Header对象进行编码
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    # 获取邮件对象
    def _get_email(self):
        # 同时支持HTML和Plain格式
        return  MIMEMultipart("alternative")

    # 邮件对象添加发送者
    def _add_sender(self, from_addr):
        self.msg['From'] = self._format_addr('%s <%s>'% (from_addr, from_addr))

    # 邮件对象添加收件人
    def _add_receivers(self):
        addrs = [self._format_addr('%s <%s>' % (addr, addr)) for addr in self.to_addrs]
        self.msg['To'] = ",".join(addrs)


if __name__ == '__main__':
    email = EmailSender("xxx@163.com", "xxx")
    email.set_header("你好")
    email.add_text("hello1")
    email.add_text("hello2")
    # email.add_attach("images/guilunmei.jpeg")
    # email.add_attach("images/guilunmei.jpeg")
    email.add_receiver("xxx@qq.com")
    email.add_receiver("ooo@qq.com")
    email.send()

