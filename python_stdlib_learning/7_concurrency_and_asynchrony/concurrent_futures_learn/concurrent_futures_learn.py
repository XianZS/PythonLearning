"""
concurrent.futures 标准库学习
"""

import concurrent.futures
from contextlib import contextmanager
import time


# 基础-1：线程池基础
# 适合IO密集型任务
# 如何向线程池之中提交任务
# 单提交/批量提交
def task(name, delay):
    print(f"任务{name}开始，花费时间为:{delay}")
    time.sleep(delay)
    return f"任务{name}"


# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         # 通过 executor.submit() 提交单个任务
#         f1 = executor.submit(task, "A", 2)
#         f2 = executor.submit(task, "B", 3)
#         f3 = executor.submit(task, "C", 4)
#         print(f"[f1]:{f1.result()};[f2]:{f2.result()};[f3]:{f3.result()}")

# 批量提交任务：通过任务的提交顺序，获取任务执行的结果
# if __name__ == "__main__":
#     names = ["a", "b", "c"]
#     times = [1, 2, 3]
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         results = executor.map(task, names, times)
#         for child in results:
#             print(child)

# 批量提交任务：通过任务的完成顺序，获取任务执行的结果
# if __name__ == "__main__":
#     names = ["a", "b", "c"]
#     times = [3, 2, 1]
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         futures = {
#             executor.submit(task, names[i], times[i]): f"任务{i}" for i in range(3)
#         }
#         print(f"[futures-type]:{type(futures)},{futures}")
#         for future in concurrent.futures.as_completed(futures):
#             task_name = futures[future]
#             try:
#                 res = future.result()
#                 print(f"{task_name} 完成,结果是:{res}")
#             except Exception as e:
#                 print(f"{e}")
#


# 基础-2：进程池
# CPU密集型任务
def cpu_task(x: float):
    time.sleep(1)
    return x * x


# if __name__ == "__main__":
#     # 单进程版本
#     start_time = time.time()
#     results = [cpu_task(x) for x in range(4)]
#     print(f"[单进程]：{results}，花费时间为:{time.time() - start_time}")
#     # [单进程]：[0, 1, 4, 9]，花费时间为:4.001375198364258
#     # 多进程版本
#     start_time = time.time()
#     with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
#         results = executor.map(cpu_task, range(4))
#         spend_time = time.time() - start_time
#         print(f"[多进程]：{list(results)}，花费时间为:{spend_time}")
#         # [多进程]：[0, 1, 4, 9]，花费时间为:0.056931257247924805


# 基础-3：Future对象的基础方法
# 异步任务的核心
# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
#         f = executor.submit(task, "A", 20000)
#         print(f"[f]:{f},[type]:{type(f)}")
#         # f.cancel()
#         # 标识当前任务是否完成
#         print(f"任务是否完成:{f.done()}")
#         # 得到任务的执行结果
#         print(f"任务的执行结果:{f.result()}")
#         print(f"任务是否完成:{f.done()}")
#         # 取消任务
#         # f.cancel()

# 进阶-1：上下文管理
# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.submit(task, "A", 1)


# 进阶-2：回调函数
# 执行时机：在Future完成时，会自动执行回调函数（不需要阻塞等待结果）
def save_result(future):
    """回调函数：保存任务的结果"""
    try:
        result = future.result()
        print(f"回调函数收到结果:{result}")
    except Exception as e:
        print(f"回调函数捕捉到异常:{e}")


# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future = executor.submit(task, "A", 1)
#         # 给任务添加回调函数
#         future.add_done_callback(save_result)


# 进阶-3：异常处理的捕捉
# submit() 触发的异常
def error_task(num):
    number = int(num)
    raise ValueError("任务出错了")


# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         f = executor.submit(error_task, "a")
#         try:
#             f.result()
#         except ValueError as e:
#             print(f"捕捉到异常:{e}")


# map() 触发的异常
def maybe_error(x):
    if x == 3:
        raise ValueError(f"x={x} 出错了")
    return x * x


# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         try:
#             for cho in executor.map(maybe_error, range(5)):
#                 print(cho)
#         except ValueError as e:
#             print(f"批量提交任务时触发异常(由map触发):{e}")


# 进阶-4：灵活等待多个任务
# wait() 等待多个Future的完成
# return_when 设置更详细的参数设置
# 默认参数：ALL_COMPLETED
# [done]:{<Future at 0x2015be4ac10 state=finished returned str>, <Future at 0x2015bd9a8b0 state=finished returned str>, <Future
#  at 0x2015be4a850 state=finished returned str>, <Future at 0x2015be9c6e0 state=finished returned str>},[len]:4
# [not_done]:set(),[len]:0

# concurrent.futures.FIRST_COMPLETED:等待第一个任务完成或者出错
# ALL_COMPLETED:等待所有任务完成
# FIRST_EXCEPTION:等待第一个任务出错，没有出错则完成所有

# if __name__ == "__main__":
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         fs = [
#             executor.submit(task, f"任务{abs(4 - time)}", time)
#             for time in range(4, 0, -1)
#         ]
#         # 等待任务的完成
#         done, not_done = concurrent.futures.wait(
#             fs, return_when=concurrent.futures.FIRST_EXCEPTION
#         )
#         print(f"[done]:{done},[len]:{len(done)}")
#         print(f"[not_done]:{not_done},[len]:{len(not_done)}")

# 进阶-5：高级参数的设置
# 进程的最大容量:max_workers

# 进程的启动方法:mp_context
# if __name__ == "__main__":
#     import multiprocessing
#
#     ctx = multiprocessing.get_context("spawn")
#     with concurrent.futures.ProcessPoolExecutor(mp_context=ctx) as executor:
#         res = list(executor.map(cpu_task, range(4)))
#         print(res)


# 进程的初始化:initializer+initargs
def init_process(config):
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = config
    print(f"进程初始化完成，全局配置更新为:{GLOBAL_CONFIG}")


def task_with_config(x):
    return x * GLOBAL_CONFIG["scale"]


if __name__ == "__main__":
    config = {"scale": 9}
    with concurrent.futures.ProcessPoolExecutor(
        initializer=init_process, initargs=(config,)
    ) as executor:
        res = list(executor.map(task_with_config, range(4)))
        print(res)
