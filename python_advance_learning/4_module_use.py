"""
（1）加载
（2）初始化
（3）读缓存
（4）销毁
"""

# （1）加载
# - 是不是标准库
# - 是：直接返回
# - 不是标准库：
#   - sys.module 路径之中查找对应的python文件
#   - sys.path 路径之中查找对应的python文件
#   - 如果没有找到
#       - modul not found error

import sys

# 模块缓存字典
modules_dict = sys.modules

for key, value in modules_dict.items():
    print(key, value)

print(len(modules_dict))

import numpy

# 在运行过程之中，会不断将你所导入的包，添加到模块缓存字典之中
# 热更新（实时更新）
print(len(modules_dict))


print("=" * 30)

path_list = sys.path
print(path_list)
"""
['D:\\code\\py_item\\PythonLearning\\python_advance_learning',
'C:\\Users\\XianZS\\.conda\\envs\\PythonLearning\\python314.zip', 
'C:\\Users\\XianZS\\.conda\\envs\\PythonLearning\\DLLs', 
'C:\\Users\\XianZS\\.conda\\envs\\PythonLearning\\Lib', 
'C:\\Users\\XianZS\\.conda\\envs\\PythonLearning', 
'C:\\Users\\XianZS\\.conda\\envs\\PythonLearning\\Lib\\site-packages']
"""
sys.path.append("C:\\Users\\XianZS\\Desktop")
print(sys.path)

# 从模块缓存字典之中销毁内容
print(modules_dict)

del modules_dict["numpy"]
print(modules_dict)
print(len(modules_dict))


if __name__ == "__main__":
    pass

