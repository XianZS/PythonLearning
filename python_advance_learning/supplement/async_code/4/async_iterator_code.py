import asyncio


class AsyncRange:
    """自定义异步迭代器：生成1~n的数，每次生成间隔0.5秒"""

    def __init__(self, n: int):
        self.n = n
        self.i = 0

    # 异步迭代器必须实现__aiter__（返回自身）
    def __aiter__(self):
        return self

    # 异步迭代器必须实现__anext__（返回可等待对象）
    async def __anext__(self):
        if self.i >= self.n:
            # 终止异步迭代的标志
            raise StopAsyncIteration
        self.i += 1
        await asyncio.sleep(0.5)  # 模拟异步生成数据
        return self.i


async def async_iter_demo():
    """使用异步迭代器"""
    async for num in AsyncRange(100):
        print(f"异步迭代获取：{num}")


asyncio.run(async_iter_demo())
