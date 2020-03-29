
# coding=UTF-8
# __author__='照顾一下'

import smtplib
import os
import subprocess
import tkMessageBox
from email.mime.text import MIMEText

mail_user = 'xx'      # 发送方邮箱
mail_pass = 'xx'       # 填入发送方邮箱的授权码  百度:QQ邮箱授权码如何获取 查看教程
mail_namelist = ["xx", "xx"]     # 收件人邮箱，可以选多个
# 这个是上传到fir上需要的token，自行百度
fir_token = 'xx'


# 上传ipa
def send_ipa(ipa_path):
    print ipa_path
    if os.path.exists(ipa_path) == 1:
        try:
            subprocess.call(["fir", "login", fir_token])
            subprocess.call(["fir", "publish", ipa_path])
            print "发送 " + ipa_path
            return True
        except subprocess.CalledProcessError, exc:
            tkMessageBox.showerror(exc)
            return False
    else:
        tkMessageBox.showerror("警告", "打包失败，ipa文件不存在")
        return False


# 发送邮件
def send_qq_email(title, content):
    try:
        # content = "新版本已发布请前往:\n" + 'http://fir.im' + " 下载测试" + "\n更新内容:" + conen
        msg = MIMEText(str(content))
        # 设置标题
        msg["Subject"] = title
        # 发件邮箱
        msg["From"] = mail_user
        # 收件邮箱
        msg["To"] = ";".join(mail_namelist)
        # 设置服务器、端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(mail_user, mail_pass)
        # 发送邮件
        s.sendmail(mail_user, mail_namelist, msg.as_string())
        s.quit()
        print ("邮件发送成功!")
    except smtplib.SMTPException:
        print ("邮件发送失败!")