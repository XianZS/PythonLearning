# asyncio异步编程的组成部分：
# （1）协程对象；（2）可等待对象；（3）事件循环；（4）循环策略；（5）Task/Future
import asyncio


# 创建一个协程对象
async def worker(num: int) -> int:
    print("协程对象开始执行")
    await asyncio.sleep(num)
    print("协程对象开始执行")
    return num


# （第一种方式）往往被用作协程脚本的入口，python-version>=3.6
def run_function_1():
    # asyncio.run(需要传入协程对象)
    import time

    begin_time = time.time()
    # 相当于建立了三个事件循环
    # 第一个事件循环
    res = asyncio.run(worker(3))
    # 第二个事件循环
    res = asyncio.run(worker(3))
    # 第三个事件循环
    res = asyncio.run(worker(3))
    spend_time = time.time() - begin_time
    print(f"[第一种方式]:{res}，花费时间为:{spend_time}")


# （第三种）create_task()方式
async def run_function_3():
    """
    将三个协程Task对象，封装到一个事件循环之中
    """
    import time

    begin_time = time.time()
    task1 = asyncio.create_task(worker(3))
    task2 = asyncio.create_task(worker(3))
    task3 = asyncio.create_task(worker(3))
    # res = asyncio.run(task1, task2, task3)
    await task1
    await task2
    await task3
    res = await asyncio.gather(task1, task2, task3)
    spend_time = time.time() - begin_time
    print(f"[第三种方式]:花费时间为:{spend_time},res:{res}")
    # [第三种方式]:花费时间为:3.0160465240478516


if __name__ == "__main__":
    # run_function_1()
    asyncio.run(run_function_3())
