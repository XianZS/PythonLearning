"""
1.module的使用
    （1）导入方式和重命名
    （2）module的分类
2.自定义模块
    （1）创建和导入自定义模块
    （2）__name__
    （3）模块的私有变量
3.自定义包
    （1）自定义包的使用
    （2）__init__
    （3）第三方包的使用
"""

# module 的使用
# 定义一个无穷大的变量
# import math # 导入东西过多，会导致系统的开支过大
# a = math.inf
from math import inf  # 极大程度上减少了系统的开支


a = inf
# from 包名 import 变量/类对象/类/方法/函数
print(a)
# module的分类
# 标准库（math datetime time）；第三方库（numpy pandas keras sklearn matplotlib）；自定义库
# from math import sin
# from datetime import datetime
# import math
# as ： 重命名时使用
import numpy as np

nums = np.array([1, 2, 3])
print(nums, type(nums))

# 每一个文件，就相当于，一个自定义模块
# 现需要确定自定义模块在哪里

from my_module import func1

from my_module import *

# import 包名
# from 包名 import 私有对象
# from 包名 import *


res1 = func1(1, 2)
print(res1)

# 当前文件的被操作情况
# ① 自己调用自己：__main__
# ② 其它人调用自己：自己的文件名
print(__name__)
print(__name__)
# print(__version_module_private)
print(version_module)


# 3.模块的使用
import some

# from some import func_2
# func_2.function_2()
some.f2()
some.f1()
#
# 第三方包的下载语法规范(pip-cmd)
# pip install 第三方包名
import pandas

res0 = pandas.array([1, 2, 3])
print(res0)
#
#
#
#
#
#
#
#
#
