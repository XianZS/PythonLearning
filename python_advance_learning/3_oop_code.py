"""
1.OOP概念解读，以及基础实现。
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

print("=" * 30)

"""
2.封装
"""


# 封装用户信息
class User:
    # user_name="shjenm"
    def __init__(self, user_name, user_password, user_address, user_details):
        self.user_name = user_name
        # password 应该具备“私有属性”
        self.__user_password = user_password
        self._user_address = user_address
        self._user_details = user_details


user_1 = User(
    user_name="jom", user_password="jom123", user_address="H市", user_details="详细信息"
)

print(user_1.user_name)
print(user_1._user_address)
print(user_1._user_details)

# 并不存在真正的私有，只是对响应的私有属性，进行了后台重命名处理
# User __user_password
# _User__user_password
# _类名__私有属性名
print(user_1._User__user_password)  # type:ignore

print()


# 访问器
# @property
# 修改器
# 修改对象.setter(self,传入参数)
class Stu:
    def __init__(self, stu_name):
        self.__stu_name = stu_name

    # 实现私有属性的get方法
    def get_stu_name(self):
        return self.__stu_name

    # 实现私有属性的set方法
    def set_stu_name(self, new_stu_name):
        self.__stu_name = new_stu_name


stu = Stu("student")
# 以函数形式访问的get_stu_name
print(stu.get_stu_name())
stu.set_stu_name("jom")
print(stu.get_stu_name())

print()


class NewStu:
    def __init__(self, stu_name):
        self.__stu_name = stu_name

    # 使用property这个装饰器，装饰私属性的get方法，
    # 然后就可以将它的get方法
    # 以属性字段的形式进行访问
    # 【访问器】
    @property
    def get_stu_name(self):
        return self.__stu_name

    # 【修改器】
    @get_stu_name.setter
    def set_stu_name(self, new_stu_name):
        self.__stu_name = new_stu_name


new_stu = NewStu("student")
# 以属性字段的形式访问的get_stu_name
print(new_stu.get_stu_name)
new_stu.set_stu_name = "kom"
print(new_stu.get_stu_name)

print()


class People1:
    def __init__(self, people_name, people_address):
        self.people_name = people_name
        self.people_address = people_address

    # 内层：内层方法理论上是不允许被访问的
    def __format_people_details(self):
        return f"{self.people_name}居住在{self.people_address}城市之中"

    def __format_people_somethings(self):
        return "额外信息如下:"

    # 表层：表层的方法可以被访问
    def super_format(self):
        # 先得到起始的详细信息
        res_1 = self.__format_people_details()
        res_2 = self.__format_people_somethings()
        return res_2 + "\n" + res_1


people_1 = People1(people_name="kom", people_address="A市")
res = people_1.super_format()

print(res)

print("=" * 30)

"""
    继承
    1.如何实现
    2.单继承
    3.多继承
"""


# （1）继承如何实现？
# 将公共的部分抽象出来，作为父类，然后让每个小类去继承这个父类
# 就充分体现了代码的模块化和可复用性
class Animal:
    def __init__(self, animal_name, animal_note):
        self.animal_name = animal_name
        self.__animal_note = animal_note

    def call(self, how_make):
        pass

    def have_foot(self, number):
        pass


# 狗 属于动物
class Dogi(Animal):
    pass


dog = Dogi(animal_name="狗", animal_note="我是一条狗")
print(dog.animal_name)
print(Dogi.__mro__)


# 猫 属于动物
class Cat(Animal):
    pass


cat = Cat(animal_name="猫", animal_note="我是一条猫")
print(cat.animal_name)


"""
    单继承？
    一个子类，只继承一个父类
    在单继承之中，调用父类的魔法函数，它的语法规范是：
        `父类.对应方法()`
