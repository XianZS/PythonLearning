"""
subprocess 标准库学习
"""

import subprocess

# 1、核心概念和安全注意事项
# 创建新的子进程，用来和新的子进程进行交互，获取子进程的输入、输出、错误和检查状态码。
# 尽量不要使用shell=True这个特性
# 2、基础操作
# 如何运行外部命令 subprocess.run()实现
# subprocess.run(args,shell=True/False,check=False/True,capture_output=False/True,text=False/True)
# 查看当前目录下，有哪些文件和文件夹
result = subprocess.run(["dir"], shell=True)
print(f"result:>>>\n{result}")
result_1 = subprocess.run(["ls"], shell=True)
print(f"result_1:>>>\n{result_1}")
# 0运行成功 1运行失败
# 使用shell特性，通配符处理
result_2 = subprocess.run("dir *.py", shell=True)
print(f"result_2:>>>\n{result_2}")
print("-" * 10)
# 3、获取命令的输出
# 最常用的场景，最重要！！！
# ls -l/dir的输出
cmd = ["cmd", "/c", "dir"]
res1 = subprocess.run(cmd, capture_output=True, text=True, check=True)
print(f"标准输出:{res1.stdout}")
print(f"标准错误:{res1.stderr}")
# 获取ping测试
print("-" * 10)
ping_cmd = ["ping", "-n", "2", "www.baidu.com"]
ping_res = subprocess.run(ping_cmd, capture_output=True, text=True)
print("Ping输出：")
print(ping_res.stdout)
# 错误处理和返回码
# check=True,CalledProcessError错误，可以捕捉到错误失败时的returncode、stdout、stderr。
print("=== 错误处理 ===")
try:
    res = subprocess.run(["不存在的命令"], capture_output=True, text=True, check=True)
except FileNotFoundError as e:
    print(e)
except subprocess.CalledProcessError as cpe:
    print(f"错误返回码:{cpe.returncode}")
    print(f"错误输出:{cpe.stdout}")
else:
    print("命令运行成功")

# 5、如何给命令提供输入
# 通过input参数给命令提供输入（文本模式下是字符串，二进制模式下是bytes）
# 假设下载需要给python解释器输入代码
print("=== 给命令提供输入 ===")
python_code = """
    print("hello from subprocess!")
    print(1+2+3)
"""

res = subprocess.run(["python"], input=python_code, capture_output=True, text=True)
print(res.stdout)
print(res)
print()
print()
print()
print()
# 6、高级用法
# popen
# 是底层类，比run更加灵活
# 需要实时获取输出的场景，需要与命令进行持续交互的场景
# Popen.poll() 检查命令是否完成，返回None就表示未完成，返回returncode就表示已经完成
# Popen.wait() 等待命令完成，实现阻塞功能
# Popen.communicate(input=None) 发送输入，获取输出/错误
# Popen.stdout/stderr 标准的输出或者错误的文件对象
print("Popen 实时获取输出")
ping_cmd = ["ping", "-n", "4", "www.baidu.com"]
with subprocess.Popen(
    ping_cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
    universal_newlines=True,
) as proc:
    for line in proc.stdout:  # type:ignore
        print(line, end="")
# 7、常见应用场景
# 调用系统工具：git ffmpeg
# 批量处理文件：shell命令批量重命名等一些操作
# 检查系统状态：ping检查网络状态 df检查磁盘空间状态 ps查看进程状态
# 调用其它脚本：运行其它python脚本
# 自动化任务：（Linux）cron或者（Windows）任务计划程序，定时执行命令
