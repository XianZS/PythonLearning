# --- 4.9.1.默认值参数
def stu(
    name,
    age,
    details="无备注信息",
):
    return {
        "name": name,
        "age": age,
        "details": details,
    }


def func(a, L=None):
    if not L:
        L = []
    L.append(a)
    print(L)


# func(1)
# func(2)
# func(L=[0, 0, 0], a=3)


# --- 4.9.2.关键字参数
# 位置参数 和 关键字参数
def add(a, b):
    print(f"[a]:{a}")
    print(f"[b]:{b}")
    return a * 10 + b * 3


# result = add(b=4, a=10)
# print(result)

# --- 4.9.3.特殊参数
# 位置参数 / 位置参数或关键字参数
# 位置参数或关键字参数 * 关键字参数
# 必须先设置位置参数，再设置关键字参数


def func1(*, a, b):
    print(a, b)


# func1(1, 2)
# func1(a=1, b=2)


def test_ip(ip, /, *, user, port):
    print(f"[ip] >>> {ip}")
    print(f"[user] >>> {user}")
    print(f"[port] >>> {port}")


# test_ip(
#     "192.168.8.1",
#     user="root",
#     port=80,
# )


# --- 4.9.4.任意实参列表
def func2(*args, **kwargs):
    """
    先接收若干个位置参数
    再接收若干个关键字参数
    """
    print(f"[args] >>> {args} | {type(args)}")
    print(f"[kwargs] >>> {kwargs} | {type(kwargs)}")
    print("---" * 10)


# func2(1, 2, 3, user="jom", address="ShangHai")
# func2(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, user="lom")


# --- 4.9.5.解包实参列表
def func3(a, b, c, d, e, f):
    # 前三个是位置参数
    # 后三个是关键字参数
    print(a, b, c, d, e, f)


args = (1, 2, 3)
kwargs = {
    "d": 4,
    "e": 5,
    "f": 6,
}

# func3(*args, **kwargs)


# --- 4.9.6.Lambda 表达式
# lambda 传入参数:简化函数体内容
# a*10+b*3
def add1(a, b):
    return a * 10 + b * 3


result1 = add1(11, 3)
f = lambda a, b: a * 10 + b * 3
result2 = f(11, 3)
# print(f"[result1] >>> {result1}")
# print(f"[result2] >>> {result2}")
#
stus = [
    ["jom", 19, "ShangHai"],
    ["kom", 11, "ShangHai"],
    ["lom", 33, "ShangHai"],
    ["aom", 19, "ShangHai"],
    ["som", 20, "ShangHai"],
    ["dom", 23, "ShangHai"],
]

stus.sort(key=lambda child: child[1])

# print(stus)


# --- 4.9.7.文档字符串
def mul(a: int, b: int, c: int) -> int:
    """
    mul a and b and c

    a*b >> a_b
    a_b*c >>> result
    return result
    """
    return a * b * c


# doc = mul.__doc__
# print(doc)

print(mul(1, 2, 3))


if __name__ == "__main__":
    pass
