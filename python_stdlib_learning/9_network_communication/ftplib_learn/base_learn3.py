# 基础-3:文件上传和文件下载
# 上传文件:
# storlines(cmd,fp):以ascii格式上传文件
# storbinary(cmd,fp,blocksize=8192):以二进制形式上传文件
# 下载文件:
# retlines(cmd,callback=None)
# retrbinary(cmd,callback,blocksize=8192)
# cmd 参数是FTP命令
from ftplib import FTP
import socket
import os
from typing import final


def ftp_file_transfera_demo():
    ftp = FTP()
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        ftp.connect(local_ip, 2121, timeout=10)
        ftp.login("testuser", "testpass")
        # 上传 base_learn.py 文件
        text_file = "test_text.txt"
        binary_file = "test_binary.png"
        # 写入文件测试
        with open(text_file, "w", encoding="utf-8") as f:
            f.write("这是一个测试文件\n")
            f.write("这是第二行\n")
            f.write("这是第三行")
        png_data = b"\x89PNG\r\n\x1a"
        with open(binary_file, "wb") as f:
            f.write(png_data)
        print("本地测试文件创建成功")
        # 以二进制形式上传文本文件
        with open(text_file, "rb") as f:
            ftp.storbinary(f"STOR {text_file}", f)
        # 以二进制形式上传二进制文件
        with open(binary_file, "rb") as f:
            ftp.storbinary(f"STOR {binary_file}", f)
        # 通过FTP.dir()来确保成功上传
        ftp.dir()
        # 以二进制形式进行下载文件
        download_text = "download_text.txt"
        with open(download_text, "wb") as f:
            ftp.retrbinary(f"RETR {text_file}", f.write)
        # 以二进制形式下载二进制文件
        download_binary = "download_binary.png"
        with open(download_binary, "wb") as f:
            ftp.retrbinary(f"RETR {binary_file}", f.write)
    except Exception as e:
        print(f"[Error]:{e}")
    finally:
        ftp.quit()


if __name__ == "__main__":
    ftp_file_transfera_demo()
