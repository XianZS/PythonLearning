# 进阶-4：高级语法技巧
# 浮点数精度问题：四舍五入，高级参数部分匹配设置
import doctest


def div(a, b):
    """
        计算 a 除以 b 的结果

    >>> round(div(1,3),6)
    0.333333

    >>> div(1,3)    # doctest: +ELLIPSIS
    0.333333333...
    """
    return a / b


# 处理对象表示
# 1.为类定义 __repr__ 方法
# 2.忽略
# 3.测试对象的属性而不是对象本身
class Person:
    def __init__(self, name):
        self.name = name


def create_person(name):
    """
    创建一个 Person 对象

    >>> create_person("Alice")  # doctest: +ELLIPSIS
    <d_l_4.Person object at ...>
    """
    return Person(name=name)


# 进阶-5：命令行参数详解
# -v --verbose 显示详细的测试过程
# -q --quiet 只显示失败的测试
# -f 遇到第一个失败就停止
# -o 设置doctest选项
# --no-color 禁用颜色输出
# --force-color 强制启动颜色输出
