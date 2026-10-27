# 进阶-3:大文件传输优化
from ftplib import FTP
import socket
import os
import time


def ftp_large_file_opt_demo():
    ftp = FTP()
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        ftp.connect(local_ip, 2121, timeout=60)
        ftp.login("testuser", "testpass")
        # 创建一个50MB左右的文件
        large_file = "50mb_file.bin"
        file_size = 50 * 1024 * 1024
        with open(large_file, "wb") as f:
            f.write(os.urandom(file_size))
        # 测试不同块的上传速率
        block_sizes = [8192, 65536, 262144, 1048576]
        upload_results = {}
        for block_size in block_sizes:
            start_time = time.time()
            with open(large_file, "rb") as f:
                ftp.storbinary(f"STOR {large_file}", f, blocksize=block_size)
                upload_time = time.time() - start_time
                upload_speed = file_size / upload_time / 1024 / 1024  # MB/s
                upload_results[block_size] = {
                    "time": upload_time,
                    "speed": upload_speed,
                }
                ftp.delete(large_file)
        print(upload_results)
    except Exception as e:
        print(f"[Error]:{e}")
    finally:
        ftp.quit()


if __name__ == "__main__":
    ftp_large_file_opt_demo()
