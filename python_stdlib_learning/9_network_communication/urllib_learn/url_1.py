import urllib.request

# 进阶-1：自定义opener和handler
# urlopen调用opener，opener底层使用handler
http_handler = urllib.request.HTTPHandler(debuglevel=1)
https_handler = urllib.request.HTTPSHandler(debuglevel=1)
# 创建自定义opener对象
opener = urllib.request.build_opener(http_handler, https_handler)
# 使用自定义opener发送请求
res = opener.open("https://www.baidu.com")
print(f"[响应状态码]:{res.getcode()}")
