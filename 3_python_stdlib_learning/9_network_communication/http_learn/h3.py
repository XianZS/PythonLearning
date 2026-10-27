import http.client
import http.cookiejar
import urllib.request

# 进阶-2：cookie管理
# 创建cookie管理器
cookie_jar = http.cookiejar.CookieJar()
# 创建请求对象
req = urllib.request.Request("https://httpbin.org/cookies/set?name=python&version=3.14")
# 创建连接对象
conn = http.client.HTTPSConnection("httpbin.org")
# 尝试开始请求
try:
    # 设置cookie
    conn.request("GET", req.full_url)
    resp = conn.getresponse()
    resp.read()
    # 提取cookie，从cookiejar里面提取cookie
    # cookie_jar.extract_cookies(响应对象response，请求对象request)
    cookie_jar.extract_cookies(resp, req)
    print("打印cookie:")
    for c in cookie_jar:
        print(f"[{c.name}]={c.value}")
    # 根据cookiejar再次发送请求
    cookie_list = [f"{c.name}={c.value}" for c in cookie_jar]
    cookie_header = ";".join(cookie_list)
    # 创建header
    headers = {"Host": "httpbin.org", "Cookie": cookie_header}
    # 发送请求
    conn.request("GET", "/cookies", headers=headers)
    resp2 = conn.getresponse()
    print(f"返回结果>>>{resp2.read().decode('utf-8')}")
except Exception as e:
    print(e)
finally:
    conn.close()
