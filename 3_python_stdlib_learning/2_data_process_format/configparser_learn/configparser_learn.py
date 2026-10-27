"""
configparser stdlib learn
1、ini文件核心概念
2、读取ini文件
（1）创建解析器对象
（2）加载配置文件
（3）读取配置
（4）判断节/配置项是否存在
3、创建、写入、修改配置文件
4、进阶实战部分
5、实战案例
"""

import configparser as cp
from pathlib import Path


# 1、ini文件结构
# 节和键值对
# 节：[]
# 键值对：=

# 2、如何读取配置文件
# 创建conf文件读取对象
conf = cp.ConfigParser()
# 读取文件信息
conf.read(filenames="./config.ini", encoding="utf-8")
# 查看相关内容
print(f"config:{conf},type:{type(conf)}")
# 通过文件对象，访问节，就可以得到节里面的所有键值对
database_things = conf["DATABASE"]
db_dicts = dict(database_things)
print("database节之中的内容:")
print(db_dicts)
ui_dicts = dict(conf["UI"])
print("ui节之中的内容:")
print(ui_dicts)

# 精准访问
# conf.get(节对象,key对象) >>> value对象
password = conf.get("DATABASE", "password")
print(f"password:{password}")

# 判断database节之中，是否有create_time和user这两个key
j1 = conf.has_option("DATABASE", "create_time")
j2 = conf.has_option("DATABASE", "user")
print(f"database-create_time:{j1}；database-user:{j2}")
# 判断节是否存在
j3 = conf.has_section("DATABASE")
print(f"DATABASE:{j3}")
als = conf.sections()
print(als)

print("-" * 10)
# 3、如何进行创建、写入和修改配置文件
# 步骤一：从0创建配置文件
# 步骤二：添加节、添加/修改配置项
# 步骤三：保存到文件
# 步骤四：删除节/配置项

# 创建解析器
c = cp.ConfigParser()
# 添加节
c.add_section("redis")
c.add_section("openai")
c.add_section("deepseek")
als_sections = c.sections()
print(f"自定义配置文件之中的所有节对象为:{als_sections}")
# 给节添加配置项，也就是给节添加键值对
# conf.set(节，配置项-key，配置项-value)
c.set("redis", "user", "admin")
c.set("redis", "password", "admin123")
c.set("redis", "port", "10086")
c.set("openai", "key", "dhjahduwhuifgqhkjlndbqwigfioq")
c.set("deepseek", "key", "dji0agdfugqwuidgfyuiqwfguqgidgi")
redis_als = dict(c["redis"])
print(redis_als)
# 实现配置项的修改
c.set("redis", "password", "123456")
new_redis_als = dict(c["redis"])
print(new_redis_als)
# 删除
# 删除-配置项
c.set("openai", "user", "root")
openai_als = dict(c["openai"])
print(f"openai修改之前为:{openai_als}")
c.remove_option("openai", "user")
openai_als = dict(c["openai"])
print(f"openai修改之后为:{openai_als}")
# 删除-节
sections_als = c.sections()
print(f"删除之前，所有的节对象为:{sections_als}")
c.remove_section("deepseek")
sections_als = c.sections()
print(f"删除之后，所有的节对象为:{sections_als}")
# 存储-存储到文件之中
with open("c.ini", mode="w", encoding="utf-8") as f:
    c.write(f)
print("配置文件写入成功")


# 4、实战应用技巧
# 如何在读取时设置默认值
config = cp.ConfigParser()
config.read(filenames="./config.ini", encoding="utf-8")
# 得到database节之中的port配置项
db_port = config.get("DATABASE", "port", fallback="3306")
print(f"db_port:{db_port}")
# 如何多行处理
desc = config.get("OPT", "desc", fallback="无描述")
print(desc)
# 如何兼容大小写


# 5、简易程序配置器的创建
# 在程序启动时，自动加载ini配置文件
# 如果文件不存在，自动生成默认配置
# 支持：查看配置、修改配置、保存配置
# 读取数据和界面配置，用于系统启动
class AppCofig:
    def __init__(self, file_path="app.ini"):
        self.file_path = Path(file_path)
        self.conf = cp.ConfigParser()
        # 加载配置，如果不存在，就自动进行初始化
        self.load_config()

    def load_config(self):
        """
        加载配置，文件不存在则创建默认配置
        """
        if self.file_path.exists():
            self.conf.read(self.file_path, encoding="utf-8")
            print("配置文件加载成功")
        else:
            self.create_default_config()
            print("默认配置文件生成成功")

    def create_default_config(self):
        """
        创建默认配置
        """
        self.conf.add_section("DATABASE")
        self.conf.set("DATABASE", "host", "localhost")
        self.conf.set("DATABASE", "user", "admin")
        self.conf.add_section("THEME")
        self.conf.set("THEME", "color", "red")
        self.save_config()

    def save_config(self):
        with open(self.file_path, mode="w", encoding="utf-8") as f:
            self.conf.write(f)

    def select_section(self):
        selections_als = self.conf.sections()
        print(selections_als)

    def select_opt(self, section):
        opts_dict = dict(self.conf[section])
        print(opts_dict)

    def update_opt(self, section, option, value):
        if not self.conf.has_section(section):
            print("节不存在")
            return False
        else:
            self.conf.set(section, option, value)
            self.save_config()
            print("修改成功")
            return True


def test():
    # 测试创建解析器对象
    app = AppCofig()
    # 测试查看节对象
    app.select_section()
    # 测试查看配置项
    app.select_opt("DATABASE")
    # 测试修改
    app.update_opt("DATABASE", "user", "root")
    # 查看修改结果
    app.select_opt("DATABASE")


if __name__ == "__main__":
    test()
