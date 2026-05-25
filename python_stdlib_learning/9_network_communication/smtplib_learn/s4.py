# 进阶-1：发送HTML格式邮件

import smtplib
from email.mime.text import MIMEText

# 配置信息
sender_email = "your_send_email"
sender_password = "qegpizcjxcckdebe"
recv_email = "your_recv_email"
smtp_server = "smtp.qq.com"
smtp_port = 465
# 创建邮件内容
subject = "Python HTML 格式邮件"
html_body = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>HTML测试邮件</title>
</head>
<body style="font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
        <h1 style="color: #2e6c80; text-align: center; border-bottom: 2px solid #2e6c80; padding-bottom: 10px;">
            这是一封HTML格式的邮件
        </h1>
        
        <p>尊敬的用户：</p>
        
        <p>这是使用Python smtplib库发送的<strong>HTML格式测试邮件</strong>。</p>
        
        <h3 style="color: #4a90e2;">邮件特点：</h3>
        <ul>
            <li>支持<strong style="color: #ff0000;">彩色文字</strong></li>
            <li>支持<em>斜体文字</em></li>
            <li>支持<a href="https://www.python.org" style="color: #4a90e2; text-decoration: none;">超链接</a></li>
            <li>支持表格和列表</li>
        </ul>
        
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background-color: #f5f5f5;">
                <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">功能</th>
                <th style="border: 1px solid #ddd; padding: 10px; text-align: left;">状态</th>
            </tr>
            <tr>
                <td style="border: 1px solid #ddd; padding: 10px;">纯文本邮件</td>
                <td style="border: 1px solid #ddd; padding: 10px; color: green;">✅ 已支持</td>
            </tr>
            <tr>
                <td style="border: 1px solid #ddd; padding: 10px;">HTML邮件</td>
                <td style="border: 1px solid #ddd; padding: 10px; color: green;">✅ 已支持</td>
            </tr>
            <tr>
                <td style="border: 1px solid #ddd; padding: 10px;">附件邮件</td>
                <td style="border: 1px solid #ddd; padding: 10px; color: orange;">⏳ 即将支持</td>
            </tr>
        </table>
        
        <p style="margin-top: 30px; color: #666; font-size: 14px;">
            祝您使用愉快！<br>
            Python邮件发送程序
        </p>
    </div>
</body>
</html>
"""

msg = MIMEText(html_body, "html", "utf-8")
msg["From"] = sender_email
msg["To"] = recv_email
msg["Subject"] = subject

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recv_email, msg.as_string())
    print("HTML格式邮件发送成功")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    if "server" in locals():
        server.quit()  # type: ignore
