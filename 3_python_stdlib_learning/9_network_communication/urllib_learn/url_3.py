import urllib.request

# 进阶-3：代理设置
# ProxyHandler
# 代理选项：http https
# 第一步：设置代理服务器地址
proxy_handler = urllib.request.ProxyHandler(
    {"http": "http://127.0.0.1:12345", "https": "https://127.0.0.1:12345"}
)
# 第二步：创建包含代理服务器的opener对象
opener = urllib.request.build_opener(proxy_handler)
# 第三步：通过代理来发送请求
try:
    response = opener.open("https://httpbin.org/ip", timeout=10)
    print(f"代理IP:{response.read().decode('utf-8')}")
except Exception as e:
    print(f"[Error]:{e}")
