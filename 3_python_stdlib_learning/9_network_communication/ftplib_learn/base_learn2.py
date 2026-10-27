# 基础-2:目录操作
# pwd() 获取当前工作目录
# cwd(path) 更改当前工作目录,将当前工作目录改为path
# mkd(path) 创建新目录
# rmd(path) 删除目录
# dir() 列出当前目录的详细信息
# nlst() 列出当前目录的文件名列表
from ftplib import FTP, error_perm
import socket
from typing_extensions import Dict


def ftp_directory_demo():
    ftp = FTP()

    def directory_exists(ftp, path):
        # 检查远程目录是否存在
        try:
            original_dir = ftp.pwd()
            ftp.cwd(path)
            ftp.cwd(original_dir)
            return True
        except Exception as e:
            print(f"[Error]:{e}")
            return False

    def safe_mkd(ftp, path):
        # 安全创建目录
        if not directory_exists(ftp, path):
            ftp.mkd(path)
            print(f"创建成功,创建对象为:{path}")
        else:
            print(f"目录{path}已经存在,不需要创建")

    def safe_rmd(ftp, path):
        # 安全的删除目录
        if directory_exists(ftp, path):
            ftp.rmd(path)
            print(f"目录{path}删除成功")
        else:
            print(f"目录{path}不存在,删除失败")

    try:
        # 尝试连接并且登录
        local_ip = socket.gethostbyname(socket.gethostname())
        ftp.connect(local_ip, 2121, timeout=10)
        ftp.login("testuser", "testpass")
        print("登录成功")
        # 获取当前目录
        current_dir = ftp.pwd()
        print(f"[当前目录]:{current_dir}")
        # 创建目录的测试
        dir1, dir2, dir3 = "documents", "documents/reports", "images"
        safe_mkd(ftp, dir1)
        safe_mkd(ftp, dir2)
        safe_mkd(ftp, dir3)
        # 更改工作目录
        ftp.cwd(dir2)
        print(f"更改工作目录到:{ftp.pwd()}")
        # 返回上级目录
        ftp.cwd("..")
        print(f"返回上级目录:{ftp.pwd()}")
        # 所有的目录详细信息
        print(f"[目录详细信息]:{ftp.dir()}")
        # 列出所有的文件名列表
        file_list = ftp.nlst()
        print(f"[文件名列表]:{file_list}")
        # 删除目录
        ftp.cwd("/")
        safe_rmd(ftp, dir2)
        print(f"[删除之后]:{ftp.dir()}")
    except Exception as e:
        print(f"[Error]:{e}")
        if "ftp" in locals() and ftp.sock:
            print(f"当前报错目录:{ftp.pwd()}")
        else:
            pass
    finally:
        ftp.quit()
        print("FTP连接已经成功关闭")


if __name__ == "__main__":
    ftp_directory_demo()
