# 进阶-1:模式切换
# 主动连接/被动连接
# set_pasv(True) 被动模式(默认)
# set_pasv(False) 主动模式
from ftplib import FTP
import socket


def ftp_mode_demo():
    ftp = FTP()
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        ftp.connect(local_ip, 2121, timeout=10)
        ftp.login("testuser", "testpass")
        now_demo = ftp.passiveserver
        print(f"[当前模式]:{now_demo}")
        ftp.set_pasv(False)
        now_demo = ftp.passiveserver
        print(f"[当前模式]:{now_demo}")
    except Exception as e:
        print(f"[Error]:{e}")


if __name__ == "__main__":
    ftp_mode_demo()
