"""
platform 标准库
"""

import platform
import logging
from typing import Dict

# 1、基础概念和快速入门
# platform 和 (os/sys)标准库之间的区别
# platform：全维度信息，标准库返回值，系统/硬件/python解释器信息
# os/sys：os系统名，syspython解释器，信息获取维度有限
# 一键获取核心平台信息
sys_als_things = platform.system()
print(f"操作系统类型：{sys_als_things}")
print(f"操作系统完整标识：{platform.platform()}")
print(f"CPU硬件架构：{platform.machine()}")
print(f"python版本：{platform.python_version()}")
print(f"详细的版本信息：{platform.version()}")
print("-" * 10)
# 2、核心模块-1，操作系统信息的获取（跨平台开发核心之中）
# 操作系统类型的判断
os_type = platform.system()
if os_type == "Windows":
    print("Windows操作系统")
elif os_type == "Linux":
    print("Linux系统")
elif os_type == "Darwin":
    print("macos操作系统")
else:
    print("其它操作系统")
print("-" * 10)
# 完整平台表示
print(f"完整平台标识：{platform.platform()}")
print(f"精简平台标识：{platform.platform(aliased=True, terse=True)}")
# 系统版本详情
print(f"系统内核发行版本号:{platform.release()}")
print(f"更加精准:{platform.version()}")
# 系统信息的批量获取
uname_info = platform.uname()
print(uname_info)
# 3、Python解释器信息的获取
# 如何获取版本，如何进行版本判断
res1 = platform.python_version()
res2 = platform.python_version_tuple()
print(f"res1:{res1}")
print(f"res2:{res2}")
# 获取python解释器类型
py_impl = platform.python_implementation()
print(f"python解释器的实现方式:{py_impl}")
# 补充函数
print(f"python解释器信息:{platform.python_compiler()}")
print(f"python构建时间、构建分支信息:{platform.python_build()}")
# 4、核心模块3，硬件与架构信息获取
# 获取硬件架构
print(f"硬件构架为:{platform.machine()}")
# 获取系统位数
print(f"系统位数:{platform.architecture()}")
# 补充函数
print(f"CPU具体型号:{platform.processor()}")
# 5、核心模块4，系统专属高级信息的获取
# 【Linux】platform.freedesktop_os_release()
# 【MacOS】platform.mac_ver()
# 【Windows】专属信息
print(f"Windows专属信息:{platform.win32_ver()}")


# 6、常见坑点和避坑指南
# 需要进行系统判断
# 版本比较
# 操作系统位数进行比较
# 推荐使用platform标准库，而不是os标准库
# 7、实战案例，跨平台信息采集工具
def set_logger():
    logger = logging.getLogger("env_checker")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # 控制台输出handler：以简洁格式输出
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    # 文件输出对象
    file_handler = logging.FileHandler("env_info.log", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger


def collect_env_info() -> Dict:
    """全维度采集环境工具，返回结构化字典"""
    env_info = {}
    # 操作系统的核心信息
    env_info["system"] = platform.system()
    env_info["system_release"] = platform.release()
    env_info["system_version"] = platform.version()
    # 硬件和架构信息
    env_info["machine_arch"] = platform.machine()
    env_info["processor"] = platform.processor()
    env_info["python_bits"] = platform.architecture()
    # 获取python解释器信息
    env_info["python_version"] = platform.python_version()
    env_info["python_version_tuple"] = platform.python_version_tuple()
    env_info["python_com"] = platform.python_compiler()
    return env_info


class Tool:
    def __init__(self, user):
        self.user = user

    def my_set_logger(self):
        print(f"=== {self.user} ===")
        return set_logger()

    def my_collect_env_info(self):
        print(f"=== {self.user} ===")
        return collect_env_info()


tool = Tool("admin")
print(tool.my_collect_env_info())
