"""
os标准库学习
1、路径操作
    （1）获取路径
    （2）路径拼接
    （3）拆分路径和文件名
    （4）路径是否存在
    （5）判断对象是文件还是路径？
    （6）获取文件大小
2、目录操作
    （1）创建目录
    （2）删除目录
    （3）遍历目录 非递归/递归
3、环境变量与系统操作
    （1）获取环境变量
    （2）设置临时环境变量
    （3）获取系统信息
    （4）执行系统命令
"""

import os

# 1、路径操作
# 获取当前路径
now_cwd = os.getcwd()
print(f"当前工作路径为:{now_cwd}")
# 路径拼接
res_cwd = os.path.join(now_cwd, "os_learn.py")
print(f"拼接之后的路径:{res_cwd}")
# 拆分路径
# D:\code\py_item\PythonLearning\python_stdlib_learning\1_file_path_opt\os_learn.py
a = os.path.dirname(res_cwd)  # 路径
b = os.path.basename(res_cwd)  # 文件名
print(f"a:{a}")
print(f"b:{b}")
# 判断路径是否存在
test_path = "/user/opt"
if os.path.exists(test_path):
    print("路径存在")
else:
    print("路径不存在")

if os.path.exists(a):
    print("路径存在")
else:
    print("路径不存在")

# 判断对象是路径还是文件名
if os.path.isfile(b):
    print("是文件")
else:
    if os.path.isdir(b):
        print("是路径")
    else:
        print("都不是")

# 获取文件大小
# 单位：字节
size_b = os.path.getsize(b)
print(f"b文件的大小是:{size_b}字节")


# 2、目录操作
# 增加一个目录
# 非递归增加
# os.mkdir("test_dir")
# 使用递归增加目录
os.makedirs("test_dir_2/some", exist_ok=True)
# 如何删除目录
# os.rmdir("test_dir")  # 以非递归形式来进行删除
# os.removedirs("test_dir_2/some")  # 以递归形式删除
# 如何查找
# 非递归查找
ls1 = os.listdir(".")
print(f"{ls1}")
# 递归查找
ls2 = os.walk(".")
ls2 = list(ls2)
# print(f"{ls2},{type(ls2)}")
for a, b, c in ls2:
    print(f"[{a}]:文件夹{b},文件:{c}")

# 3、环境变量和系统操作
# 获取环境变量
envs = os.environ.get("PATH")
# print(envs)
print(type(envs))
# 列表化环境变量 PATH
if envs:
    path_envs = envs.split(";")
    # print(path_envs)
    for cho in path_envs:
        print(cho)
else:
    print("未找到对应的环境变量")

# 设置临时环境变量
os.environ["MY_SET_ENV"] = "MY_SET_ENVing"
print(f"我设置的环境变量:{os.environ.get('MY_SET_ENV')}")

# 获取当前系统信息
# posix=MACOS/LINUX
# NT=WINDOWS
name_pc = os.name
print(name_pc)

print("---" * 10)
# 如何执行系统命令
sys_obj = os.system("tree /a /f")
print("---" * 10)
print(sys_obj)
