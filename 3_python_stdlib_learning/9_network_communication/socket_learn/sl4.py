# 进阶-3：非阻塞式socket和IO多路复用
import socket
import selectors

# 创建selector对象
sel = selectors.DefaultSelector()


def accept(sock, mask):
    """处理新连接"""
    conn, addr = sock.accept()
    print(f"新客户端接入:{addr}")
    # 设置非阻塞式
    conn.setblocking(False)
    # 注册事件
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    """处理客户端数据"""
    try:
        data = conn.recv(1024)
        if data:
            print(f"接收到数据:{data.decode('utf-8')}")
            conn.send("数据回显")
        else:
            print("客户端关闭连接")
            sel.unregister(conn)
            conn.close()
    except ConnectionResetError:
        print("客户端强制断开连接")
        sel.unregister(conn)
        conn.close()


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", 12345))
    server_sock.listen(10)
    server_sock.setblocking(False)
    # 注册服务器套接字的读事件 read()
    sel.register(server_sock, selectors.EVENT_READ, accept)
    print("已经成功启动了IO多路复用TCP服务器")
    try:
        while True:
            # 等待事件的发生
            events = sel.select(timeout=None)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except Exception as e:
        print(f"[Error]:{e}")
    finally:
        sel.close()
        server_sock.close()


if __name__ == "__main__":
    main()
