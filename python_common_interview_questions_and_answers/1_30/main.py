def main1():
    # 算术运算符示例
    a, b = 10, 3
    print(a + b)  # 13
    print(a // b)  # 3（整除）
    print(a % b)  # 1（取余）
    print(a**b)  # 1000（幂运算）

    # 复合赋值示例
    c = 5
    c += 2  # 等价于 c = c + 2
    print(c)  # 7


def main2():
    print(3 and 0)  # 0（有假返假）
    print(3 or 0)  # 3（有真返真）
    print(not True)  # False


def main3():
    lst = [1, 2, 3]
    print(2 in lst)  # True
    print("a" in "apple")  # True
    print("name" in {"name": "Tom"})  # True（判断键）


def main4():
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(a == b)  # True（值相等）
    print(a is b)  # False（不是同一个对象）

    c = a
    print(a is c)  # True（指向同一内存地址）


def main5():
    a = 6  # 0110
    b = 3  # 0011
    print(a & b)  # 2（0010）
    print(a | b)  # 7（0111）
    print(a << 1)  # 12（1100）


def main6():
    # 直接表示多进制
    bin_num = 0b1010  # 十进制10
    oct_num = 0o12  # 十进制10
    hex_num = 0xA  # 十进制10

    # 十进制转其他进制
    print(bin(10))  # '0b1010'
    print(hex(10))  # '0xa'


def main7():
    d = {"name": "Tom", "age": 18}
    # 方法1：keys()方法
    keys = d.keys()
    print(list(keys))  # ['name', 'age']

    # 方法2：遍历字典
    for key in d:
        print(key)


def main8():
    pass


def main9():
    # 链式赋值
    x = y = z = 0

    # 并行赋值
    a, b, c = 1, "hello", True

    # 解包赋值
    lst = [10, 20]
    m, n = lst


def main10():

    # 基础解包
    t = (1, 2, 3)
    a, b, c = t

    # 带*接收剩余元素
    t2 = (1, 2, 3, 4, 5)
    first, *middle, last = t2
    print(middle)  # [2, 3, 4]

    # 经典应用：交换变量
    x, y = 10, 20
    x, y = y, x
    print(x, y)


def main11():
    pass


def main12():
    pass


def main13():
    pass


def main14():
    pass


def main15():
    pass


def main16():
    s1 = "I'm Tom"  # 内含单引号，用双引号
    s2 = '他说："你好"'  # 内含双引号，用单引号


def main17():
    # break
    for i in range(5):
        if i == 3:
            break
        print(i)  # 输出 0 1 2

    # continue
    for i in range(5):
        if i == 2:
            continue
        print(i)  # 输出 0 1 3 4

    # pass 占位
    def func():
        pass


def main18():
    # 字典映射实现
    def case1():
        return "周一"

    def case2():
        return "周二"

    def default():
        return "其他"

    switch = {1: case1, 2: case2}
    result = switch.get(3, default)()


def main19():
    # 1个参数：0~4
    for i in range(5):
        print(i)

    # 2个参数：2~5
    for i in range(2, 6):
        print(i)

    # 3个参数：步长2，1,3,5,7,9
    for i in range(1, 10, 2):
        print(i)

    # 倒序
    for i in range(5, 0, -1):
        print(i)


def main20():

    # 元素类型转换：字符串转整数
    str_list = ["1", "2", "3"]
    # 列表推导式
    int_list = [int(x) for x in str_list]
    # map函数
    int_list2 = list(map(int, str_list))

    # 列表转其他容器
    lst = [1, 2, 3]
    t = tuple(lst)  # 转元组
    s = set(lst)  # 转集合


def main21():
    import dis

    def test():
        for x in range(10):
            print(x)

    dis.dis(test)


def main22():
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(a == b)  # True（值相等）
    print(a is b)  # False（不是同一对象）


def main23():
    print(all([1, True, "a"]))  # True
    print(any([0, False, ""]))  # False
    print(all([]))  # True（空集逻辑）
    print(any([]))  # False


def main24():
    import time

    def timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            print(f"{func.__name__} 耗时：{time.time() - start}")
            return res

        return wrapper

    @timer  # 等价于 func = timer(func)
    def func():
        time.sleep(1)


def main25():
    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            yield b
            a, b = b, a + b

    # 迭代生成器
    for num in fib(5):
        print(num)  # 1 1 2 3 5


def main26():
    lst = ["a", "b", "c"]
    for index, value in enumerate(lst, start=1):
        print(index, value)
    # 输出：
    # 1 a
    # 2 b
    # 3 c


def main27():
    print(-10 // 3)  # -4（向下取整）
    print(-10 % 3)  # 2（余数与除数同号）
    print(2**3)  # 8


def main28():
    pass


def main29():
    a, b = 10, 20
    max_num = a if a > b else b
    print(max_num)  # 20


def main30():
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello Flask!"

    app.run()


def pr():
    print("===" * 10)


if __name__ == "__main__":
    pass
    # main1()
    # main2()
    # main3()
    # main4()
    # main5()
    # main6()
    # main7()
    # main8()
    # main9()
    # main10()
    # main11()
    # main12()
    # main13()
    # main14()
    # main15()
    # main16()
    # main17()
    # main18()
    # main19()
    # main20()
    # main21()
    # main22()
    # main23()
    # main24()
    # main25()
    # main26()
    # main27()
    # main28()
    # main29()
    # main30()
