# 进阶-2：选项与超时设置
# 语法规范：通过setsockopt()来精细化socket的行为
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 端口复用
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 端口重用
# linux 3.9+ python  3.12>
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # type: ignore
# 设置接收缓冲区大小
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 131415926)
# 设置发送缓冲区大小
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 555555)
# 语法规范，仅用nagle算法
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# 超时时间
s.settimeout(5.0)
# 获取socket选项
res = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
print(f"查看端口复用选项:{res}")
s.close()
