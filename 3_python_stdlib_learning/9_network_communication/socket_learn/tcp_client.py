# 客户端
import socket

# 创建客户端套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 连接服务器
    client_socket.connect(("127.0.0.1", 12345))
    # 发送数据
    client_socket.send("---你好，我是客户端---".encode("utf-8"))
    # 接收响应
    res = client_socket.recv(1024)
    print(f"服务端返回的内容:{res.decode('utf-8')}")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    client_socket.close()
