# class 常见方法


class People:
    def __init__(self, name, age):
        """
        在初始化类对象时，会自动调用该方法
        不需要返回值
        """
        self.name = name
        self.age = age

    def __del__(self):
        """
        在资源被释放时调用，会自动调用该方法
        不需要返回值
        """
        print("当资源被释放时调用")

    def __str__(self):
        """
        当打印类对象时，会调用该方法
        需要返回值，需要将自定义输出结果返回
        """
        return f"[self]:self.name:{self.name};self.age:{self.age}"

    def change(self, new_name, new_age):
        self.name = new_name
        self.age = new_age

    def __call__(self, new_name, new_age):
        """
        将类对象以函数的方式调用时，会触发该方法
        并不需要返回值
        """
        self.name = new_name
        self.age = new_age

    def __eq__(self, other):
        """
        接收一个类对象 other.type=self.type
        需要返回值，返回值类型Bool
        进行数值比较，而不是地址比较
        """
        if isinstance(other, People):
            return other.name == self.name and other.age == self.age
        else:
            return False


# test __init__
people = People(name="jom", age=28)
print(people.name, people.age)

# test __str__
# 未自定义之前：<__main__.People object at 0x00000146DA81C6E0>
print(people)
# 自定义之后：[self]:self.name:jom;self.age:28

# test __call__
people.change("kom", 21)
people("tom", 99)
print(people.name, people.age)
print(people.name, people.age)

# is 和 ==
# is：判断地址
# ==：判断的是数值
# test __eq__
if people == 1:
    print("people 是 1")
else:
    print("people 不是 1")

people2 = People(name="tom", age=99)
if people == people2:
    print("相等")
else:
    print("不相等")

print(id(people), ";", id(people2))


if __name__ == "__main__":
    pass
