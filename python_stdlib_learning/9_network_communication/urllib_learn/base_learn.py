"""
URL library 标准库学习
"""

import urllib.request
import urllib.parse
import urllib.error
import urllib.robotparser

# 基础-1：发送GET请求
# 语法规范：urllib.request.urlopen() 发送响应
res_get = urllib.request.urlopen("http://www.baidu.com")
# 读取响应内容 read() 方法
html_obj = res_get.read()
print(f"[html_obj]:\n>>>\n{html_obj}")
# 解析成字符串 decode() 方法
html_str = html_obj.decode("utf-8")
print(f"[字符串解析之后的结果]:\n{html_str}")
# 获取响应状态码
print(f"[响应状态码]:{res_get.getcode()}")
print(f"[实际访问的url]:{res_get.geturl()}")
print(f"[响应头信息]:{res_get.info()}")
print(f"[网页的前100个字符]:{html_str[:100]}")
print("-" * 10)
# 基础-2：处理编码与解码
# 以ASCII字符为标准
params = {"wd": "Python 3.14 最新教程", "ie": "utf-8", "tn": "baidu"}
strs_paras = urllib.parse.urlencode(params)
print(f"[strs_paras]:{strs_paras}")
# [strs_paras]:wd=Python+3.14+%E6%9C%80%E6%96%B0%E6%95%99%E7%A8%8B&ie=utf-8&tn=baidu
# 构造完整的url
base_url = "http://www.baidu.com/s"
full_url = f"{base_url}?{strs_paras}"
print(f"[完整URL]:{full_url}")
# 解析url
url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%E6%97%B6%E9%97%B4&oq=Python%2520%2526lt%253B.14%2520%25E6%259C%2580%25E6%2596%25B0%25E6%2595%2599%25E7%25A8%258B&rsv_pq=ed087d26038d6899&rsv_t=d057%2BBIHRNdRqkCnN0pZhTjytn%2BgJM8xSSGNFEb4Tl2lKHX3p%2F3icCfe%2F8Q&rqlang=cn&rsv_dl=tb_enter&rsv_enter=1&rsv_sug3=12&rsv_sug1=4&rsv_sug7=100&rsv_btype=t&inputT=970&rsv_sug4=970&rsv_sug=1"
parsed = urllib.parse.urlparse(url)
print("URL解析结果为:")
print(f"协议:{parsed.scheme}")
print(f"域名:{parsed.netloc}")
print(f"路径:{parsed.path}")
print(f"查询参数:{parsed.query}")
print(f"片段:{parsed.fragment}")
print("-" * 10)

# 基础-3：发送POST请求
data = {"username": "testuser", "password": "1234567890", "remember": "True"}
# 编码POST数据
encode_data = urllib.parse.urlencode(data).encode("utf-8")
print(f"[POST数据编码结果]:{encode_data}")
# 发送POST请求
url = "https://httpbin.org/post"
res = urllib.request.urlopen(url, data=encode_data)
# 读取响应内容
res_data = res.read().decode("utf-8")
print(f"[POST请求返回结果]:{res_data}")
print("-" * 10)
# 基础-4：添加请求头
# 很多网站会检查请求头之中的user-agent字段
url = "https://httpbin.org/headers"
headers = {
    "User-Agent": "Mozilla/5.0 (WindowsNT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
}
req = urllib.request.Request(url, headers=headers)
res = urllib.request.urlopen(req)
res_data = res.read().decode("utf-8")
print(f"自定义请求头响应:{res_data}")
print("-" * 10)
# 基础-5：异常处理
url = "https://www.nonexistent-website-example.com"
try:
    res = urllib.request.urlopen(url, timeout=5)
    print(f"响应状态码:{res.getcode()}")
except urllib.error.HTTPError as e:
    print(f"[Error]:{e},[Reason]:{e.reason}")
    print(f"错误响应头:{e.headers}")
except TimeoutError:
    print("请求超时")
except Exception as e:
    print(f"其它错误:{e}")
print("-" * 10)
# 基础-6：解析安全文件
# 创建解析对象
rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://www.baidu.com/robots.txt")
# 读取并且解析文件
rp.read()
# 检查某个URL是否允许被爬取
user_agent = "*"
urls = ["/", "/s?wd=python", "/baidu.html", "/search/"]
for url in urls:
    allowed = rp.can_fetch(user_agent, url)
    print(f"爬取{url}：{'允许' if allowed else '禁止'}")
