import asyncio

# （第一部分）异步锁
# 模拟银行存取钱的过程
# 实例化异步锁对象
lock = asyncio.Lock()

# 模拟一个全局变量，作为你当前在银行所拥有的金钱数量
number = 0  # 临界资源


async def worker():
    global number
    for _ in range(1000):
        # 在什么时候调用异步锁？
        # 【临界区】同一时刻只允许一个协程访问临界区
        # 应该在此时添加异步锁
        async with lock:
            temp = number
            await asyncio.sleep(0.0001)
            number = temp + 1


# number=100
# a/b temp_a=100 temp_b=100
# a/b number=101 理想值102


async def run_1():
    tasks = [asyncio.create_task(worker()) for _ in range(10)]
    res = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"[Res]:{res}")
    print(f"[Number]:{number}")


# 如何实现在同一时刻允许c个HTTP请求访问服务器
sem = asyncio.Semaphore(3)  # 此时c=3


# 信号量
async def sem_worker():
    async with sem:
        print(sem._value)
        print(f"当前处于运行状态的协程数:{3 - sem._value}")
        await asyncio.sleep(1)


async def run_2():
    tasks = [asyncio.create_task(sem_worker()) for _ in range(10)]
    res = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"[Res]:{res}")


if __name__ == "__main__":
    # asyncio.run(run_1())
    asyncio.run(run_2())
