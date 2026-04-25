"""
string 标准库学习
"""

import string
import random
from string import Template

# 1、预定义字符串常量
# 获取所有的大小写字母
print(list(string.ascii_letters))
# 获取所有的小写字母/获取所有的大写字母
print(f"[小写字母]:{string.ascii_lowercase}")
print(f"[大写字母]:{string.ascii_uppercase}")
# 获取其它参数
print(f"[所有数字]:{string.digits}")
print(f"[所有标点符号]:{string.punctuation}")
print(f"[所有的空白字符]:{string.whitespace}")
# 2、设置单词首字母大写
# string.capwords(s,sep=None)
# s：需要处理的字符串
# sep：单词分隔符
text = "hello,world,from,python"
res = string.capwords(text)
print(f"[分隔符:空格]首字母大写之后的结果为:{res}")
new_res = string.capwords(text, sep=",")
print(f"[分隔符:,]首字母大写之后的结果为:{new_res}")
# 3、安全字符串模板
# template=string.Template("包含 $占位符 的字符串")
# template.substitute(占位符1=数值1,占位符2=数值2)
# template.safe_substitute(...):如果在替换过程之中，出现缺少占位符的情况，那么就保留占位符，不报错。
template = string.Template("大家好,我是 $name ,我今年 $age 岁")
res = template.substitute(name="jom", age=22)
print(res)
safe_res = template.safe_substitute(name="kom")
print(safe_res)


# 进阶-1：自定义template分隔符
# 语法规范：继承Template类，然后重写delimiter方法以及idpattern方法
class MyTemplate(string.Template):
    delimiter = "%"  # 自定义分隔符设置为%
    idpattern = r"[a-zA-Z_]+"  # 占位符名称规则：字母或者下划线开头


# 使用自定义分隔符模板
template = MyTemplate("我是一名 %people_type , 我的名字是 %name !")
res = template.substitute(people_type="学生", name="jom")
print(f"自定义分隔符返回对象:{res}")


# 进阶-2：使用random生成随机字符串
def generate_password(length=12):
    """
    返回随机字符串，需要设置随机字符串的长度，默认长度为12
    """
    import string
    import random

    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(length))
    return password


for index in range(3):
    print(f"[INFO-{index}+1]:{generate_password((index + 1) * 3)}")


# 进阶-3：string标准库的高级字符串格式化
# string.Formatter()的底层是str.format()
# 需要继承string.Formatter类，重写format_field()方法
class CurrencyFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        if format_spec == "currency":
            return f"${value:.2f}"
        elif format_spec == "string":
            return f"${value}"
        return super().format_field(value, format_spec)


# 测试使用自定义的formatter对象
formatter = CurrencyFormatter()
res = formatter.format("商品价格:{price:currency}", price=19.9)
res1 = formatter.format("商品名称:{name:string}", name="香蕉")
print(res)  # 商品价格:$19.90
print(res1)


# 实战案例：实现用户信息注册工具
# - 验证用户的用户名是否合法
# - 生成随机初始密码
# - 格式化用户姓名
# - 用模板生成欢迎消息
class UserRegistrationTool:
    def __init__(self):
        # 定义合法用户名的字符集合
        self.valid_username_chars = set(string.ascii_letters + string.digits + "_")

    def valid_username(self, username):
        """验证用户名是否合法"""
        if not username:
            return False, "用户名为空，请先输入用户名"
        for char in username:
            if char not in self.valid_username_chars:
                return False, f"用户名之中包含非法字符:{char}"
        return True, "用户名合法"

    def generate_initial_password(self, length=10):
        """生成随机初始密码"""
        chars = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(chars) for _ in range(length))

    def format_name(self, name):
        return string.capwords(name)

    def generate_welcome_message(self, name, username):
        """生成欢迎消息"""
        template = Template(
            "欢迎 $formatted_name 加入，你的用户名是: $username ，请妥善保管您的初始密码"
        )
        formatted_name = self.format_name(name)
        return template.safe_substitute(
            formatted_name=formatted_name, username=username
        )


if __name__ == "__main__":
    tools = UserRegistrationTool()
    # 模拟用户的输入
    raw_name = "li si"
    username = "lisi_2026"
    # 验证用户名
    is_valid, msg = tools.valid_username(username)
    print(f"[用户名验证]:{msg}")
    # 生成随机初始密码
    if is_valid:
        password = tools.generate_initial_password()
        print(f"[初始密码]:{password}")
        welcome_msg = tools.generate_welcome_message(raw_name, username)
        print(f"[欢迎消息]:{welcome_msg}")
