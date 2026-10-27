# ftplib 标准库学习
# 两个独立的TCP连接
# 控制连接:21,发送命令和接收响应
# 数据连接:20,传输数据,只有在数据传输时才开启,传输结束之后关闭

from ftplib import FTP
import socket
from typing import final


# 基础-1:连接和登录服务器
def ftp_connect_demo():
    # 创建FTP连接对象
    ftp = FTP()
    try:
        # 获取本地IP地址
        local_ip = socket.gethostbyname(socket.gethostname())
        print(f"[local_ip]:{local_ip}")
        # 连接
        ftp.connect(local_ip, 2121, timeout=10)
        print(f"成功连接FTP服务器:{local_ip}:2121")
        # 登录
        user, password = "testuser", "testpass"
        # 匿名登录:ftp.login()
        ftp.login(user, password)
        print(f"{user}已经成功登录到FTP服务器")
        # 获取欢迎信息
        welcome_msg = ftp.getwelcome()
        print(f"=== welcome message ===\n{welcome_msg}")
        # 获取当前用户的登录的目录
        current_dir = ftp.pwd()
        print(f"[工作目录]:{current_dir}")
    except Exception as e:
        print(f"[Error]:{e}")
    finally:
        if "ftp" in locals() and ftp.sock:
            ftp.quit()
            print("已经成功退出FTP连接")


if __name__ == "__main__":
    ftp_connect_demo()
