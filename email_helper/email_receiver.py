# -*- coding: utf-8 -*-

# @File    : get_email.py
# @Date    : 2018-06-17
# @Author  : Peng Shiyu

# 邮件收取助手

# poplib模块负责接收， email模块负责解析

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib

class EmailReceiver(object):

    def __init__(self, email, password, server="pop.163.com"):
    # 输入邮件地址, 口令和POP3服务器地址:
        self.email = email
        self.password = password
        self.pop3_server = server
        self._connect()
        self.message = {
            "From": None,
            "To": None,
            "Subject": None,
            "text": [],
            "attachment": []
        }  # 解析后的邮件内容



    # stat()返回邮件数量和占用空间:
    def get_stat(self):
        return self.server.stat()

    # list()返回所有邮件的编号:
    def get_list(self):
        resp, mails, octets = self.server.list()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
        return mails

    # 获取一封邮件
    def get_email(self, index):
        self._get_email(index)
        return self.message

    # 获取最新一封邮件, 注意索引号从1开始:
    def get_last_email(self):
        index = len(self.get_list())
        return self.get_email(index)

    # 连接到POP3服务器:
    def _connect(self):
        self.server = poplib.POP3(self.pop3_server)
        # 身份认证:
        self.server.user(self.email)
        self.server.pass_(self.password)

    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)

    def _get_welcome(self):
        # 可选:打印POP3服务器的欢迎文字:
        return self.server.getwelcome().decode('utf-8')

    # 获取一封邮件
    def _get_email(self, index):
        resp, lines, octets = self.server.retr(index)

        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)

        # 可以根据邮件索引号直接从服务器删除邮件:
        # server.dele(index)
        return self._get_email_content(msg)


    def __del__(self):
        # 关闭连接:
        self.server.quit()

    # 解码
    def _decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    # 获取编码
    def _guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset


    # 解析邮件 indent用于缩进显示:
    def _parse_email(self, msg, indent=0):
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = self._decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        name = self._decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                self.message[header] = value

        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                self._parse_email(part, indent + 1)

        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = self._guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                self.message["text"].append(content)
            else:
                self.message["attachment"].append(content_type)

    # 获取邮件内容
    def _get_email_content(self, msg):
        self._parse_email(msg)
        return self.message


if __name__ == '__main__':
    email = EmailReceiver("xxx@163.com", "xxx")
    msg = email.get_last_email()
    print(msg)

