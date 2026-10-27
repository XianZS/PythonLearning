"""
服务端：
server-udp 交流实现
"""

import socket

# 创建服务端对象
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 服务端必须要绑定端口号
server.bind(("0.0.0.0", 55555))

print("[server info]:服务端已经成功绑定端口号")


# tcp:建立连接的通信，意味着：必须要知道客户端对象是什么？
# 如何发送的数据？ 客户端对象.send(send_data)
# [tcp]:server.recv() ===>>> 客户端对象,客户端IP地址
# udp:不建立连接的通信，意味着：我不需要知道客户端对象是什么？
# 如何发送的数据？ 客户端IP地址来进行传输数据
# [udp]:server.recvfrom() ===>>> 客户端发送的数据,客户端IP地址
# IPV4 32位 每8二进制数位为一个数
# 192.168.8.1

rf_data, rd_address = server.recvfrom(1024)

print("=== 服务端接收数据 ===")
print(rf_data.decode("utf-8"))
print(rd_address)
print("===" * 3)

print("=== 服务端发送数据 ===")
send_data_from_server = "[UDP]服务端 >>> 客户端".encode("utf-8")
server.sendto(send_data_from_server, rd_address)
print("===" * 3)


if __name__ == "__main__":
    pass
