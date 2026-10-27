# 基础-4:文件管理操作
# 删除 重命名 文件大小 发送FTP命令
from ftplib import FTP
import socket


def ftp_file_mangager_demo():
    ftp = FTP()
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        ftp.connect(local_ip, 2121, timeout=10)
        ftp.login("testuser", "testpass")
        # 创建一个测试文件
        test_file = "orginal_file.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("这是一个测试文件")
        # 上传的FTP服务器之中
        with open(test_file, "rb") as f:
            ftp.storbinary(f"STOR {test_file}", f)
        # 获取文件大小
        file_size = ftp.size(test_file)
        print(f"[文件大小]:{file_size}")
        # 重命名操作
        new_name = "renamed_file.txt"
        ftp.rename(test_file, new_name)
        # 移动文件的位置
        target_dir = "archive"
        ftp.mkd(target_dir)
        ftp.rename(new_name, f"{target_dir}/{new_name}")
        # 验证文件的移动
        ftp.dir()
        # 验证文件的移动
        ftp.cwd(target_dir)
        print("-" * 10)
        ftp.dir()
    except Exception as e:
        print(f"[Error]:{e}")


if __name__ == "__main__":
    ftp_file_mangager_demo()
