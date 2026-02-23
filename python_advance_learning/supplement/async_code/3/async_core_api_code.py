"""
asyncio 的其它核心API接口
"""

import asyncio


async def worker(num: int) -> int:
    await asyncio.sleep(num)
    return num


# （1）批量一次性执行多个任务
async def run_1():
    """
    在上节课之中，将所有的协程封装成Task对象，然后将其加入当前的“异步循环”之中。
    在使用asyncio.gather(协程1，协程2)
    会将传入的协程对象，在底层自动调用create_task()，将其封装成Task对象，然后将其加入循环之中。
    """
    # * args:允许接收多个顺序参数
    import time

    begin_time = time.time()
    cores = [worker(1), worker(2), worker(3)]
    res = await asyncio.gather(*cores)
    spend_time = time.time() - begin_time
    print(res, spend_time)


# （2）灵活自定义并发任务
async def run_2():
    """
    pass
    """
    tasks = []
    for x in range(1, 4):
        now_task = asyncio.create_task(worker(x))
        # now_task.cancel()# 手动取消任务的执行
        tasks.append(now_task)
    print(tasks)
    res = await asyncio.gather(*tasks)
    print(res)


# （3）灵活调试并发任务
async def run_3():
    tasks = []
    for x in range(1, 4):
        tasks.append(asyncio.create_task(worker(x)))
    finish_work, padding_work = await asyncio.wait(
        tasks,
        # FIRST_EXCEPTION：当第一个任务异常时返回
        # FIRST_COMPLETED：当第一个任务成功执行时返回
        return_when=asyncio.FIRST_EXCEPTION,
        timeout=3,
    )
    print(len(finish_work), len(padding_work))
    print(finish_work)
    print(padding_work)


if __name__ == "__main__":
    asyncio.run(run_1())
    asyncio.run(run_2())
    asyncio.run(run_3())
