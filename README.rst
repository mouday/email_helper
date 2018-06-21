email\_helper
=============

    only support python3

    默认服务器为163免费邮箱服务器，也可以自己配置

安装
====

::

    $ pip install email-helper

发送邮件
========

.. code:: python

    from email_helper.email_sender import EmailSender

    # 实例化
    email = EmailSender(from_addr="xxx@163.com", password="xxx")

    # 设置标题
    email.set_header("这是邮件标题")

    # 添加正文
    email.add_text("这是邮件的文本")

    # 添加收件人
    email.add_receiver("ooo@163.com")

    # 发送
    email.send()

接收邮件
========

.. code:: python

    from email_helper.email_receiver import EmailReceiver

    # 实例化
    client = EmailReceiver(email="xxx@163.com", password="xxx")

    # 接收最后一封邮件
    email = client.get_last_email()

    # 打印邮件信息
    for k, v in email.items():
        print(k , v)

    """
    From  <xxx@163.com>
    To  <ooo@163.com>
    Subject 这是邮件标题
    text ['这是邮件的文本']
    attachment []
    """
