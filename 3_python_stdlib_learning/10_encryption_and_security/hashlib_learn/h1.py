# 基础-1：字符串的hash
import hashlib

data = "我现在正在测试Python里面的hash标准库，我使用的是SHA-256算法。"
# SHA-256算法
hash_obj = hashlib.sha256()

# 向hash对象之中输入数据
hash_obj.update(data.encode("utf-8"))

# 获取16进制的HASH值
hash_hex = hash_obj.hexdigest()
print(f"[原始数据]:{data}")
print(f"[加密数据]:{hash_hex}")
# [原始数据]:我现在正在测试Python里面的hash标准库，我使用的是SHA-256算法。
# [加密数据]:5c0bc7c3c68fdc7575b03ea3a4a9baed42a207f6f1ac56aacfa6cfabf6d36df9
