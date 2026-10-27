# 模拟本地FTP服务器的实现
from threading import local
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import socket


def get_local_ip():
    # 获取本地局域网给我当前主机分配的IP地址
    try:
        # socket-udp套接字获取详细的外部地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"[Error]:{e}")


def run_ftp_server():
    # 将本地的某个文件夹模拟为FTP服务器的根目录
    ftp_root = os.path.join(os.getcwd(), "ftp_root")
    if not os.path.exists(ftp_root):
        os.makedirs(ftp_root)
        print("FTP根目录已经成功被创建")
    else:
        print("FTP根目录存在,不用被创建")
    print("=== start run ===")
    # 创建匿名用户目录
    anonymous_dir = os.path.join(ftp_root, "anonymous")
    if not os.path.exists(anonymous_dir):
        os.makedirs(anonymous_dir)
    # 创建用户授权器
    my_authorizer = DummyAuthorizer()
    # 添加用户
    # 参数:(用户名,密码,目录,权限)
    # e 更改目录 l 列出文件 r 下载 a 追加 d 删除 f 重命名 m 创建目录 w 上传
    my_authorizer.add_user("testuser", "testpass", ftp_root, perm="elradfmw")
    # 添加匿名用户-只读权限
    my_authorizer.add_anonymous(anonymous_dir, perm="elr")
    # 创建FTP处理器
    handler = FTPHandler
    handler.authorizer = my_authorizer
    # 设置欢迎信息
    handler.banner = "欢迎使用本地FTP服务器测试"
    # 启动
    local_ip = get_local_ip()
    server_obj = FTPServer((local_ip, 2121), handler)
    print(f"FTP服务器已经成功启动,ip:{local_ip}")
    print(f"FTP根目录:{ftp_root}")
    try:
        # 启动服务器-阻塞式启动
        server_obj.serve_forever()
    except KeyboardInterrupt:
        print("手动暂停,FTP服务器运行结束")
    except Exception as e:
        print(f"[Error]:{e}")
    finally:
        server_obj.close()


if __name__ == "__main__":
    run_ftp_server()
