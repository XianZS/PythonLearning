# 基础-3：使用加密连接

import smtplib
from email.mime.text import MIMEText
from typing import final

# 配置信息
sender_email = "3135989009@qq.com"
sender_password = "qegpizcjxcckdebe"
recv_email = "xianzhisen_yang@outlook.com"
smtp_server = "smtp.qq.com"
smtp_port = 587

subject = "Python SMTP TLS 加密测试发送邮件"
body = "这是一封测试邮件，使用Python里面的SMTP标准库发送。"


msg = MIMEText(body, "plain", "utf-8")
msg["From"] = sender_email
msg["To"] = recv_email
msg["Subject"] = subject

try:
    server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
    # 启动TLS加密
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recv_email, msg.as_string())
    print("TLS加密邮件发送成功")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    if "server" in locals():
        server.quit()  # type: ignore
