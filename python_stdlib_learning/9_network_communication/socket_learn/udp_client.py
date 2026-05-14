# UDP 客户端
import socket

# 创建套接字
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送数据
client_sock.sendto("你好服务端，我是UDP客户端！".encode("utf-8"), ("127.0.0.1", 12345))

# 接收响应
data, server_addr = client_sock.recvfrom(1024)
print(f"[客户端]:{data.decode('utf-8')}")

# 关闭连接对象
client_sock.close()
