"""
socket 编程学习
"""

import socket

# 基础-1：socket简单实用
# 套接字编程
# TCP套接字 UDP套接字
# socket.socket(IPV4/IPV6,TCP/UDP)
# TCP-IPV4
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# UDP-IPV4
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# TCP-IPV6
tcp_sock6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
print(f"[socket]:{tcp_sock}")
print(f"[socket]:{udp_sock}")
print(f"[socket]:{tcp_sock6}")

# 基础-2：TCP通信基础

# 基础-4：API速查表
# socket(family,type)
# bind((host,port))
# listen(number:int)
# accept()接收tcp链接，返回(client_sock,addr)
# connect((host,port))连接到TCP服务器
# recv(bufsize)接收TCP数据
# send(bytes)发送TCP数据
# recvfrom(bufsize)接收UDP数据
# sendto(bytes)发送UDP数据
# close()关闭套接字，释放资源
# getpeername()获取链接的远程地址
# getsockname()获取本地套接字地址
