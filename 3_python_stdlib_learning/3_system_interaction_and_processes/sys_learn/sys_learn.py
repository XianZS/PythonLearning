"""
sys 标准库学习
"""

import sys

# 1、核心概念
# sys是python的内置库，主要负责内容：
# 和python解释器进行交互、和操作系统进行交互、管理python运行时的环境、
# 常用函数学习
# 2、常用功能解析
# sys.argv() 脚本参数的入口，存储了命令行传递给脚本的所有参数
als = sys.argv
print(f"命令行所有参数为:{als},type:{type(als)}")
print(f"第一个参数:{als[0]}")  # 第一个参数是当前文件的文件名
# 处理参数
if len(als) > 1:
    print(f"传递的参数为:{als[1:]}")
    try:
        index = 1
        for cho in als[1:]:
            print(f"[ARGS-{index}]:{cho}")
            index += 1
    except Exception as e:
        print(e)
else:
    print("没有传入任何参数-程序正在主动退出")
    # 主动推出python程序，语法规范是:sys.exit(status)
    # sys.exit(0)

print("-" * 10)

# 如何解决 ModuleNotFoundError 报错
# 通常情况下，在导入python的一个模块之后，python程序会根据sys.path之中的所有路径进行查找，如果没有查找到就会报 ModuleNotFoundError
for i, path in enumerate(sys.path, 1):
    print(f"[{i}].{path}")

print("正在将桌面路径添加到环境之中")
sys.path.append("C://Users//XianZS//Desktop")

for i, path in enumerate(sys.path, 1):
    print(f"[{i}].{path}")
# import test_module  # type:ignore
#
# print(test_module.main())
# 如果处理标准输入、标准输出、错误流
# sys.stdin：标准输入
print("请再输入一行文字:")
line = sys.stdin.readline().strip()
print(f"你的输入文字为:{line}")
# sys.stdout：标准输出
sys.stdout.write("这是通过sys.stdout打印的文字\n")
# sys.stderr：错误流
sys.stderr.write("这是一条错误信息，通过sys.stderr,write所输出的错误信息\n")
print("-" * 10)
# 如何获取系统与解释器信息
print(f"python版本信息:{sys.version}")
print(f"python版本信息-更加详细:{sys.version_info}")
print(f"获取当前程序运行的平台:{sys.platform}")
print(f"python解释器的可执行文件路径:{sys.executable}")
print(f"python解释器的默认编码方式:{sys.getdefaultencoding()}")
# 如何查看对象占用的内存空间大小
print(f"int类型占用的空间大小为:{sys.getsizeof(1)}")
print(f"char类型占用的空间大小为:{sys.getsizeof('c')}")
print(f"list类型占用空间大小为:{sys.getsizeof(['a', 'b', 'c', 'd'])}")
# 只是计算容器本身的大小，比如说列表的大小，并不会列表内元素本身的大小。
# 重置递归深度的大小
# python为了防止栈溢出，默认递归深度的大小为1000
print(f"当前的递归深度为:{sys.getrecursionlimit()}")
sys.setrecursionlimit(2000)
print(f"修改之后-当前的递归深度为:{sys.getrecursionlimit()}")


# 3、system标准库的常见应用场景
# 脚本开发：sys.argv来进行传递参数 sys.exit来进行程序的主动退出
# 模块导入问题：sys.path动态添加模块所在路径
# 日志与输出：sys.stdin、sys.stdout、sys.stderr来进行输入、输出和信息调错
# 跨平台和兼容性：sys.pathform得到平台信息 sys.version_info 得到详细信息
# 性能调试：sys.getsizeof查看对象内存大小
# 4、实战案例——建议命令行系统信息工具
print("-" * 10)


class SystemInfoTool:
    def __init__(self):
        # 检查参数数量
        if len(sys.argv) < 2:
            # 如果没有传入参数，那么就提示相关用法，并且主动退出python程序
            self.show_usage()
            sys.exit(0)
        self.arg = sys.argv[1]
        self.run()

    def show_usage(self):
        """
        显示用法
        """
        print("=== 命令行简易信息管理工具 ===")
        print("参数列表:")
        print("--version    打印python版本信息")
        print("--platform   打印系统平台")
        print("--path       打印模块搜索路径")
        print("--all        打印所有信息")

    def print_version(self):
        print("=== python版本 ===")
        print(sys.version)
        print(
            f"主版本:{sys.version_info.major}，次版本:{sys.version_info.minor}，微版本:{sys.version_info.micro}"
        )

    def print_platform(self):
        print("=== 系统平台 ===")
        print(sys.platform)
        if sys.platform == "win32":
            print("当前系统：Windows")
        elif sys.platform == "darwin":
            print("当前系统：macos")
        elif sys.platform.startswith("linux"):
            print("当前系统：Linux")
        else:
            print("当前系统：其它操作系统")

    def print_path(self):
        print("打印模块搜索路径")
        for i, path in enumerate(sys.path, 1):
            print(f"[{i}].{path}")

    def print_all(self):
        print("打印所有信息")
        self.print_version()
        self.print_platform()
        self.print_path()

    def run(self):
        """
        工具管理启动入口
        """
        if self.arg == "--version":
            self.print_version()
        elif self.arg == "--platform":
            self.print_platform()
        elif self.arg == "--path":
            self.print_path()
        elif self.arg == "--all":
            self.print_all()
        else:
            print("参数错误")
            self.show_usage()
            sys.exit(1)


def test():
    SystemInfoTool()


if __name__ == "__main__":
    test()
