import asyncio


async def async_func():
    print("async_func function")
    await asyncio.sleep(3)


async def hello(name):
    print(f"Hello, {name}!")
    await async_func()
    print(f"Bye, {name}!")
    print()


def run_asyncio_func():
    """
    步骤：
        事件循环启动——》将协程加入循环之中——》协程执行到await
    """
    asyncio.run(hello("jom"))
    asyncio.run(hello("kom"))
    asyncio.run(hello("lom"))


if __name__ == "__main__":
    run_asyncio_func()
