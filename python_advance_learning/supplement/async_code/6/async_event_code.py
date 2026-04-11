import asyncio

event = asyncio.Event()


async def worker_need_wait():
    try:
        print("等待事件触发")
        await event.wait()
        print("事件已经被触发")
    except Exception as e:
        raise e
    finally:
        event.clear()


async def worker_setter():
    try:
        await asyncio.sleep(3)
        print("即将设置事件")
        event.set()
    except Exception as e:
        raise e
    finally:
        print("设置结束")


async def demo():
    await asyncio.gather(worker_need_wait(), worker_setter())


if __name__ == "__main__":
    asyncio.run(demo())
