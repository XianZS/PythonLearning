# 进阶-2：带附件的邮件
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from ssl import enum_certificates

# 配置信息
sender_email = "3135989009@qq.com"
sender_password = "qegpizcjxcckdebe"
recv_email = "xianzhisen_yang@outlook.com"
smtp_server = "smtp.qq.com"
smtp_port = 465
attach_path = "./email_html.html"

# 创建附件对象
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = recv_email
msg["Subject"] = "这是带着附件的邮件"

# 创建邮件正文对象
body = "这是邮件正文"
body_msg = MIMEText(body, "plain", "utf-8")
msg.attach(body_msg)

try:
    with open(attach_path, "rb") as f:
        attachment = MIMEApplication(f.read())
    # 获取附件的文件名
    filename = os.path.basename(attach_path)
    # 设置附件的详细信息
    attachment.add_header("Content-Disposition", "attachment", filename=filename)
    # 将附件对象添加到邮件之中
    msg.attach(attachment)
    print("成功添加附件")
except Exception as e:
    print(f"[Error]:{e}")


try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recv_email, msg.as_string())
    print("邮件发送成功")
except Exception as e:
    print(f"[Error]:{e}")
