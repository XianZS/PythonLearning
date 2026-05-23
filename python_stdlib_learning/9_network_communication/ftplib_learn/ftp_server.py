from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import socket


def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        # 创建UDP套接字连接到外部地址（不会实际发送数据）
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"


def run_ftp_server():
    # 创建FTP根目录
    ftp_root = os.path.join(os.getcwd(), "ftp_root")
    if not os.path.exists(ftp_root):
        os.makedirs(ftp_root)
        print(f"创建FTP根目录: {ftp_root}")

    # 创建匿名用户目录
    anonymous_dir = os.path.join(ftp_root, "anonymous")
    if not os.path.exists(anonymous_dir):
        os.makedirs(anonymous_dir)

    # 创建用户授权器
    authorizer = DummyAuthorizer()

    # 添加普通用户（完整权限）
    # 权限说明：e-更改目录 l-列出文件 r-下载 a-追加 d-删除 f-重命名 m-创建目录 w-上传
    authorizer.add_user("testuser", "testpass", ftp_root, perm="elradfmw")

    # 添加匿名用户（只读权限）
    authorizer.add_anonymous(anonymous_dir, perm="elr")

    # 创建FTP处理器
    handler = FTPHandler
    handler.authorizer = authorizer

    # 设置欢迎信息
    handler.banner = "欢迎使用本地测试FTP服务器 - Powered by pyftpdlib"

    # 启动服务器
    local_ip = get_local_ip()
    server = FTPServer((local_ip, 2121), handler)

    print(f"\nFTP服务器已成功启动")
    print(f"服务器地址: {local_ip}:2121")
    print(f"普通用户: 用户名=testuser, 密码=testpass (完整权限)")
    print(f"匿名用户: 无需密码 (只读权限)")
    print(f"FTP根目录: {ftp_root}")
    print("按 Ctrl+C 停止服务器\n")

    # 启动服务器（阻塞式）
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nFTP服务器已停止")
        server.close()


if __name__ == "__main__":
    run_ftp_server()
