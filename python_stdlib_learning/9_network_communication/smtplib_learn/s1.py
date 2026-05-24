# SMTP 标准库学习
# qegpizcjxcckdebe
# 基础-1：纯文本邮件的发送
import smtplib
from email.mime.text import MIMEText

# 配置信息
sender_email = "3135989009@qq.com"
sender_password = "qegpizcjxcckdebe"
recv_email = "xianzhisen_yang@outlook.com"
smtp_server = "smtp.qq.com"
smtp_port = 465

subject = "Python SMTP 测试发送邮件"
body = "这是一封测试邮件，使用Python里面的SMTP标准库发送。"
# 封装整个邮件对象
msg = MIMEText(body, "plain", "utf-8")
msg["From"] = sender_email
msg["To"] = recv_email
msg["Subject"] = subject

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
    server.login(sender_email, sender_password)

    server.sendmail(sender_email, recv_email, msg.as_string())
    print("邮件发送成功")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    if "server" in locals():
        server.quit()  # type: ignore
