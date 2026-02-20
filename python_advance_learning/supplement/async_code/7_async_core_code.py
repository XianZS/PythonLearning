"""
async核心概念
（1）异步编程的基本单元：协程
（2）事件循环：asyncio的心脏
（3）可等待对象：await关键字的唯一合法操作数
（4）Task对象 VS Future对象
    Future:底层抽象，手动创建时需要调用set_result()/set_exception()标记完成，通常不需要手动进行创建
    Task:Futrure的子类，专为协程设计，create_task()会自动将协程封装为Task，并且交由事件循环调度，是实际开发之中最常用的对象。
（5）管理事件循环的创建/获取/销毁的规则，默认由asyncio提供。
"""

import asyncio


# 定义协程函数（async def 是标志）
async def simple_asyncio_code(name: str) -> None:
    print(f"协程 {name} 开始执行")
    await asyncio.sleep(1)
    print(f"协程 {name} 结束执行")


# 执行协程的三种方式
def run_asyncio_code_1():
    """
    方式1：asyncio.run()
    自动管理事件循环，比较适用于单协程执行，协程脚本的入口
    """
    asyncio.run(simple_asyncio_code("方式1"))


def run_asyncio_code_2():
    """
    方式2：
        loop=asyncio.get_event_loop()
        loop.run_until_complete(simple_asyncio_code("方式"))
    手动管理事件
    """
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(simple_asyncio_code("方式2"))
    except Exception as e:
        print(e)
    finally:
        loop.close()


if __name__ == "__main__":
    run_asyncio_code_1()
    run_asyncio_code_2()
