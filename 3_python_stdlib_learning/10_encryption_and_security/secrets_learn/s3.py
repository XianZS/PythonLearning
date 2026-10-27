# 进阶-2：生成一次性密码
import secrets
import time
from typing import Dict, Tuple

# 存储已经使用过的一次性密码
otp_store: Dict[str, Tuple[int, str]] = {}
otp_expire_time = 300


def generate_otp(length, user_id=None):
    # 生成一次性密码
    if not 4 <= length <= 8:
        raise ValueError("OTP 长度需要在4-8位之间")
    otp = str(secrets.randbelow(10**length)).zfill(length)
    expire_time = int(time.time()) + otp_expire_time
    otp_store[otp] = (expire_time, user_id)  # type: ignore
    return otp


def verify_otp(otp, user_id):
    if otp not in otp_store:
        return False, "OTP不存在或者已经被使用"
    expire_time, stored_user_id = otp_store[otp]
    current_time = int(time.time())
    if current_time > expire_time:
        # 删除过期的otp
        del otp_store[otp]
        return False, "OTP已经过期"
    if user_id is not None and stored_user_id != user_id:
        return False, "用户不匹配"
    del otp_store[otp]
    return True, "OTP验证通过"


if __name__ == "__main__":
    user_id = "user123"
    otp = generate_otp(6, user_id)
    print(f"[6位otp]:{otp}")
