"""
asyncio 标准库学习
"""

import asyncio


# 基础-1：协程的定义与运行
# 定义协程函数
async def hello(name):
    print(f"Hello, {name}.")
    await asyncio.sleep(1)
    print(f"Bye, {name}")


# 协程函数的调用方式
# asyncio.run(hello("admin"))


# 基础-2：await关键字
async def compute(x, y):
    print(f"Now is compute {x} and {y}!")
    await asyncio.sleep(2)
    return x + y


async def main():
    x, y = 3, 4
    res = await compute(x, y)
    print(f"[res]:{res}")


# asyncio.run(main())


# 基础-3：Task对象
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main3():
    # 创建两个并发任务
    task1 = asyncio.create_task(say_after(1, "hello jom"))
    task2 = asyncio.create_task(say_after(2, "hello kom"))
    print("Tasks is started!")
    await task1
    await task2


# 基础-4：批量管理协程
# gather wait 关键字
async def fetch_data(delay, data_id):
    await asyncio.sleep(delay)
    return f"Data {data_id}"


async def main4():
    # 通过gather并发执行收集结果
    results = await asyncio.gather(fetch_data(1, 1), fetch_data(2, 2), fetch_data(3, 3))
    print(f"[results]:{results}")
    # 通过await关键字收集结果
    tasks = [
        asyncio.create_task(fetch_data(1, 1)),
        asyncio.create_task(fetch_data(2, 2)),
        asyncio.create_task(fetch_data(3, 3)),
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        print(task.result())
    print(f"[done]:{done}")
    print(f"[pending]:{pending}")


# 进阶-1：同步原语
# 便于协程之间的协作
# 互斥锁
shared_counter = 0
lock = asyncio.Lock()


async def increment():
    global shared_counter
    # 获取锁
    async with lock:
        temp = shared_counter
        await asyncio.sleep(0.1)
        shared_counter = temp + 1


async def main5():
    # 启动10个协程，并且让10个协程之间并发修改变量
    await asyncio.gather(*[increment() for _ in range(10)])
    print(f"Final counter:{shared_counter}")


# Semaphore 信号量
# 控制并发访问数量，常常用于限制并发连接数
async def limited_access(sem, resource_id):
    async with sem:
        print(f"Accessing resource: {resource_id}")
        await asyncio.sleep(5)
        print(f"Releasing resource: {resource_id}")


async def main6():
    sem = asyncio.Semaphore(3)
    print(f"[sem]:{sem},[sem]:{type(sem)}")
    await asyncio.gather(*[limited_access(sem, i) for i in range(10)])


# 进阶-2：异步上下文管理器
# 需要实现 async enter 和 async exit 这两个方法
class AsyDataBaseConnection:
    async def connect(self):
        print("Connecting to database ......")
        await asyncio.sleep(1)
        print("Connected")

    async def disconnect(self):
        print("Disconnect to database ......")
        await asyncio.sleep(1)
        print("Disconnect")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
        # return >>>
        #   False：不抑制异常
        #   True：抑制异常
        return False


async def main7():
    async with AsyDataBaseConnection():
        print("=== 测试自定义上下文管理器 ===")


# 进阶-3：异步迭代器和异步生成器
# 异步迭代器：实现 async iter 和 async next 方法
# 异步生成器：async def 和 yield 关键字实现
async def async_counter(n):
    for i in range(n):
        await asyncio.sleep(0.5)
        yield i


async def main8():
    async for num in async_counter(5):
        print(f"Counter:{num}")


# 进阶-4：任务取消和异常处理
# Task.cancel()取消
# 会抛出一个异常： CancelledError
async def long_running_task():
    try:
        for i in range(5):
            print(f"Working ... {i}")
            await asyncio.sleep(1)
    except Exception as e:
        print(f"[Error]:{e}")
        raise e
    finally:
        print("Clean up resource ......")


async def main9():
    task = asyncio.create_task(long_running_task())
    await asyncio.sleep(2)
    print("Cancelling task ......")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Main task is cancel!")
    except Exception as e:
        print(f"[Error]:{e}")


if __name__ == "__main__":
    asyncio.run(main9())
