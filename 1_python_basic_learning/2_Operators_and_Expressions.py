"""
# 运算符和表达式

1.算术运算符
2.赋值运算符
3.比较运算符
4.逻辑运算符
5.成员运算符
6.身份运算符
"""

# 加、减、乘/整除、除、取模、幂运算
a = 100
b = 30
c = 20
print(a + b + c, a - b - c)
print(a * b * c)
print(a / b, a // b)
print(a % b)
print(a**2)
# = += -= *= /=
a %= b  # 相当于 a=a%b
print(a)
# > >= < <=
if a > b:
    print("a>b")
else:
    print("a<b")


# and or not
# 当逻辑条件成立时，那么结果是True，反之为False
# 逻辑条件1 and 逻辑条件2 and 逻辑条件3
def res1():
    print("=== res1 ===")
    return True


def res2():
    print("=== res2 ===")
    return False


# and 逻辑运算符:逻辑条件全部成立
if res1() and res2():
    print("res1 true res2 true")
else:
    print("res1 或 res2 存在False")

print("=" * 20)

# or 逻辑运算符:只要存在一个逻辑条件成立 只要有一个逻辑条件成立，那么该逻辑条件的后续逻辑条件都不会被执行
if res1() or res2():
    print("or 成立")
else:
    print("or 不成立")

# not 逻辑运算符:取反;False的反就是True，相对的，True的反就是False
if not res2():
    print("not 成立")
else:
    print("not 不成立")

# in 、 not in
names = ["aom", "som", "dom"]
people1 = "dom"
people2 = "jack"
# if 成员 in 数据集合:True
# else: False
if people1 in names:
    print(f"{people1}在{names}之中")
else:
    print(f"{people1}不在{names}之中")

if people2 in names:
    print(f"[in]:{people2}在{names}之中")
else:
    print(f"[in]:{people2}不在{names}之中")

if people2 not in names:
    print(f"[not in]:{people2}不在{names}之中")
else:
    print(f"[not in]:{people2}在{names}之中")

# is 、 not is
# is 和 == 的区别？
# is 比较的是对象的地址
# == 比较的是对象的数值
a = 1
b = 1
print(a == b)  # True
print(a is b)  # True
nums1 = [1, 2, 3]
nums2 = [1, 2, 3]
print(nums1 == nums2)  # True
print(nums1 is nums2)  # False


if __name__ == "__main__":
    pass
