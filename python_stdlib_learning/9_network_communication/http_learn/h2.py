import http.client
import socket

# HTTP client 高级用法
# 持久连接
conn = http.client.HTTPSConnection("httpbin.org")
try:
    # 第一次请求
    conn.request("GET", "/get?request=1")
    response_1 = conn.getresponse()
    print(f"[response_1 status code]:{response_1.status}")
    response_1.read()
    # 第二次请求
    conn.request("GET", "/get?request=2")
    response_2 = conn.getresponse()
    print(f"[response_2 status code]:{response_2.status}")
    response_2.read()
    # 查看TCP连接状态
    print(f"[连接状态]:{conn.sock}")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    conn.close()
    print(f"[连接状态]:{conn.sock}")
# 分块传输编码处理
# Transfer-Encoding:chunked
conn = http.client.HTTPSConnection("httpbin.org")
try:
    # 这个端点会返回分块数据
    conn.request("GET", "/stream/3")
    response = conn.getresponse()
    print(f"[status code]:{response.status}")
    print(f"[是否分块传输]:{response.chunked}")
    while True:
        chunk = response.read(1024)
        if not chunk:
            break
        print(f"[收到块]:{chunk.decode('utf-8').strip()}")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    conn.close()
print("-" * 10)
# 异常处理
# http.client 有许多异常类，用来处理不同的异常错误。
try:
    conn = http.client.HTTPSConnection("httpbin.org", timeout=5)
    conn.request("GET", "/")
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    print(f"[status code]:{response.status}")
    # print(f"[data]:{data}")
except socket.gaierror:
    print("域名错误")
except http.client.InvalidURL:
    print("URL错误")
except http.client.HTTPException as e:
    print("HTTP 协议错误")
except socket.timeout:
    print("超时错误")
except ConnectionRefusedError:
    print("连接拒绝访问")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    try:
        conn.close()
    except:
        pass
