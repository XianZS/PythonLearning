"""
traceback 标准库学习
"""

from os import listvolumes
import traceback
import logging
import sys


# 基础-1：异常与标准库之间的关系
def func_a():
    func_b()


def func_b():
    func_c()


def func_c():
    raise ValueError("这是一个测试异常")


try:
    func_a()
except Exception as e:
    print(f"[Error]:{e}")
    print(f"[Error-Type]:{type(e).__name__}")


# 基础-2：基础函数
# 打印当前异常的traceback
def div(a, b):
    return a / b


try:
    div(10, 0)
except ZeroDivisionError as e:
    print(f"[Error]:{e}")
    traceback.print_exc()
print("-" * 10)

# 将traceback格式化为字符串
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)
try:
    div(9, 0)
except ZeroDivisionError:
    error_msg = traceback.format_exc()
    logging.error(f"程序发生异常:{error_msg}")
    print("转换成功，已经成功记录")
print("-" * 10)


# 只打印traceback部分
def func_d():
    func_e()


def func_e():
    raise RuntimeError("运行时错误")


try:
    func_d()
except RuntimeError as e:
    print("接下来开始堆栈跟踪")
    traceback.print_tb(e.__traceback__)

print("-" * 10)


# 基础-3：控制深度
# 语法规范：通过limit参数来限制打印的堆栈深度，只显示最近的几层调用
def func_1():
    func_2()


def func_2():
    func_3()


def func_3():
    func_4()


def func_4():
    func_5()


def func_5():
    func_6()


def func_6():
    raise ValueError("深度测试异常")


try:
    func_1()
except ValueError:
    print("完成堆栈:")
    traceback.print_exc()
    print("=" * 10)
    print("最近3层的堆栈信息:")
    traceback.print_exc(limit=3)
print("-" * 10)


# 基础-4：写入文件
# 语法规范：使用file参数将traceback信息写入到文件之中，而不是打印到控制台之上。
def risky_operation():
    raise IOError("文件操作失败")


try:
    risky_operation()
except IOError:
    with open("error.log", mode="a", encoding="utf-8") as f:
        f.write("=" * 50)
        f.write("\n")
        traceback.print_exc(file=f)
        f.write("=" * 50)
        f.write("\n")
print("-" * 10)

# 进阶-1：获取traceback之中的详细信息
try:
    func_a()
except ValueError as e:
    print(f"=== [Error]:{e} ===")
    # 获取traceback之中的详细信息
    tbs = traceback.extract_tb(e.__traceback__)
    print("堆栈跟踪详细信息:")
    for i, frame in enumerate(tbs):
        print(f"第{i + 1}层:")
        print(f"    文件名:{frame.filename}")
        print(f"    行号:{frame.lineno}")
        print(f"    函数名:{frame.name}")
        print(f"    代码行:{frame.line}")
