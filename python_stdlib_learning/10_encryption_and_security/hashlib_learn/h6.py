# 进阶-2：可更新的hash对象
import hashlib

datas = ["Hello, ", "I ", "am ", "jom"]
strs = "Hello, I am jom"
h1 = hashlib.sha256()
h2 = hashlib.sha256()
for data in datas:
    h1.update(data.encode("utf-8"))
h2.update(strs.encode("utf-8"))
res1 = h1.hexdigest()
res2 = h2.hexdigest()
print(f"[res1]:{res1}")
print(f"[res2]:{res2}")
