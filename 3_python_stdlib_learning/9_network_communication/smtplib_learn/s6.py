# 进阶-3：异常处理和重传机制
import smtplib
from email.mime.text import MIMEText
import time
from smtplib import (
    SMTPException,
    SMTPAuthenticationError,
    SMTPConnectError,
    SMTPRecipientsRefused,
    SMTPSenderRefused,
    SMTPDataError,
)

# 配置信息
sender_email = "your_send_email"
# sender_password = "qegpizcjxcckdebe"
sender_password = "qegpizcjxcckdadw"
recv_email = "your_recv_email"
smtp_server = "smtp.qq.com"
smtp_port = 465
max_retres = 3
retr_delay = 5


def send_email_with_retry():
    # 创建邮件的基础信息
    subject = "这是邮件主题"
    body = "这是一封测试异常处理和重传机制的测试邮件。"
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = sender_email
    msg["To"] = recv_email
    msg["Subject"] = subject
    for attempt in range(1, max_retres + 1):
        server = None
        try:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recv_email, msg.as_string())
            print(f"邮件发送成功，第{attempt}次尝试")
            return True
        except SMTPAuthenticationError:
            print("邮箱验证失败")
            return False
        except SMTPConnectError:
            print("邮箱连接失败")
            return False
        except SMTPRecipientsRefused:
            print("收件人地址被拒绝")
            return False
        except SMTPSenderRefused:
            print("发件人地址被拒绝")
            return False
        except (SMTPDataError, SMTPException):
            print("邮件数据错误/邮件协议错误")
            return False
        finally:
            if server:
                try:
                    server.quit()
                except Exception:
                    pass
        if attempt < max_retres:
            print("正在等待")
            time.sleep(retr_delay)
    print(f"{max_retres}次重传都失败了，请见信息")
    return False


if __name__ == "__main__":
    judge = send_email_with_retry()
    if judge:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
