"""
requests
"""

import requests
from requests.exceptions import RequestsDependencyWarning

url = "https://httpbin.org"
params = {"user": "admin", "password": "admin123"}
headers = {"User-Agent": "Python/3.14"}

# [get] >>> https://httpbin.org/get
res_get = requests.get(url=url + "/get", params=params, headers=headers)
print(res_get, type(res_get))
text_html = res_get.text
print(f"[text]:{text_html}")
headers = res_get.headers
print(f"[headers]:{headers}")
res_json = res_get.json()
print(f"[json]:{res_json}")
baidu = requests.get("https://www.baidu.com/").text
# print(baidu)


# [post] >>> https://httpbin.org/post
res_post = requests.post(url=url + "/post")
print(f"[post]:{res_post.status_code},{res_post.url}")

# [delete] >>> https://httpbin.org/delete
res_delete = requests.delete(url=url + "/delete")
print(res_delete)

# [put] >>> https://httpbin.org/put
res_put = requests.put(url=url + "/put")
print(res_put)


if __name__ == "__main__":
    pass
