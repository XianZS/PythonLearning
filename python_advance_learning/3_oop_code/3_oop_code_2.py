# 类属性 VS 实例属性
class People:
    # 类属性
    count_people = 0
    # 只要创建一个 people 对象，就让 count_people加1

    # 实例属性
    def __init__(self, people_name, people_age):
        self.people_name = people_name
        self.people_age = people_age
        self.change()

    def change_1(self):
        pass

    @classmethod
    # 更改类属性
    def change(cls):
        cls.count_people += 1


# 如何更改实例属性？
# 共享性：不共享
# 类对象.实例属性名
people1 = People(people_name="jom", people_age=19)
people2 = People(people_name="kom", people_age=22)
print(f"【实例属性】更改之前的结果为:{people1.people_age}")
people1.people_age = 99
print(f"【实例属性】更改之后的结果为:{people1.people_age}")
print(f"【实例属性】更改之前的结果为:{people2.people_age}")


print("=" * 30)


print(people1.count_people)
print(people2.count_people)

people3 = People(people_name="tom", people_age=100)
print(people3.count_people)
print(people2.count_people)


# 类方法
# 实例方法
# 静态方法
class User:
    # 类属性（共享）
    user_statement = True

    def __init__(self, user_name, user_password):
        # 实例属性（不共享）
        self.user_name = user_name
        self.user_password = user_password

    @classmethod
    def class_method_function(cls, judge: bool):
        """类方法"""
        cls.user_statement = judge

    def state_method_function(self, new_user_name):
        """实例方法"""
        self.user_name = new_user_name

    @staticmethod
    def add(a, b):
        """静态方法：定义与“类”和“类对象”无关的方法"""
        return a + b


user = User(user_name="admin", user_password="admin123")
user.class_method_function(judge=False)

user2 = User(user_name="jom", user_password="jom123")
print(user2.user_statement)

user2.state_method_function(new_user_name="hom")
print(user2.user_name)

print(user2.add(2312, 321233))
