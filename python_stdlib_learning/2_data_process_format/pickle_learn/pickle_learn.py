"""
pickle 标准库学习
"""

import pickle


# 1、核心概念
# 序列化？反序列化？
# 序列化：python对象 》》》 字节流
# 序列化：字节流 》》》 python对象
# Python专属，不可以进行跨语言操作，支持python所有的对象

# 2、如何在内存之中实现序列化和反序列化？
data = {
    "name": "admin",
    "password": "admin123",
    "classes": ["数学", "英语", "C语言"],
    "scores": [11, 22, 33],
    "is_student": True,
}
print(data)
# 序列化操作
# 序列化操作：pickle.dumps(python对象)
bytes_data = pickle.dumps(data)
print(f"转换之后的二进制字节流为:{bytes_data},type:{type(bytes_data)}")
# 反序列化操作：pickle.loads(bytes_obj)
res = pickle.loads(bytes_data)
print(f"反序列化之后res的结果为:{res}")
# 3、如何将序列化和反序列化之后的结果保存到硬盘之中
# 序列化：pickle.dump(obj,file)
# 反序列化：pickle.dump(file)
with open("./test.pkl", mode="wb") as f:
    pickle.dump(data, f)
    print("数据保存成功")

with open("./test.pkl", mode="rb") as f:
    load_data = pickle.load(f)
    print(f"load_data:{load_data}")


# 4、进阶：序列化自定义的实例对象
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def say_hello(self):
        print(f"大家好，我的名字是:{self.name}")


stu = Student(name="admin", age=123, score=99)

# 自定义类对象的序列化操作
with open("./student.pkl", mode="wb") as f:
    pickle.dump(stu, f)
    print("学生信息已经保存")

# 自定义类对象的反序列化操作
with open("./student.pkl", mode="rb") as f:
    read_data = pickle.load(f)
    print("-" * 10)
    print(read_data)
    read_data.say_hello()


# 5、安全警告部分
def test():
    """
    !!!恶意代码
    """
    import pickle
    import os

    class Evil:
        def __reduce__(self):
            return {os.system, "echo恶意代码提示信息"}

    evil_data = pickle.dumps(Evil())


# 6、常见应用场景
# 【程序状态保存情况】
# 游戏存档
# 编辑器的草稿
# 【复杂数据缓存情况】
# 在机器学习结束之后，可以把模型对象，存储成pickle文件
# 爬虫爬取的复杂数据，可以暂时把多层嵌套数据存储成pickle文件，然后等待统一的处理
# 【在短时间内，实现python不同进程之间的数据传输】
# 在不同项目之间，可以使用pickle来传递复杂对象
#
