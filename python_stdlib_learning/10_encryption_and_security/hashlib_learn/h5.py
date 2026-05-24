# 进阶-1：加盐哈希
import hashlib
import os
import secrets


def hash_password(password):
    # 对密码进行加盐hash处理
    # secrets.token_hex(number:int) 单位字节 128位
    salt = secrets.token_hex(16)
    salt_res = (password + salt).encode("utf-8")
    password_hash = hashlib.sha256(salt_res).hexdigest()
    return password_hash, salt


def v_password(password, stored_hash, stored_salt):
    # 验证
    salted_password = (password + stored_salt).encode("utf-8")
    cal_hash = hashlib.sha256(salted_password).hexdigest()
    return secrets.compare_digest(cal_hash, stored_hash)


if __name__ == "__main__":
    user1, user2 = "jom", "kom"
    pd1, pd2 = "123", "123"
    print(f"[{user1}-hash]:{hash_password(pd1)}")
    print(f"[{user2}-hash]:{hash_password(pd2)}")
    a, b = hash_password(pd2)
    if v_password(pd2, a, b):
        print("相同")
    else:
        print("不同")
