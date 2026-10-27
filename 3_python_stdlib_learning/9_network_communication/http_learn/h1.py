from http import HTTPStatus
import http.client
import http.cookies
import urllib.parse
import json
import http.server

# 基础-1：状态码
print(f"{HTTPStatus.OK}")
print(f"{HTTPStatus.NOT_FOUND.value}")
print(f"状态码短语:{HTTPStatus.NOT_FOUND.phrase}")
print(f"详细描述:{HTTPStatus.NOT_FOUND.description}")
status_obj = HTTPStatus(403)
print(f"{status_obj.name}")
# 基础-2：基础客户端
# 持久连接、分块传输、HTTPS特性
# （1）GET请求
conn = http.client.HTTPConnection("baidu.com", timeout=10)
try:
    conn.request("GET", "/")
    response = conn.getresponse()
    print(f"[status code]:{response.status};[reason]:{response.reason}")
    print("响应头:")
    for k, v in response.getheaders():
        print(f"{k}={v}")
    print("响应体:")
    body = response.read()
    print(f"响应体的长度:{len(body)}")
    print(f"解码:{body.decode('utf-8')}")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    conn.close()
print("-" * 10)
# （2）HTTPS请求
# http.client.HTTPSConnection()
# （3）带着请求头和查询参数的请求
params = urllib.parse.urlencode({"q": "python http client", "page": 1, "per_page": 10})
# 自定义请求头
headers = {
    "User-Agent": "Python http.client/3.14.0 (Learning Demo)",
    "Accept": "application/json",
}
conn = http.client.HTTPSConnection("httpbin.org")
try:
    conn.request("GET", f"/get?{params}", headers=headers)
    response = conn.getresponse()
    print(response.read().decode("utf-8"))
except Exception as e:
    print(f"[Error]:{e}")
finally:
    conn.close()
print("-" * 10)
# （4）POST请求与（json和表单数据）
conn = http.client.HTTPSConnection("httpbin.org")
try:
    json_data = {"name": "Python", "version": "3.14.0"}
    json_body = json.dumps(json_data)
    json_headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json_body)),
    }
    conn.request("POST", "/post", body=json_body, headers=json_headers)
    response = conn.getresponse()
    print(f"JSON POST:{response.read().decode('utf-8')}")
    print("-" * 10)
    form_data = urllib.parse.urlencode({"username": "admin", "password": "admin123"})
    form_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(form_data)),
    }
    conn.request("POST", "/POST", body=form_data, headers=form_headers)
    response = conn.getresponse()
    print(f"表单POST响应:{response.read().decode('utf-8')}")
except Exception as e:
    print(f"[Error]:{e}")
finally:
    conn.close()


# 基础-3：cookie解析与创建
# http.cookies.SimpleCookie 类
cookie = http.cookies.SimpleCookie()
cookie["user_id"] = "123456"
cookie["user_name"] = "python_learn"
cookie["user_id"]["expires"] = "19.5 2026"
cookie["user_id"]["path"] = "/"
# 输出cookie头
output = cookie.output()
print(f"[cookie out put]:{output}")
# 解析 cookie 头
cookie_header = "user_id=12345;username=python_learner;session_id=abcdef123456"
parsed_cookie = http.cookies.SimpleCookie(cookie_header)
print("解析之后的结果:")
for k, v in parsed_cookie.items():
    print(f"{k}={v}")


# 基础-4：快速搭建服务器
# http.server
# 简单web服务器的搭建
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    # 处理GET请求
    def do_get(self):
        # 设置响应状态码
        self.send_response(http.HTTPStatus.OK)
        # 设置响应头
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()  # 必须参数
        # 发送响应体
        response = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Python HTTP服务器</title>
        </head>
        <body>
            <h1>Hello from Python 3.14.0 http.server!</h1>
            <p>这是一个使用标准库搭建的简单Web服务器</p>
            <p>请求路径: {}</p>
        </body>
        </html>
        """.format(self.path)
        self.wfile.write(response.encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8000)
    # 创建服务器实例
    httpd = http.server.HTTPServer(server_address, MyRequestHandler)
    print("启动服务器:http://localhost:8000")
    try:
        httpd.serve_forever()
    except Exception as e:
        print(f"[Error]:{e}")
