version_module = "1.0.0"


def func1(a, b):
    return a + b


def func(a, b):
    return a - b


def func3(a, b):
    return a * b


def func4(a, b):
    return a / b


# 有些方法/函数/变量/类 你不希望被别人使用 但是你却不得不定义这样一个对象
__version_module_private = "2.0.0"
