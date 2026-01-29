"""
【第6节】Python之中的文件操作
"""

"""
    模块1：文件操作基础核心
        （1）文件的打开
        （2）文件的关闭
        （3）上下文管理器的使用
        （4）文件打开模式的了解
"""
# 打开文件
f = open("./test.txt")
print(f)  # <_io.TextIOWrapper name='./test.txt' mode='r' encoding='cp936'>
# 关闭文件
f.close()
# 上下文管理器 with
with open("./test.txt") as f:
    print(f)
"""
    模块2：文本文件的读取操作
        （1）文本文件的读取 read(number) readline() readlines() enumerate(f)
        （2）文本文件的写入 write(str) writelines(list)
"""
with open("./test.txt", "r", encoding="utf-8") as f:
    # read(number:Union[None,int]) 方法
    context_1 = f.read(2)
    context_2 = f.read()
    print(context_1, "\n", context_2)

print("===" * 30)
with open("./test.txt", "r", encoding="utf-8") as f:
    while True:
        context_1 = f.readline()
        if context_1:
            print(context_1)
        else:
            break
print("===" * 30)
with open("./test.txt", "r", encoding="utf-8") as f:
    context = f.readlines()
    print(context)
    # ['这是text第一行\n', '这是text第二行\n', '这是text第三行\n']

print("===" * 30)
with open("./test.txt", "r", encoding="utf-8") as f:
    some = enumerate(f)
    for index, context in enumerate(f):
        print(index, ":", context)
print("===" * 30)
# 文件写入
# write
with open("./test_1.txt", "w", encoding="utf-8") as f:
    f.write("写入对象1\n")
    f.write("写入对象2\n")
with open("./test_1.txt", "r", encoding="utf-8") as f:
    context = f.readlines()
    print(context)
# writelines
w_obj = ["今天是星期四\n", "今天是2026年1月29日\n", "今天外面下雪了\n"]
with open("./test_2.txt", "w", encoding="utf-8") as f:
    f.writelines(w_obj)
with open("./test_2.txt", "r", encoding="utf-8") as f:
    context = f.readlines()
    print(context)
"""
    模块3：文件指针操作
        （1）文件指针的位置返回 f.tell()
        （2）文件指针的移动 f.seek(参考位置，偏移量)
"""
with open("./test.txt", "r", encoding="utf-8") as f:
    context_3 = f.read(3)
    print("test.txt 前3个字内容:", context_3)
    print("当前文件的指针:", f.tell())
    # 将指针移向文件开头处
    f.seek(0, 0)
    context_else = f.read()
    print("test.txt 剩余的所有内容:", context_else)
    print("当前文件指针:", f.tell())
print("===" * 30)
"""
    模块4：高级操作--文件/目录管理
        （1）创建目录 os.mkdir()
        （2）查看目录内容 os.listdir() os.walk()
        （3）删除目录 os.rmdir(NULL) 
        （4）文件操作 os.rename(old,new) os.remove() 
        （5）常用方法 os.path.exists() os.path.isfile() os.path.isdir()
        （6）路径拼接 os.path.join(,,)
"""
import os

# os.mkdir("./test")

data = os.listdir()
print(data)
# ['1_Variables_and_Data_Types.py', '2_Operators_and_Expressions.py', '3_process_control.py', '4_Function_
# Basics.py', '5_container_structure.py', '6_file_operate.py', 'test', 'test.txt', 'test_1.txt', 'test_2.t
# xt', 'word']


data_2 = os.walk("./")
print(data_2)
print("===" * 30)
print(list(data_2))
# [('./', ['test', 'word'], ['1_Variables_and_Data_Types.py', '2_Operators_and_Expressions.py', '3_process
# _control.py', '4_Function_Basics.py', '5_container_structure.py', '6_file_operate.py', 'test.txt', 'test
# _1.txt', 'test_2.txt']), ('./test', [], []), ('./word', [], ['1_Python 数据类型分类详解.md', '2_Python
# 运算符核心类型及使用规则详解.md', '3_Python 流程控制语句及其应用详解.md', '4_Python 函数基础：掌握代码复
# 用的关键.md', '5_Python 四大核心数据结构整合示例：从基础用法到综合应用.md'])]


# os.rmdir("./test")

# os.rename("test_2.txt", "main.py")

# os.remove("test_2.txt")
print("===" * 300)
now_path = os.getcwd()
print(now_path)
if os.path.exists(now_path):
    print(f"{now_path}：存在")
else:
    print(f"{now_path}：不存在")
# 给当前路径拼接一个new
new_path = os.path.join(now_path, "new")
print(new_path)
if os.path.exists(new_path):
    print(f"{new_path}:存在")
else:
    print(f"{new_path}:不存在")

now_path = now_path + "\\test.txt"
print(now_path)
if os.path.isfile(now_path):
    print("当前传入是一个文件")
elif os.path.isdir(now_path):
    print("当前传入的是一个路径")
