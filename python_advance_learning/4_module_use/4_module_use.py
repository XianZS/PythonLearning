"""
什么是模块的生命周期：
    （1）加载阶段
        - 首先判断是不是标准库
            - 是：直接导入
            - 不是：
                模块缓存字典之中查找：
                - 存在：直接导入
                - 不存在：去path路径之中寻找
                    - 找到：直接导入
                    - 没找到：module not found error
    （2）初始化阶段
        将自定义导入的所有模块，全部添加到模块缓存字典之中
    （3）读缓存阶段
        （程序运行阶段）
        优点：速度快
        缺点：缓存之中的内容，不会自动更新
            模块缓存字典之中的模块，存在于缓存之中。
            并不能和内存进行同步更新。
    （4）销毁阶段
        手动销毁：del
        自动销毁：python解释器重启，程序运行结束，就会自动销毁
"""

import sys

# （1）加载阶段
# 得到模块缓存字典
module_dict = sys.modules
for k, v in module_dict.items():
    print(k, v)
print("加入之前的长度：", len(module_dict))
#
# （2）初始化阶段
import numpy

print("加入numpy包之后的模块缓存字典长度：", len(module_dict))

# 模块缓存字典的长度：不是添加1，而是单位“1”
#
# （3）读缓存阶段
#   略
#
# （4）销毁阶段
del module_dict["site"]
print("销毁site模块之后的模块缓存字典长度：", len(module_dict))
# 可以手动结束某个模块的生命周期


if __name__ == "__main__":
    pass
