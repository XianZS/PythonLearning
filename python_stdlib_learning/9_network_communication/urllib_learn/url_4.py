# 进阶-4：HTTP认证
import urllib.request
import urllib.error

# 第一步：设置认证信息
username = "admin"
password = "secret"
url = "https://httpbin.org/basic-auth/admin/secret"
# 第二步：创建密码管理器
password_mag = urllib.request.HTTPPasswordMgrWithDefaultRealm()
# 添加认证信息
password_mag.add_password(None, url, username, password)
# 第三步：创建基本认证处理器
auth_handler = urllib.request.HTTPBasicAuthHandler(password_mag)
# 第四步：创建opener对象
opener = urllib.request.build_opener(auth_handler)
# 第五步：尝试运行
try:
    response = opener.open(url)
    print(f"认证成功，响应内容:{response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    if e.code == 401:
        print("认证失败，账号或者密码错误")
    else:
        print("HTTP错误")
