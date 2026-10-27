"""
客户端
client-udp 交流实现
"""

import socket

# 创建udp通信之中的客户端对象
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 不需要使用connet()方法

print("=== 客户端发送数据 ===")
send_data = "[UDP]客户端 >>> 服务端".encode("utf-8")

# [UDP] 模拟客户端向IP为127.0.0.1:55555的IP发送数据
client.sendto(send_data, ("127.0.0.1", 55555))
print("===" * 3)

print("=== 客户端接收数据 ===")
rf_data, rd_address = client.recvfrom(1024)
print(rf_data.decode("utf-8"))
print(rd_address)
print("===" * 3)

if __name__ == "__main__":
    pass
