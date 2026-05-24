# 基础-2：发送给多个收件人
import smtplib
from email.mime.text import MIMEText

# 配置信息
sender_email = "3135989009@qq.com"
sender_password = "qegpizcjxcckdebe"
to_email = "3135989009@qq.com"
cc_email = "xianzhisen_yang@outlook.com"
bcc_email = "xianzhisen3135@gmail.com"
smtp_server = "smtp.qq.com"
smtp_port = 465

subject = "Python SMTP 测试发送邮件"
body = "这是一封测试邮件，使用Python里面的SMTP标准库发送。"

msg = MIMEText(body, "plain", "utf-8")
msg["From"] = sender_email
msg["To"] = to_email
msg["Cc"] = cc_email
msg["Subject"] = subject

# 所有收件人的列表
all_recv = [to_email, cc_email, bcc_email]
try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, all_recv, msg.as_string())
    print("发送成功")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    if "server" in locals():
        server.quit()  # type: ignore
