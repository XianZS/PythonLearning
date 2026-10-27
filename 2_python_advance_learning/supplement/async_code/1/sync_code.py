"""
sync 同步实现
"""

# 客户端发起请求 ——》 服务端接收请求 ——》 服务端处理请求

from time import sleep, time


def web_request_response(*args, **kwargs):
    print("=== 服务端处理请求 ===")
    print(f"[args]:{args}")
    print(f"[kwargs]:{kwargs}")
    sleep(3)


def web_request():
    # 实现服务端接收请求
    print("=== 客户端接收请求 ===")
    web_request_response()


def client():
    # 实现客户端发起请求
    begin_time = time()
    for _ in range(3):
        web_request()
    spend_time = time() - begin_time
    print(f"[同步]:{spend_time}")
    # [同步]:9.002230644226074


if __name__ == "__main__":
    client()
