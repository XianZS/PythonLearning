# 进阶-2:断点续传
# rest(offset) 来指定从文件的哪个偏移量开始传输
# 示例:从第三个偏移量处开始重新传输
from ftplib import FTP, error_temp
import socket
import os
import time


def ftp_resume_transfer_demo():
    ftp = FTP()
    try:
        # === 断点下载 ===
        local_ip = socket.gethostbyname(socket.gethostname())
        ftp.connect(local_ip, 2121, timeout=10)
        ftp.login("testuser", "testpass")
        # 创建一个测试文件
        large_file = "test_file.bin"
        # 基础单位:字节B,1MB=1024KB=1024*1024B
        file_size = 10 * 1024 * 1024
        with open(large_file, "wb") as f:
            f.write(os.urandom(file_size))
        # 上传文件到服务器之中
        with open(large_file, "rb") as f:
            ftp.storbinary(f"STOR {large_file}", f)
        # 模拟下载中断
        partial_file = "partial_file_download.bin"
        target_download_size = 3 * 1024 * 1024
        with open(partial_file, "wb") as f:

            def callback(data):
                nonlocal target_download_size
                if f.tell() > target_download_size:
                    return False
                f.write(data)
                return True

            try:
                ftp.retrbinary(f"RETR {large_file}", callback)
            except error_temp as e:
                print(f"[Error]:{e}")
            except Exception as e:
                print(f"[Error]:{e}")
        # 获取已经下载的大小
        actual_downloaded = os.path.getsize(partial_file)
        print(f"[已经下载的实际大小为]:{actual_downloaded}")
        start_time = time.time()
        # 开始断点续传
        with open(partial_file, "ab") as f:
            ftp.retrbinary(f"RETR {large_file}", f.write, rest=actual_downloaded)
        spend_time = time.time() - start_time
        print(f"[花费的时间]:{spend_time}")
        # 验证文件的完整性
        original_size = os.path.getsize(large_file)
        downloaded_size = os.path.getsize(partial_file)
        print(f"[原始文件的大小]:{original_size}")
        print(f"[下载文件的大小]:{downloaded_size}")
        if original_size == downloaded_size:
            print("文件完整性:100%")
        else:
            print("文件不完整")
        # === 断点上传 ===
        partial_upload = "partial_upload.bin"
        upload_file_size = 5 * 1024 * 1024
        with open(large_file, "rb") as f_in, open(partial_upload, "wb") as f_out:
            # 先读取5MB左右的数据到将要上传的文件之中
            f_out.write(f_in.read(upload_file_size))
        with open(partial_upload, "rb") as f:
            ftp.storbinary(f"STOR {large_file}_upload", f)
        with open(large_file, "rb") as f:
            # 移动文件指针
            # 初始化:文件指针在头部,需要将其移动到文件5MB左右处
            f.seek(upload_file_size)
            ftp.storbinary(f"STOR {large_file}_upload", f, rest=upload_file_size)
        # 验证文件的完整性
        uploaded_size = ftp.size(f"{large_file}_upload")
        print(f"[被上传的文件的大小]:{uploaded_size}")
        if original_size == uploaded_size:
            print("断点续传成功")
        else:
            print("断点续传失败")

    except Exception as e:
        print(f"[Error]:{e}")


if __name__ == "__main__":
    ftp_resume_transfer_demo()
