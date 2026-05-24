# 进阶-1：生成复杂度要求的安全密码
import secrets
import string


def generate_password(
    length=12,
    include_uppercase=True,
    include_lowercase=True,
    include_digits=True,
    include_symbols=True,
):
    if length < 8:
        raise ValueError("密码长度不符合要求")
    char_sets = []
    if include_uppercase:
        char_sets.append(string.ascii_uppercase)
    if include_lowercase:
        char_sets.append(string.ascii_lowercase)
    if include_digits:
        char_sets.append(string.digits)
    if include_symbols:
        char_sets.append("!@#?+=-*<>.,")
    if not char_sets:
        raise ValueError("至少包含一种字符设置")
    # 合并所有的字符集
    all_chars = "".join(char_sets)
    password = []
    for char_set in char_sets:
        password.append(secrets.choice(char_set))
    # 填充剩余的长度
    len_password = len(password)
    for _ in range(length - len_password):
        password.append(secrets.choice(all_chars))
    # 打乱顺序
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


if __name__ == "__main__":
    print("=== 安全密码生成器 ===")
    default_password = generate_password()
    print(f"[默认密码]:{default_password}")
    strong_password = generate_password(length=16)
    print(f"[16位密码]:{strong_password}")
    try:
        res = generate_password(length=4)
        print(f"[4位密码]:{res}")
    except Exception as e:
        print(f"[Error]:{e}")
