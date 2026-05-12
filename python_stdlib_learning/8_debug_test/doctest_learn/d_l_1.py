"""
doctest 标准库学习
"""

import doctest


# 基础-1：基础使用
def add(a, b):
    """
        计算两个数之和。
    >>> add(2,3)
    5
    >>> add(-1,1)
    0
    >>> add(0,1000)
    1000
    """
    return a + b


# 基础-2：三种启动方式
# === 直接运行脚本：
#   不会有任何的输出，也可以添加 -v 参数
# === 命令行运行 doctest 模块
# python -m doctest my_file.py -v
# === 在交互式解释器之中运行

# 基础-3：基本语法规范
# doctest 语法规范：
# - 测试输入：必须以 >>> 开头，后面跟随python代码
# - 预期输出：必须在测试输入的后面，截止于下一个测试输入或者空行
# - 空行：标识一个测试用例的结束
# - 续行：多行语句使用 ... 作为提示符
# - 空白符：在默认情况下，输出之中的空白符必须是完全匹配


# 基础-4：异常测试的写法
def div(a, b):
    """
    计算a除以b的结果

    >>> div(10,2)
    5.0

    >>> div(10,0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    return a / b


# 基础-5：空白符处理
# doctest提供了一个方法：
# NORMALIZE_WHITESPACE


if __name__ == "__main__":
    doctest.testmod()
