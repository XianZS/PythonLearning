# 进阶-4：hash值的安全比较
import hashlib
import secrets
import time


def unsafe_compare(a, b):
    return a == b


def safe_compare(a, b):
    # 主要体现在，可以抵抗时序攻击
    return secrets.compare_digest(a, b)


if __name__ == "__main__":
    hash1 = hashlib.sha256(b"test1").hexdigest()
    hash2 = hashlib.sha256(b"test2").hexdigest()
    print(f"哈希数值1：{hash1}")
    print(f"哈希数值2：{hash2}")
    # 测试不安全比较的时间
    start_time = time.time()
    for _ in range(100000):
        unsafe_compare(hash1, hash2)
    spend_unsafe_time = time.time() - start_time
    start_time = time.time()
    for _ in range(100000):
        safe_compare(hash1, hash2)
    spend_safe_time = time.time() - start_time
    print(f"[unsafe time]:{spend_unsafe_time}")
    print(f"[safe time]:{spend_safe_time}")
