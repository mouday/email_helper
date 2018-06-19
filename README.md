# email_helper

only support python3


# 默认服务器为163免费邮箱服务器，也可以自己配置


# 发送邮件
```
from email_helper.email_sender import EmailSender

email = EmailSender(from_addr="xxx@163.com", password="xxx")
email.set_header("这是邮件标题")
email.add_text("这是邮件的文本")
email.add_receiver("ooo@163.com")
email.send()
```

# 接收邮件
```
from email_helper.email_receiver import EmailReceiver

client = EmailReceiver(email="xxx@163.com", password="xxx")
email = client.get_last_email()
for k, v in email.items():
    print(k , v)

"""
From  <xxx@163.com>
To  <ooo@163.com>
Subject 这是邮件标题
text ['这是邮件的文本']
attachment []
"""

```