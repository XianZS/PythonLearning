# udp 通信 服务端
import socket

# 创建udp套接字
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定udp地址和端口
server_sock.bind(("0.0.0.0", 12345))
print("UDP服务端成功启动")

# 接收数据
data, client_addr = server_sock.recvfrom(1024)
print(f"收到了来自{client_addr}的数据:（{data.decode('utf-8')}）")

# 向客户端发送响应
server_sock.sendto("你好。UDP用户".encode("utf-8"), client_addr)
server_sock.close()
