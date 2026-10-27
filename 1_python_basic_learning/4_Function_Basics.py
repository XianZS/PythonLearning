"""
# 函数基础

1.函数定义
2.函数参数
3.函数返回值
4.函数的自定义文档帮助
5.函数的作用域
6.匿名函数（lambda 表达式）
"""


# 1.函数定义
#   函数名+参数+函数体
def add(a, b):
    """
    add:函数名（必选）
    a，b：参数（可选）
    return a+b：函数体（必选）
    """
    return a + b


print(add(1, 2))


# 2.函数参数
#   （1）位置参数:需要按照顺序传入参数
def add_1(a, b, c):
    print(f"a:{a},b:{b},c:{c}")
    return a + b + c


# 1+2+3 a=1 b=2 c=3
print(add_1(1, 2, 3))


#   （2）关键字参数:直接指明字段所属的对象，就叫做关键字参数
def some(name, age, details):
    print(f"name:{name},age:{age},details:{details}")
    return ""


# 我不知道三个参数的顺序，但是我知道有三个参数
some(name="jom", details="详细信息", age=19)


#   （3）默认参数:参数传入的可选性，提前设定字段的内容，如果传入，就是用传入内容，如果没有传入，就使用默认设置的参数
def some2(name, age, details="这是设置的默认参数"):  # 我可能不知道当前对象的详细信息
    print(f"name:{name},age:{age},details:{details}")
    return ""


some2(name="jom", age=20, details="这是我传入的参数")
some2(name="kom", age=19)


#   （4）可变位置参数 *args：我不知道应该传入多少个参数，传入参数的个数不确定的情况
#   位置参数，会按照你传入参数的顺序，将他们封装成一个元组对象
#   *args
# def some3(a, b, c, d, e, f, g):
def some3(*args):
    print(args)
    # print(f"{a},{b},{c},{d},{e},{f},{g}")
    return ""


some3(1, 2, 3, 4, 5)
some3(1, 2, 3, 4, 5, 6)
some3()


#   （5）可变关键字参数 **kwargs:我也不知道要传入多少个键值对，以k-v的形式传入参数
#   将传入的内容，封装成一个dict格式
def some4(**kwargs):
    print(kwargs)
    print(type(kwargs))
    return ""


# 封装一个学生信息
some4(stu_name="jom", stu_age="19", stu_details="暂无详细信息")
some4(teacher_name="kom", stu_age="32")


# 3.函数返回值：return 后面的内容就是函数的返回值
#   （1）单返回值
def add_2(a, b):
    return a + b


print(add_2(1, 2))


#   （2）多返回值:多返回值的类型是元组，会将多个返回值封装到一个元组之中
def some5(child1, child2, child3):
    return child1, child2


print(some5(1, 2, 3))


# 4.函数的自定义文档帮助：面向共同开发者，解释自己的函数功能
def some6(a, b, c):
    """
    函数自定义文档
    - 需要指明函数名：some6
    - 需要指明传入参数：a:int，b:int，c:int
    - 需要指明函数的大致功能：返回大于5的参数
    """
    res = []
    if a > 5:
        res.append(a)
    if b > 5:
        res.append(b)
    if c > 5:
        res.append(c)
    return res


some6(3, 6, 10)
help(some6)


#   help帮助文档
# 5.函数的作用域
#   （1）全局变量
#   - 可以读：可以在函数内部调到（read）全局变量
#   - 不可以写：不可以修改全局变量
a = 1


def some7():
    print(a)
    # a = 2
    return ""


some7()


#   （2）局部变量
#   在函数内部定义的变量，就是当前函数的局部变量，局部变脸具有不可互通性质
#   不可以在全局之中，访问局部变量
def main():
    a = 1
    b = 2
    print(a + b)
    return ""


main()


#   （3）转换：在函数内容，修改全局变量，使用global参数修饰全局变量
b = 1


def some8():
    global b
    b = 2
    print(b)
    return ""


some8()
print("===", b)


# 6.匿名函数
#   lambda 参数列表：表达式
# c=lambda a,b:a+b
x = 2
y = 5
number = lambda x, y: x**y
print(number)
print(number(x, y))

some = [("jom", 89), ("kom", 99), ("lom", 32), ("fom", 55)]  # type:ignore
print("现在将要按照成绩排序：", some)
some.sort(key=lambda x: x[1])  # type:ignore
print("按照成绩排序之后的结果为：", some)
