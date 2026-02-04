import sys

"""
    模块生命周期：
        加载 ——》 初始化 ——》 缓存 ——》 销毁
"""

res = sys.modules
print(type(res), len(res))

import test

print(type(res), len(res))

print(
    res["test"]
)  # <module 'test' from 'D:\\code\\py_item\\PythonLearning\\python_advance_learning\\test.py'>
