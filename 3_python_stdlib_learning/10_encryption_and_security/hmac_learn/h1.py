# 基础-1：HMAC基础使用
import hmac
import hashlib

secret_key = "my_secret_key_123".encode("utf-8")
data = "HMAC数据".encode("utf-8")
hmac_obj = hmac.new(secret_key, data, hashlib.sha256)
res = hmac_obj.hexdigest()
print(f"[密钥]:{secret_key}")
print(f"[原数据]:{data}")
print(f"[HMAC]:{res}")

# 基础-2：不同算法的支持
algs = ["md5", "sha1", "sha256", "sha512", "blake2b"]
for alg in algs:
    hmac_obj = hmac.new(secret_key, data, alg)
    hmac_hex = hmac_obj.hexdigest()
    print(f"[hmac_hex]:{hmac_hex}")

# 基础-3：可更新的hmac对象
hmac1 = hmac.new(secret_key, digestmod=hashlib.sha256)
datas = ["Hello, ", "World."]
strs = "Hello, World."
for data in datas:
    hmac1.update(data.encode("utf-8"))
res1 = hmac1.hexdigest()
hmac2 = hmac.new(secret_key, digestmod=hashlib.sha256)
hmac2.update(strs.encode("utf-8"))
res2 = hmac2.hexdigest()
print(f"[res1]:{res1}")
print(f"[res2]:{res2}")


# 基础-4：安全比较
# 时序攻击
def unsafe_compare(a, b):
    return a == b


def safe_compare(a, b):
    return hmac.compare_digest(a, b)


unsafe_res = unsafe_compare(res1, res2)
safe_res = safe_compare(res1, res2)
print(f"[unsafe_compare]:{unsafe_res}")
print(f"[safe_res]:{safe_res}")
