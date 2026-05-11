"""
python debug 标准库
"""

import pdb


# 基础-1：四种启动方式
# 命令行启动方式
# python -m pdb your_script.py
# 在代码内插入断点
def test():
    result = 0
    breakpoint()
    for i in range(1, 11):
        result += i
    return result


# 事后调试 （异常捕捉情况下）
# 在交互式解释器之中调试

# 基础-2：命令
# list l 显示当前位置附近的11行代码
# next n 执行下一行代码（不进入函数体）
# step s 执行下一行代码（进入函数体）
# continue c 自动执行到下一个断点或者程序结束
# print p 打印变量或者表达式的数值
# pprint pp 格式化打印复杂数据结构


def fact(n):
    if n < 0:
        raise ValueError(f"{n}不合法")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def test2():
    nums = [3, 5, 7]
    for num in nums:
        print(f"{num} ! = {fact(num)}")


# 进阶-1：断点高级管理
# b func/number/file:number
# tbreak
# 查看所有断点：break
# 修改：disable NUM_Id
# enable NUM_Id
# 删除：clear NUM_Id/None
# ignore NUM_Id counter
# 忽略NUM_Id接下来的counter次触发


# 进阶-2：栈和帧操作
# 语法规范：where 简写 w
# > 标识当前正在执行的帧
# 最上面的是最外层调用
# 最下面的是正在执行的函数
# up 向上移动一个帧单位
# down 向下移动一个帧单位
# frame number:int 直接跳转到第number个帧
# globals() locals()
# 查看当前帧的所有全局/局部变量

# 进阶-3：运行时修改与执行
# 在调试的过程之中，可以直接修改变量的数值，来测试不同的场景
# 语法规范：
# !var=new_value
# p new_func() or old_func()
# import new_module
# new_module.func() or new_module.some

# 进阶-4：事后调试
try:

    def div(a, b):
        return a / b

    def test3():
        div(10, 0)

    result = test3()
    print(f"[result]:{result}")
except Exception as e:
    print(f"[Error]:{e}")
    pdb.post_mortem()


if __name__ == "__main__":
    print(test2())

