class Name:
    def __init__(self, input_name):
        self.name = input_name

    def pr(self):
        print(f"name >>> {self.name}")
        print(self, type(self))


print(type(Name))

name_obj = Name(input_name="jom")
print(type(name_obj))
print(type(name_obj.name))
print(type(name_obj.pr))
name_obj.pr()


class MySystem:
    def __init__(self, user_name, user_password):
        self.__user_name = user_name
        self.__user_password = user_password

    def pr(self):
        print(f"username:{self.__user_name},user_password:{self.__user_password}")


system = MySystem("admin", "admin123")
print(system._MySystem__user_password)  # type:ignore


if __name__ == "__main__":
    pass
