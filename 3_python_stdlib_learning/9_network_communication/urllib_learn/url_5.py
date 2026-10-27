import urllib.request
import ssl

# 进阶-5：HTTPS证书验证
# 第一步：验证证书
# try:
#     res = urllib.request.urlopen("https://expired.badssl.com")
#     print("证书验证成功")
# except ssl.SSLError as e:
#     print(f"证书验证失败:{e}")

# 第二步：关闭证书验证
context = ssl._create_unverified_context()
try:
    res = urllib.request.urlopen("https://expired.badssl.com", context=context)
    print("取消证书验证成功")
except ssl.SSLError as e:
    print(f"证书验证失败:{e}")
