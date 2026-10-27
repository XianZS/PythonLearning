# 基础-3：hash值的表示形式
# 十六进制表示形式 原始字节表示形式
import hashlib

data = "HASH值的不同表示形式".encode("utf-8")
hash_obj = hashlib.sha256()
hash_obj.update(data)
hex_res = hash_obj.hexdigest()
raw_res = hash_obj.digest()
print(f"[16进制表示]:{hex_res}")
print(f"[原始字节表示]:{raw_res}")
tran_res = raw_res.hex()
print(f"[16进制表示-转换之后]:{hex_res}")
