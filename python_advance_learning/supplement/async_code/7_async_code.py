"""
async 异步实现
"""

import asyncio
from time import time


# 【定义-语法规范】：async def 函数名()
# 【调用-语法规范】：await 函数名()
async def web_request_response(*args, **kwargs):
    print("=== 服务端处理请求 ===")
    print(f"[args]:{args}")
    print(f"[kwargs]:{kwargs}")
    await asyncio.sleep(3)


async def web_request(*args, **kwargs):
    print("=== 客户端接收请求 ===")
    await web_request_response()


async def client():
    begin_time = time()
    # task=asyncio.create_task(web_request)
    tasks = []
    for x in range(3):
        tasks.append(asyncio.create_task(web_request()))
    print(tasks)
    for task in tasks:
        await task
    spend_time = time() - begin_time
    print(f"[异步]:{spend_time}")
    # [异步]:3.007171869277954


if __name__ == "__main__":
    asyncio.run(client())
