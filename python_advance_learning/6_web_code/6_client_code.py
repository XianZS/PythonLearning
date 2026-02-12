"""
客户端
"""

# （第二步）客户端请求建立连接
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 55555))
print("客户端加载成功")
# 体现出：
#   只有先启动服务端，客户端才能成功响应

# （第三步）客户端向服务端发送数据
# 泛用方法:send()
# 泛用方法:recv()
try:
    send_data = "客户端向服务端发送数据".encode("utf-8")
    print(send_data)
    client.send(send_data)

    # （第六步）客户端接收服务端发送的数据
    res_data = client.recv(1024).decode("utf-8")
    print(res_data)
except Exception as e:
    print(e)
