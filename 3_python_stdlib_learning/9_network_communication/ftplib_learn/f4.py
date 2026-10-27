# 进阶-4:错误处理的完善和异常捕捉
# error_reply 服务器返回了意外的响应代码
from ftplib import FTP, error_reply, error_temp, error_perm, error_proto, all_errors
import socket
import os
import time


def ftp_err_demo():
    ftp = FTP()
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        ftp.connect(local_ip, 2121, timeout=10)
        ftp.login("testuser", "testpass")
        print("成功登录")
        try:
            ftp.cwd("non_exists_dir")
        except error_perm as e:
            print(f"进入不存在的目录:{e}")
        try:
            ftp.delete("non_exists_file")
        except error_perm as e:
            print(f"删除不存在的文件:{e}")
        # 超时连接
        ftp2 = FTP()
        try:
            ftp2.connect("192.168.255.255", 21, timeout=3)
            ftp2.login()
        except socket.timeout:
            print("超时连接")
        except socket.error as e:
            print(f"[Error]:{e}")
        finally:
            ftp2.quit()
    except Exception as e:
        print(f"[Error]:{e}")


if __name__ == "__main__":
    ftp_err_demo()
