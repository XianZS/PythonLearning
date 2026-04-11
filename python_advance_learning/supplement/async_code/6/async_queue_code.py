import asyncio


async def producer(queue: asyncio.Queue):
    """生产者：向队列中放入数据"""
    for i in range(5):
        await asyncio.sleep(1)  # 模拟生产数据耗时
        data = f"数据{i}"
        await queue.put(data)  # 放入队列（队列满则阻塞）
        print(f"生产者：放入 {data} | 队列当前大小：{queue.qsize()}")
    # 放入终止信号
    await queue.put(None)


async def consumer(queue: asyncio.Queue):
    """消费者：从队列中取出数据并处理"""
    while True:
        data = await queue.get()  # 取出队列（队列空则阻塞）
        if data is None:
            # 收到终止信号，退出循环
            queue.task_done()  # 标记任务完成
            break
        print(f"消费者：处理 {data} | 队列剩余大小：{queue.qsize()}")
        await asyncio.sleep(2)  # 模拟处理数据耗时
        queue.task_done()  # 标记任务完成（用于queue.join()）


async def queue_demo():
    """测试异步队列：生产者-消费者模型"""
    # 创建队列（最大容量=3，超过则生产者阻塞）
    queue = asyncio.Queue(maxsize=3)
    # 启动生产者和消费者
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    # 等待队列中所有任务完成（所有put的元素都被task_done）
    await queue.join()
    # 等待生产者完成
    await producer_task
    # 取消消费者
    consumer_task.cancel()


asyncio.run(queue_demo())
