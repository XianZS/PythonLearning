"""
服务端
"""

import socket

# （第一步）服务端监听接口

# socket.socket(连接方式-IPV4模式,数据编码模式-字节流模式)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 0~65535 但是一般情况下0不会被使用
server.bind(("0.0.0.0", 55555))

server.listen(5)

print("服务端加载成功……")


# 测试休眠-服务端持久化
# import time
# time.sleep(100)

# 服务端和客户端的数量
# 可能只存在一个服务端
# 但是可能存在多个用户端

# （第四步）服务端接收客户端发送的数据
try:
    # 该语句会阻塞当前进程，直到有来自客户端的请求到来
    client_socket_obj, client_address = server.accept()
    res_data = client_socket_obj.recv(1024).decode("utf-8")
    print(res_data)

    # （第五步）服务端向客户端发送的数据
    send_data = "服务端向客户端发送的数据".encode("utf-8")
    client_socket_obj.send(send_data)
except Exception as e:
    print(e)
