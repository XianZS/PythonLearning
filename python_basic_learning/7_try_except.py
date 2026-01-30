"""try-except 异常捕捉模式"""

# 1.基础概念和异常结构

some = [1, 2, 3]
# print(some[5])
# IndexError: list index out of range
# IndexError 异常类型
# list index out of range 异常的详细信息
# ZeroDivisionError: division by zero
# ZeroDivisionError 异常类型
# division by zero 异常的详细信息
# try-except:
try:
    # 你需要执行的代码片段
    print(some[5])
except Exception as e:
    # 当发生异常时，会触发此处的代码片段的执行操作
    print("不可以访问some之中下标为5的元素")
    print(e)
# 2.指定异常捕捉 （单/双）
try:
    b = 0
    c = 1
    d = c / b  # d=1/0
    a = some[4]
except IndexError:
    print("[IndexError]:发生异常")
except ZeroDivisionError:
    print("[ZeroDivisionError]:发生异常")

try:
    b = 0
    c = 1
    d = c / b  # d=1/0
    a = some[4]
except (IndexError, ZeroDivisionError):
    print("===发生异常===")

# 3.捕捉异常详情
try:
    b = 0
    c = 1
    d = c / b  # d=1/0
    a = some[4]
except (IndexError, ZeroDivisionError) as e:
    print(f"异常信息为e:{e}")
print("===" * 30)
# 4.else 无异常时执行
adict = {"name": "jom", "age": 18, "details": "详细信息"}
print(f"adict:{adict}")
try:
    # 代码执行板块
    adict[("test")] = ["test"]
except Exception as e:
    # 【代码发生错误】触发
    print("已经触发错误", e)
else:
    # 【代码不发生错误】触发
    print("没有触发错误")

# 5.finally 有无异常都执行:无论是否发生异常，都会执行finally所指向的代码逻辑
data = [1, 2, 3]
try:
    a = data[1]
    print(a)
except IndexError as e:
    print(f"(except) >>> [IndexError]:{e}!!!")
else:
    print("(else) >>> ")
finally:
    print("(finally) >>> 无论是否发生错误都会执行")
    del data

print("===" * 30)

# 6.主动抛出异常 raise
name: str = input("请输入一个name，其中1<name.size<9: ")
try:
    if len(name) <= 1 or len(name) >= 9:
        raise ValueError("在设置name时，name的长度应该在合法范围之内")
    else:
        print("设置成功")
except ValueError as e:
    print(f"[ValueError]:{e}")


# 7.自定义异常 Exception
class My_Exception(Exception):
    def __init__(self, *args: object) -> None:
        print(f"args:{args}")
        # super().__init__(异常详情)
        super().__init__("这是我的自定义异常详情")


try:
    raise My_Exception("自定义")
except My_Exception as e:
    print("My_Exception", e)


class PassWordLengthCheckError(Exception):
    def __init__(self, details, *args: object) -> None:
        super().__init__(f"异常参数:{args},异常详情：{details}")


class PasswordTypeCheckError(Exception):
    def __init__(self, details, *args: object) -> None:
        super().__init__(f"异常参数:{args},异常详情：{details}")


password: str = input("请在此处输入密码: ")
try:
    if len(password) <= 1 or len(password) >= 6:
        raise PassWordLengthCheckError("密码长度不符合规范", "无异常的其它参数")
    else:
        # 密码不能出现 除数字或字母之外的任何字符
        data = []
        import string

        data.extend(string.ascii_lowercase)
        data.extend(string.ascii_uppercase)
        data.extend(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
        print(f"{data}")
        for value in password:
            if value not in data:
                raise PasswordTypeCheckError("密码不符合预定义规范", "无异常的其它参数")
        print("设置成功")
except PassWordLengthCheckError as e:
    print(f"[PassWordLengthCheckError]:{e}")
except PasswordTypeCheckError as e:
    print(f"[PasswordTypeCheckError]:{e}")


#
#
#
