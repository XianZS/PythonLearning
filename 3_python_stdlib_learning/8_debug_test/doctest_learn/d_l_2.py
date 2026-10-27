"""
# doctest 标准库进阶学习
"""

import time
import doctest

# 进阶-1：常用选项详解
# 语法规范：# doctest: + 常用选项
# NORMALIZE_WHITESPACE：忽略空白符差异，将多个空白符视为一个空白符


def print_list(lst):
    """
    打印列表之中的元素

    >>> print_list([1,2,3])
    1 2 3

    >>> print_list([4,5,6]) # doctest: +NORMALIZE_WHITESPACE
    4   5   6
    """
    print(" ".join(map(str, lst)))


# ... 匹配任意字符串
# ELLIPSIS
def get_cur_time():
    """
    获取当前时间
    >>> get_cur_time()  # doctest: +ELLIPSIS
    'Current time: ...'
    """
    return f"Current time: {time.ctime()}"


# IGNORE_EXCEPTION_DETAIL
# 忽略异常信息之中的详细内容，只检查异常类型

# SKIP
# 跳过某些测试用例


# 只报告第一个失败的测试用例
# doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_RAILURE)

# 进阶-2：独立测试文件
# 将测试过程写入到txt文件之中
# 运行语法规范：
# python -m doctest my_file.txt -v
