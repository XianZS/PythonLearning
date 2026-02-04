"""
什么是OOP?
OPP面向对象编程，将现实世界中某些事物所具有的属性和动作抽象起来。
小狗：
    属性：狗名、狗年龄、狗的种类、狗的颜色
    动作：叫、摇尾巴、吃
小狗抽象为类
    属性也对应的是属性
    动作：魔法方法
OOP的组成部分？
（1）class 类 （狗这个大类）
（2）object 对象 （每一条狗）
（3）attribute 属性
（4）method 方法
"""


# 养一条狗
class Dog:
    dog_name = "小红"
    dog_age = 3
    dog_color = "棕色"
    dog_type = "藏獒"

    def call(self):
        print("狗在叫")

    def make(self):
        print("狗在摇尾巴")


# 定义三条狗 object
# obj.属性
# obj.方法()

dog_1 = Dog()
print(f"dog_1 name is {dog_1.dog_name}")

dog_2 = Dog()
dog_2.call()

dog_3 = Dog()
dog_3.make()

if __name__ == "__main__":
    pass
