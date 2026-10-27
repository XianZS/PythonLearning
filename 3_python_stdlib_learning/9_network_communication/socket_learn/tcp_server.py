"""
tcp 服务端
"""

import socket

# 创建套接字
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 端口复用
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定地址和端口
server_sock.bind(("0.0.0.0", 12345))

# 开始监听
server_sock.listen(5)
print("TCP服务器已经成功启动")

# 接收客户端的链接（阻塞等待的过程）
client_sock, client_addr = server_sock.accept()
print(f"[client_sock]:{client_sock};[client_addr]:{client_addr}")

# 数据收发
try:
    # 接收数据
    # 语法规范:已经的客户端对象.recv(缓冲区大小)
    data = client_sock.recv(1024)
    if data:
        print(f"[收到数据]:{data.decode('utf-8')}")
        client_sock.send("服务器收到数据".encode("utf-8"))
    else:
        print("客户端没有发送数据")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    client_sock.close()
    server_sock.close()
