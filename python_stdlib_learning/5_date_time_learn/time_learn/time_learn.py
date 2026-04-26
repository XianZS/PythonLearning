"""
time 标准库学习
"""

import time
from typing import Callable, Optional

# 基础-1：获取当前的时间戳
t = time.time()
print(f"[时间戳]:{t}")
# 基础-2：程序暂停
# 语法规范：time.sleep(secs)：暂停的秒数
print("开始执行...")
# time.sleep(3)
print("3秒后执行完毕")
# 基础-3：时间戳转为可读字符串
# 语法规范：time.ctime([secs])
# 将当前时间转为可读字符串
current_time = time.ctime()
print(f"[当前时间]:{current_time},[type]:{type(current_time)}")
# 将指定时间戳转为可读字符串
specified_str = time.ctime(123456789)
print(f"[指定时间]:{specified_str},[type]:{type(specified_str)}")
# 基础-4：结构化时间对象
# 语法规范：time.localtime() time.gmtime()
local_struct_now_time = time.localtime()
print(
    f"[当前时间结构化]:\n{local_struct_now_time}\n[type]:{type(local_struct_now_time)}"
)
# 通过结构化事件对象.结构化时间属性的方式进行访问
print(f"年:{local_struct_now_time.tm_year}")
print(f"时:{local_struct_now_time.tm_hour}")
# 基础-5：将结构化时间转为字符串
# 语法格式：time.strftime(format[,t])
# 格式化当前时间
current_time = time.localtime()
formatted1 = time.strftime("%Y-%m-%d %H:%M:%S", local_struct_now_time)
print(f"[当前时间结构化]:{formatted1}")
# 基础-6：将字符串转换为结构化时间
# 语法格式：time.strptime(string[,format])
date_str = "2026年5月2日 3时2分1秒"
struct_time = time.strptime(date_str, "%Y年%m月%d日 %H时%M分%S秒")
print(f"[解析]:\n{struct_time}")
# 进阶-1：进行高精度性能计算
# time.perf_counter()：返回系统级高精度时间，比较适合测试代码块的实际经过时间。
start_time = time.perf_counter()
time.sleep(1)
end_time = time.perf_counter()
print(f"[perf_counter]:{end_time - start_time}")
# [perf_counter]:1.0003141999998206
# time.process_time()：返回进程的CPU执行时间，比较适合测试代码块的CPU消耗。
start_time = time.process_time()
time.sleep(1)
end_time = time.process_time()
print(f"[process_time]:{end_time - start_time}")
# [process_time]:0.0
# 进阶-2：结构化时间转为时间戳
# time.localtime()的逆向操作
# time.mktime(t)
date_str = "2026年5月2日 3时2分1秒"
struct_time = time.strptime(date_str, "%Y年%m月%d日 %H时%M分%S秒")
# 将struct_time转为时间戳
timestamp = time.mktime(struct_time)
print(f"[时间戳]:{timestamp}")
# 进阶-3：struct_time的完整属性
# struct_time本身是一个命名元组，不仅可以通过属性来进行访问，也可以通过索引进行访问。
struct_time = time.localtime()
# 通过属性进行访问
print(f"年:{struct_time.tm_year}")
# 通过索引进行访问
print(f"年:{struct_time[0]}")
print(f"[struct_time]:{struct_time}")
# 进阶-4：时区相关
# time.tzname:返回本地时区的命名元组
# time.tzset():根据环境变量TZ重置本地时区（仅Unix系统可以使用，Windows不可以使用）
# 查看本地时区的名称
print(f"[本地时区]:{time.tzname}")


# import os
# os.environ["TZ"]="UTC"
# time.tzset()
# print(f"[切换之后的时区]:{time.tzname}")
# 实战案例：代码性能测试与定时任务工具
# - 测试任意代码块的实际执行时间和CPU消耗时间
# - 设置定时任务，并且记录每次执行时的时间戳和可读时间
# - 统计任务执行的总次数和总耗时
# - 支持自定义任务间隔和执行次数
class PerformanceTester:
    """代码性能测试工具"""

    @staticmethod
    def test_code_block(code_func: Callable, run_times: int = 1) -> dict:
        """
        测试代码块的性能
        """
        total_perf = 0.0
        total_proc = 0.0
        for i in range(run_times):
            # 测试实际运行时间
            start_perf_time = time.perf_counter()
            # 测试CPU运行时间
            start_proc_time = time.process_time()
            # 执行代码
            code_func()
            # 计算耗时
            spend_perf_time = time.perf_counter() - start_perf_time
            spend_proc_time = time.process_time() - start_proc_time
            total_perf += spend_perf_time
            total_proc += spend_proc_time
        return {
            "run_times": run_times,
            "total_perf": total_perf,
            "total_proc": total_proc,
        }


class ScheduledTask:
    """定时任务执行器"""

    def __init__(
        self, task_func: Callable, interval: float, max_runs: Optional[int] = None
    ):
        """
        定时任务执行器初始化
        """
        # 无参数的任务函数对象本身
        self.task_func = task_func
        # 任务间隔（单位：秒）
        self.interval = interval
        # 最大运行次数（类型：int）
        self.max_runs = max_runs
        # （已经发生）运行此时
        self.run_count = 0
        # 开始时间（初始化为None）
        self.start_time = None

    def _log_execution(self):
        """记录单次执行的时间"""
        timestamp = time.time()
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        print(
            f"[执行记录]: 第{self.run_count}次 | 时间戳:{timestamp:.6f} | 本地时间:{local_time}"
        )

    def run(self):
        """启动定时任务"""
        self.start_time = time.perf_counter()
        try:
            while True:
                if self.max_runs is not None and self.run_count >= self.max_runs:
                    break
                self.run_count += 1
                # 开始执行任务
                self.task_func()
                # 记录执行时间
                self._log_execution()
        except KeyboardInterrupt:
            print("手动中断任务")
        finally:
            total_duration = time.perf_counter() - self.start_time
            print(f"任务执行结束，总耗时为:{total_duration}")


if __name__ == "__main__":
    # 性能测试
    def test_task():
        res = 0
        for i in range(1000000):
            res += i
        return res

    tester = PerformanceTester()
    per_res = tester.test_code_block(test_task, run_times=3)
    print(f"[代码性能测试结果]:\n{per_res}")

    # 定时任务执行测试
    def scheduled_job():
        print("执行定时任务：Hello time！")
        time.sleep(1)

    task = ScheduledTask(scheduled_job, interval=2, max_runs=5)
    task.run()
