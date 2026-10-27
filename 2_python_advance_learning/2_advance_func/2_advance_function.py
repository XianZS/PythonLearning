"""
1.迭代器
"""

# 创建可迭代对象 iterable
from ntpath import exists
from time import strftime


nums = [1, 2, 3]
print(nums, type(nums))
# 创建迭代器 iterator
res = iter(nums)
print(res, type(res))

# iterator特性1:通过next求值
print(res.__next__())  # next(res)
# iterator特性2:指针的不可逆性，每次指针会向后移动一位
print(res.__next__())
print(next(res))
# iterator特性3:只可以进行一次访问，当访问越界时，会触发StopIteration错误
# print(res.__next__())


# 需要自定义实现一个iterator对象 迭代器
# 需要实现 __iter__ __next__ 这两个方法
class MyIterator:
    def __init__(self, nums):
        self.nums = nums
        self.current = 1
        self.length = len(nums)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.length:
            res = self.nums[self.current - 1]
            self.current += 1
            return res
        else:
            raise StopIteration


my_iter_obj = MyIterator(
    [3, 123, 123, 4132, 12, 21, 12, 21321123, 1235, 342, 4, 2, 11, 12, 2312]
)
# <class list>:可迭代对象 iterable
# <class list_iterator>:迭代器 iterator
print(my_iter_obj, type(my_iter_obj))
print(next(my_iter_obj))
print("===" * 30)

"""
2.生成器
"""
# 列表推导式
nums = [x for x in range(1, 11)]
print(nums, type(nums))
# 生成器推导式
res = (x for x in range(1, 11))
print(res, type(res))


# 生成器函数 yield
# 对数据进行累加求数值，在上次累加的基础上，进行求数值累加和
def my_gen(number):
    res = 0
    for num in number:
        res += num
        print(f"第一次求和的结果为:{res}")
        yield res


gen_obj = my_gen([1, 2, 3, 4, 5, 6, 7, 8, 9])
next(gen_obj)
next(gen_obj)
next(gen_obj)

# 在创建时指明累加求和对象
# 现在的需求：动态的累加求和
# send() 可以向生成器发送数据
# obj.send(number)
# 发送数值 = yield 返回值


def my_gen_send():
    res = 0
    index = 1
    while True:
        send_number = yield res
        if send_number is None:
            break
        else:
            res += send_number
            print(f"第{index}次累加求和的结果为:{res}")
            index += 1


my_gen_send_obj = my_gen_send()
# 此时需要先让生成器的指针指向接收值处
next(my_gen_send_obj)
try:
    my_gen_send_obj.send(123)
    my_gen_send_obj.send(3123)
    my_gen_send_obj.send(1)
    my_gen_send_obj.send(None)
except StopIteration:
    print("动态累加求和结束")
print("=" * 30)


"""
3.闭包
"""


# 1.简单的闭包实现
# 实现要求：实现一个加法，知道一个加数，不知道另外一个加数
def add_base(number):
    # add_base 外部函数
    def add_number(number_2):
        # add_number 内部函数
        return number + number_2

    # 返回的内容：
    # 内部函数（√）
    # 内部函数的返回值（X）
    return add_number


ab_obj = add_base(10)
print(ab_obj, type(ab_obj))
print(f"10+2={ab_obj(2)}")
print(f"10+10={ab_obj(10)}")


# 思考？
# 问题1：闭包能否嵌套2层，及其两层以上？
# 答案：可以
def func1(number_1):
    def func2(number_2):
        def func3(number_3):
            return number_1 * number_2 * number_3

        return func3

    return func2


# f_1指向的是func2
f_1 = func1(10)
print(f_1, f_1(10)(10))
if f_1.__closure__:
    for cho in f_1.__closure__:
        print(cho)

print("-" * 30)

# 想要让f_1指向func3
f_1_1 = func1(2)(3)
print(f_1_1, f_1_1(3))
if f_1_1.__closure__:
    for cho in f_1_1.__closure__:
        print(cho)


# 问题2：闭包中变量的执行时机，是在什么时候？
# 答案：内层函数执行时
# === 变量延迟绑定 ===
# 绑定时机：内层函数执行时，闭包被调用时


def function1():
    res = []
    # x=0 1 2
    for x in range(3):

        def function2(x=x):
            print(x)

        res.append(function2)
    return res


# 打眼一看，可能觉得结果应该是 0；1；2（错误）
f1_obj = function1()
for cho in f1_obj:
    cho()

print("=" * 30)

"""
4.装饰器
"""


# （1）装饰器的构成
# - 基础装饰器 （无参数传入） 由2层闭包所构成
# - 进阶装饰器 （由参数传入） 由3层闭包所构成
# 装饰器 被装饰器函数
# @装饰器 # 语法糖的格式
# 被装饰函数
def func_1(func):
    print("=== 【装饰器】外层函数执行 ===")

    def func_2():
        func()
        print("=== 【装饰器】内层函数执行 ===")
        # func()

    return func_2


@func_1
def func_3():
    print("=== 被装饰函数执行 ===")


func_3()
# 被装饰函数的执行顺序和执行时机，是由装饰器所决定的


# （2）基础装饰器 由两层闭包所构成的
# 日志记录的装饰器
def count_logs(func):
    def wrapper():
        import time
        import os

        begin_time = time.time()
        func()
        spend_time = time.time() - begin_time
        if os.path.exists("./logs.txt"):
            with open("./logs.txt", "a", encoding="utf-8") as f:
                f.write(f"[{func}]：花费时间：{spend_time}\n")
        else:
            with open("./logs.txt", "w", encoding="utf-8") as f:
                f.write(f"[{func}]：花费时间：{spend_time}\n")

    return wrapper


@count_logs
def pr():
    for x in range(1, 10000 + 1):
        print(f"{x} ", end="")
    print()


pr()


# 传入参数应该如何处理？
# 进阶装饰器 （三层闭包实现）
# 最外层：接收传入参数
# 中间层：接收被装饰函数
# 最内层：需要做一个兼容处理
def out_func(judge_):
    def middle_func(func):
        def e_func(*args, **kwargs):
            print(f"当前日志级别为:{judge_}")
            res = func(*args, **kwargs)
            return res

        return e_func

    return middle_func


@out_func(judge_="级别A")
def pr_function():
    for x in range(1, 10 + 1):
        print(f"{x} ", end="")
    print()


pr_function()


@out_func(judge_="级别B")
def pr_function_2():
    for x in range(1, 10 + 1):
        print(f"{x} ", end="")
    print()


pr_function_2()


# 保存元数据
from functools import wraps


def o_func(func):
    @wraps(func)
    def e_func():
        print("e_func")
        func()

    return e_func


@o_func
def function():
    """
    function 被装饰函数的自定义帮助文档
    帮助文档内容
    """
    print("func元数据保存")


help(function)


if __name__ == "__main":
    pass
