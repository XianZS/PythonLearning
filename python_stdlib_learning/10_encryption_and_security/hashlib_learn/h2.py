# 基础-2：不同hash算法的使用
import hashlib

data = "测试不同hash算法的使用".encode("utf-8")

# 常见算法
algorithms = ["md5", "sha1", "sha256", "sha512", "blake2b"]
for algo in algorithms:
    # 创建hash对象
    # 语法规范：hashlib.new(hash算法)
    hash_obj = hashlib.new(algo)
    hash_obj.update(data)
    hash_hex = hash_obj.hexdigest()
    print(f"[algo.upper]:{algo.upper()}")
    print(f"[哈希值]:{hash_hex}")
    print(f"[长度]:{len(hash_hex)}字符;[字节]:{len(hash_hex) // 2}字节")

print(f"所有可用算法:\n{hashlib.algorithms_available}")
print(f"肯定支持算法:\n{hashlib.algorithms_guaranteed}")
