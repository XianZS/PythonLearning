import urllib.request
import http.cookiejar

# 进阶-2：cookie处理
# httpcookieprocesser 和 http.cookiejar

# 第一步-创建cookie管理器
cookie_jar = http.cookiejar.CookieJar()
cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
opener = urllib.request.build_opener(cookie_handler)
# 将自定义opener设置为全局opener
urllib.request.install_opener(opener)
# 第二步-第一次请求，设置cookie
res = urllib.request.urlopen(
    "https://httpbin.org/cookies/set?name=admin&value=123&password=admin123"
)
print("第一次请求之后的cookie:")
for cookie in cookie_jar:
    print(f"{cookie.name}={cookie.value}")
# 第三步-第二次请求，查询cookie
res = urllib.request.urlopen("https://httpbin.org/cookies")
print(f"第二次请求响应:\n{res.read().decode('utf-8')}")
# 第四步-将cookie保存到文件之中
# 文件型cookie管理器
cookie_jar_file = http.cookiejar.MozillaCookieJar("cookies.txt")
for c in cookie_jar:
    cookie_jar_file.set_cookie(c)
# 保存到文件之中
cookie_jar_file.save(ignore_discard=True, ignore_expires=True)
# 第五步-从文件之中加载cookie
loaded_cookie_jar = http.cookiejar.MozillaCookieJar()
loaded_cookie_jar.load("./cookies.txt", ignore_discard=True, ignore_expires=True)
print("从文件加载的cookie为:")
for cookie in loaded_cookie_jar:
    print(f"{cookie.name}={cookie.value}")
