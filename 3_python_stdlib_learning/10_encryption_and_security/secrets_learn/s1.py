# 基础-1：环境准备和导入
import secrets
import string
import random

print("查看secrets模块所有可以使用的方法:")
for func in dir(secrets):
    if not func.startswith("_"):
        print(f"    - {func}")


# 基础-2：生成随机字节
# 默认32字节
default_bytes = secrets.token_bytes()
print(f"32字节的随机字节为:{default_bytes}")
custom_bytes = secrets.token_bytes(16)
print(f"16字节的随机字节为:{custom_bytes}")
# 生成64字节（512位=64*8位）的随机字节
high_bytes = secrets.token_bytes(64)
print(f"64字节的随机字节为:{high_bytes}")

# 基础-3：生成随机16进制字符串
# 每个字节8位，每个16进制数占4位，每个字节就相当于两个16进制数
default_hex = secrets.token_hex()
print(f"64字符的16进制字符串为：{default_hex}")
# 生成32字符的16进制字符串
short_hex = secrets.token_hex(32 // 2)
print(f"32字符的16进制字符串为：{short_hex}")

# 基础-4：生成URL安全的随机字符串
# token_urlsafe()
default_urlsafe = secrets.token_urlsafe()
print(f"32字节的URL安全的随机字符串:{default_urlsafe}")

# 基础-5：对比区别
# 随机种子
random.seed(12345)
print("=== seed:12345 ===")
for _ in range(5):
    print(f"    {random.random()}")

random.seed(12345)
print("=== seed:12345 ===")
for _ in range(5):
    print(f"    {random.random()}")
print("=== secrets ===")
for _ in range(5):
    print(f"    {secrets.token_hex(4)}")

print("=== secrets ===")
for _ in range(5):
    print(f"    {secrets.token_hex(4)}")
