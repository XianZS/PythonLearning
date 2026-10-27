"""
argparse 标准库学习
"""

import argparse as ap
from ast import arg
from os import read
from pathlib import Path

# 1、核心概念和基础使用流程
# argparse是将命令行输入的字符串，解析成结构化的python对象，自动完成一系列重复动作。
# 创建解析器：ArgumentParser()
# ap_obj = ap.ArgumentParser(description="这是解析器")
# # 添加参数：add_argument()
# ap_obj.add_argument("user", help="登录的用户")
# ap_obj.add_argument("password", help="登录的密码")
# # 解析参数：parse_args()
# args = ap_obj.parse_args()
# # 使用参数：args.xxx 来进行参数的使用
# print(f"[args]:{args},type:{type(args)}")
# 自动将参数按照顺序进行解析，然后按照顺序赋值给argument
# 2、必选参数
# 位置参数
# 位置参数是按照顺序传递的必选参数，不需要添加--前缀，用户必须按照我们自定义的顺序进行传入，如果不传入就会报错
# apobj2 = ap.ArgumentParser(description="必选参数调试")
# apobj2.add_argument("filename", help="文件名", type=str)
# apobj2.add_argument("encoding", help="编码方式", type=str)
# args = apobj2.parse_args()
# print(f"[args]:{args}")
# 3、可选参数
# 可选参数是带着--前缀的参数，也叫做长选项，是最常用的参数类型
# p1 = ap.ArgumentParser(description="可选参数")
# # obj.add_argument(-短选项，--长选项，help="提示信息"，required=Bool，type=类型)
# p1.add_argument("-n", "--name", help="用户姓名", required=True, type=str)
# p1.add_argument("-a", "--age", help="用户年龄", default=18, type=int)
# # 开关参数
# p1.add_argument("-d", "--debug", help="调试", action="store_true")
# args = p1.parse_args()
# print(f"[args]:{args}")


# 4、参数类型和合法性检验
# sys.args拿到的所有参数都是字符串，需要手动转化类型
# 检验端口号，端口号必须要在1~65535之间
# def check_port(port_str):
#     try:
#         port = int(port_str)
#     except ValueError:
#         raise ap.ArgumentTypeError("端口号必须是整数")
#     if not 1 <= port <= 65535:
#         raise ap.ArgumentTypeError("端口号范围不合法")
#     return port
#
#
# p2 = ap.ArgumentParser(description="端口号检验解析器")
# # 第一种写法：原生的检验类型
# p2.add_argument("--num", help="一个数字", type=float, required=True)
# # 第二种写法：自定义的检验类型
# p2.add_argument("--port", help="端口号", type=check_port, default=8000)
# args = p2.parse_args()
# print(f"num:{args.num}")
# print(f"port:{args.port}")
# 5、进阶用法：子命令系统 27
# 创建主解析器
mainp = ap.ArgumentParser(description="主解析器", prog="filetool")
mainp.add_argument("-v", "--version", help="输出版本号", action="store_true")
# 创建子解析器
childp = mainp.add_subparsers(dest="command", title="支持的子命令", required=True)
read_opt = childp.add_parser("read", help="读取文件内容")
# 设置子命令自己的参数
read_opt.add_argument("filename", help="要读取的文件路径", type=str)
read_opt.add_argument("-n", "--line-numbers", help="显示行号", action="store_true")
# 添加第二个子命令
read_opt = childp.add_parser("write", help="写入文件内容")
args = mainp.parse_args()
print(args)
if args.command == "read":
    print("正在执行子命令")
else:
    print("没有在执行子命令")
# 6、如何优化帮助文档
# 在创建解析器时，执行优化帮助文档
parser = ap.ArgumentParser(
    description="""
            优化帮助文档
            dhuihioq
            dguqwfhoiq
            fqhiwj
        """,
    # 结尾的补充说明
    epilog="""
        结尾的补充说明
        dihqidhqoi
        dsahiwdhoi
        """,
)
