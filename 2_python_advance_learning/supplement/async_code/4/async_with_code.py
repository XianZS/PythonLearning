"""
异步上下文管理器
（自定义）同步上下文管理器之中，进入__enter__/退出__exit__
（自定义）异步上下文管理器之中，进入__aenter__/退出__aexit__
"""

import asyncio


class AsyncWith:
    async def __aenter__(self):
        """
        作用：异步上下文管理器的入口
        接收参数：异步上下文管理器对象本身，就是self
        返回值：异步上下文管理器对象本身，也就是self
        """
        print("=== 异步上下文管理器入口 ===")
        # 模拟入口进入时间，模拟时间为3秒钟
        await asyncio.sleep(3)
        return self

    async def __aexit__(self, *args):
        """
        作用：异步上下文管理器的出口
        接收参数：异步上下文管理器对象本身/异类类型/异常对象/异常的追踪栈
        返回值：bool
        """
        print(f"[Args]:{args}")
        try:
            # 模拟关闭时间为3秒钟
            await asyncio.sleep(3)
        except Exception as e:
            print(f"[Error]:{e}")
            return False


async def run_enter():
    async with AsyncWith() as aw:
        print("成功进入异步上下文管理器")
        # 中间可以进行一些异步上下文管理器的操作
        print("即将退出上下文管理器")
        # raise IndexError


if __name__ == "__main__":
    asyncio.run(run_enter())