"""


class People:
    def __init__(self, people_name, people_type):
        # public 公有属性
        self.people_name = people_name
        # private 私有属性
        self.__people_type = people_type

    def hi(self, say_somethings):
        pass

    # 在父类中定义了一个私有的方法
    def __get_people_type(self):
        return self.__people_type


class Worker(People):
    def __init__(self, people_name, people_address):
        People.__init__(self, people_name=people_name, people_type="工人")
        self.people_address = people_address

    # 复写People父类的init初始化函数
    # 复写People父类的打招呼函数
    def hi(self, say_somethings):
        print(f"{self} say :‘{say_somethings}’!")

    # 在父类的基础上拓展函数
    def get_address(self):
        return self.people_address

    # 【测试】：子类worker能否继承people的私有属性 self.__people_type
    # 子类不可以继承父类的私有属性
    # def get_test_people_type(self):
    # return self.__people_type

    # 【测试】：子类能否继承父类的私有方法
    # def test_method(self):
    # self.__get_people_type()


worker = Worker(people_name="工人", people_address="第13号工地")
print(worker.people_name, worker.people_address)
# 调用来自于父类的函数方法
worker.hi(say_somethings="我正在说话")
# 调用子类自定义的函数方法
print(worker.get_address())
# worker.get_test_people_type()
# worker.test_method()


"""
    多继承？
    python支持多继承
    引入两个知识点：
        - 多继承的继承顺序
        - 多继承的MRO机制
"""


class Goods:
    def say(self):
        pass


class Things(Goods):
    def say(self):
        print("Things Class")


class Shape(Goods):
    def say(self):
        print("Shape Class")


class Pen(Things, Shape):
    def use_say(self):
        super().say()


pen = Pen()
pen.use_say()
# 如何确定 pen 调用的到底是哪个父类？
# MRO 机制 应对 多继承
mro_list = Pen.__mro__
for cho in mro_list:
    print(cho)

"""
<class '__main__.Pen'>
<class '__main__.Things'>
<class '__main__.Shape'>
<class '__main__.Goods'>
<class 'object'>
"""


print("=" * 30)

"""
    多态
"""


class A:
    def __init__(self, animal_name):
        self.animal_name = animal_name

    def call(self):
        # 只是定义了有call这个动作
        # “叫” 这个动作
        pass


class MyCat(A):
    def __init__(self, animal_name):
        super().__init__(animal_name)

    def call(self):
        print("喵喵喵")


class MyDog(A):
    def __init__(self, animal_name):
        super().__init__(animal_name)

    def call(self):
        print("汪汪汪")


# 多态 针对同一个方法，有不同的实现方式
# （入口）可以确定的：只有一个方法
# （出口）不可以确定的：实现方式


def call_function(my_obj):
    # 不需要关心 call_function 内部的实现方式
    # 咱们只需要知道有这个 call 这个方法
    # 不需要知道它的内部实现方式
    # my_obj.call()
    try:
        my_obj.call()
        return True
    except Exception as e:
        print(e)
        return False


my_cat = MyCat("咪咪")
my_dog = MyDog("旺财")
# my_cat.call()
# my_dog.call()
call_function(my_cat)
call_function(my_dog)


# Python 动态类型语言
# 鸭子类型
# 在现实世界之中，是如何定义一个事物的？
# 键盘：有按键 可输入 可连接电脑
# 假设只要满足这三个要求，就可以被称为一个键盘
# 物品B：有按键 可输入 可连接电脑
# 那么它可不可以被成为键盘？
# 答案：可以
# 只要物品B满足三个条件，那么它就是一个键盘，不管他本身是不是一个键盘


class KeyBoard:
    def __init__(self):
        self.a = "有按键"
        self.b = "可输入"
        self.c = "可连接电脑"


key_board = KeyBoard()


class B:
    def __init__(self, a_judge, b_judge, c_judge):
        self.a = a_judge
        self.b = b_judge
        self.c = c_judge


b = B(True, True, True)
# b 是不是一个键盘？
# b 就是一个键盘
# 不管 b 本质上是不是一个键盘
# 只要 b 满足了键盘的要求
# 那么就是一个键盘


if __name__ == "__main__":
    pass
