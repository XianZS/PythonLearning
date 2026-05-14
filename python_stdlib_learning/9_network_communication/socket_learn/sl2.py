# 进阶-1：多客户端TCP服务器
import socket
import threading


def handle_client(client_sock, client_addr):
    """
    处理单个客户端的通信
    """
    print(f"新客户端链接:{client_addr}")
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print(f"[客户端——>服务端]:{data.decode('utf-8')}")
            client_sock.send("服务端响应的数据".encode("utf-8"))

    except Exception as e:
        print(f"[Error]:{e}")
    finally:
        client_sock.close()


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", 12345))
    server_sock.listen(10)
    print("多线程TCP服务器已经启动")
    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            # 创建新线程来处理客户端
            thread = threading.Thread(
                target=handle_client, args=(client_sock, client_addr)
            )
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("手动中止 ...")
    finally:
        server_sock.close()


if __name__ == "__main__":
    main()
