# Python进阶：`asyncio `与 IO 密集型场景深度对比

---

## 模块1：同步VS异步 深度对比（底层逻辑+性能本质）

`asyncio`的核心价值体现在**IO密集型任务**的处理上，先从底层维度拆解同步与异步的本质差异，为理解`asyncio`奠定基础。

### 1.1 核心维度对比表（深度版）

|对比维度|同步编程（Sync）|异步编程（Async，基于asyncio）|
|---|---|---|
|**执行模型**|串行阻塞：代码按顺序执行，遇到IO（网络/文件/数据库）时，整个线程/进程暂停等待，直到IO完成|非阻塞并发：代码执行到IO时，协程**挂起**（放弃CPU），事件循环调度其他就绪协程执行，IO完成后恢复原协程|
|**底层调度**|操作系统内核调度（线程/进程切换），切换成本高（内核态→用户态）|用户态调度（事件循环调度协程），切换成本极低（仅函数调用级）|
|**资源占用**|为避免阻塞，需创建多线程/多进程（如1000个请求需1000个线程），内存占用高（每个线程栈≈1MB）|单线程/少量线程即可处理大量并发（1000个请求仅需1个线程），内存占用极低|
|**IO处理逻辑**|主动等待（Polling）：CPU空转等待IO结果|被动通知（Event-driven）：IO完成后由操作系统触发回调，CPU无空转|
|**性能表现**|IO密集型任务：总耗时≈各任务耗时之和（如5个2秒任务→10秒）；CPU密集型：无劣势|IO密集型任务：总耗时≈最长单个任务耗时（如5个2秒任务→2秒）；CPU密集型：无优势（协程无法利用多核）|
|**编程思维**|线性思维：代码执行顺序=逻辑顺序，易理解|异步思维：需关注协程挂起/恢复点，需结合`await`/事件循环，入门门槛高|
|**典型实现**|`requests`（HTTP）、`pymysql`（数据库）、`time.sleep()`|`aiohttp`（HTTP）、`aiomysql`（数据库）、`asyncio.sleep()`|
### 1.2 直观性能对比：同步VS异步处理IO密集型任务

以下代码模拟「批量网络请求（IO密集型）」场景，清晰体现异步的性能优越性：

#### 1.2.1 同步版本（耗时高）

```Python
import time
import requests  # 同步HTTP库（模拟IO耗时）

def sync_fetch(url: str, delay: int) -> str:
    """
    同步获取URL数据（模拟IO密集型任务）
    :param url: 模拟请求的URL
    :param delay: 模拟IO延迟（秒）
    :return: 模拟响应结果
    """
    print(f"[同步] 开始请求 {url}（延迟{delay}秒）| 时间戳：{time.time():.2f}")
    # 同步阻塞等待（模拟网络IO耗时，CPU空转）
    time.sleep(delay)
    # 实际场景中是requests.get(url)，此处用sleep模拟
    print(f"[同步] 完成请求 {url} | 时间戳：{time.time():.2f}")
    return f"{url} 响应数据"

def sync_main():
    """同步执行批量IO任务"""
    # 模拟5个IO任务，每个延迟2秒
    urls = [f"https://example.com/{i}" for i in range(5)]
    delays = [2] * 5  # 每个任务耗时2秒

    # 记录开始时间
    start_time = time.time()
    # 串行执行：完成一个再执行下一个
    for url, delay in zip(urls, delays):
        sync_fetch(url, delay)
    
    # 计算总耗时
    total_time = time.time() - start_time
    print(f"\n[同步] 所有任务完成 | 总耗时：{total_time:.2f}秒（理论值：5×2=10秒）")

if __name__ == "__main__":
    sync_main()
```

**同步版本输出（核心耗时）**：

```Plain Text

[同步] 开始请求 https://example.com/0（延迟2秒）| 时间戳：1711000000.00
[同步] 完成请求 https://example.com/0 | 时间戳：1711000002.00
[同步] 开始请求 https://example.com/1（延迟2秒）| 时间戳：1711000002.00
[同步] 完成请求 https://example.com/1 | 时间戳：1711000004.00
...（中间省略3个任务）
[同步] 所有任务完成 | 总耗时：10.00秒（理论值：5×2=10秒）
```

#### 1.2.2 异步版本（耗时极低）

```Python

import time
import asyncio

async def async_fetch(url: str, delay: int) -> str:
    """
    异步获取URL数据（模拟IO密集型任务）
    :param url: 模拟请求的URL
    :param delay: 模拟IO延迟（秒）
    :return: 模拟响应结果
    """
    print(f"[异步] 开始请求 {url}（延迟{delay}秒）| 时间戳：{time.time():.2f}")
    # 异步挂起：放弃CPU，事件循环调度其他协程（CPU无空转）
    await asyncio.sleep(delay)  # 替代同步的time.sleep，非阻塞
    print(f"[异步] 完成请求 {url} | 时间戳：{time.time():.2f}")
    return f"{url} 响应数据"

async def async_main():
    """异步执行批量IO任务"""
    # 模拟5个IO任务，每个延迟2秒
    urls = [f"https://example.com/{i}" for i in range(5)]
    delays = [2] * 5  # 每个任务耗时2秒

    # 记录开始时间
    start_time = time.time()
    # 步骤1：创建Task对象（将协程封装为可并发调度的单元）
    tasks = [
        asyncio.create_task(async_fetch(url, delay), name=f"task-{i}")
        for i, (url, delay) in enumerate(zip(urls, delays))
    ]
    # 步骤2：等待所有Task完成（并发执行，而非串行）
    # gather会收集所有任务的返回结果，return_exceptions=True避免单个任务异常导致整体失败
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 计算总耗时
    total_time = time.time() - start_time
    print(f"\n[异步] 所有任务完成 | 总耗时：{total_time:.2f}秒（理论值：≈2秒）")
    print(f"[异步] 任务结果：{results}")

if __name__ == "__main__":
    # asyncio.run：Python3.7+推荐的高层API，自动管理事件循环的创建/运行/关闭
    asyncio.run(async_main())
```

**异步版本输出（核心耗时）**：

```Plain Text

[异步] 开始请求 https://example.com/0（延迟2秒）| 时间戳：1711000000.00
[异步] 开始请求 https://example.com/1（延迟2秒）| 时间戳：1711000000.00
[异步] 开始请求 https://example.com/2（延迟2秒）| 时间戳：1711000000.00
[异步] 开始请求 https://example.com/3（延迟2秒）| 时间戳：1711000000.00
[异步] 开始请求 https://example.com/4（延迟2秒）| 时间戳：1711000000.00
[异步] 完成请求 https://example.com/0 | 时间戳：1711000002.00
[异步] 完成请求 https://example.com/1 | 时间戳：1711000002.00
[异步] 完成请求 https://example.com/2 | 时间戳：1711000002.00
[异步] 完成请求 https://example.com/3 | 时间戳：1711000002.00
[异步] 完成请求 https://example.com/4 | 时间戳：1711000002.00

[异步] 所有任务完成 | 总耗时：2.00秒（理论值：≈2秒）
[异步] 任务结果：['https://example.com/0 响应数据', ..., 'https://example.com/4 响应数据']
```

### 1.3 核心差异总结（异步优越性）

- **耗时差异**：同步版本总耗时=5×2=10秒（串行等待），异步版本总耗时≈2秒（所有任务并发执行，仅等待最长的IO耗时）；

- **CPU利用率**：同步版本CPU空转90%以上（等待IO），异步版本CPU在IO等待期可调度其他任务，利用率接近100%；

- **资源占用**：同步版本若处理1000个请求需创建1000个线程（内存占用≈1GB），异步版本仅需1个线程（内存占用≈MB级）。

---

## 模块2：`asyncio`核心概念（深度理解）

要掌握`asyncio`，需先吃透以下核心概念，这是理解异步编程的基础：

> 构建持久的多线程代码可能充满挑战且容易出错。异步 `I/O` 可以避免多线程设计中可能遇到的一些潜在速度瓶颈。然而，这并不意味着在 `Python `中进行异步编程是一件简单的事情。
>
> 请注意，异步编程一旦深入到底层，就会变得非常复杂。Python 的异步模型围绕着回调、协程、事件、传输、协议和`Future`等概念构建——即使仅仅是这些术语本身也可能令人望而生畏。

### 2.1 协程（Coroutine）：异步编程的基本单元

- **定义**：通过`async def`定义的函数，调用后返回「协程对象」（而非直接执行），需通过事件循环调度执行；

- **核心特性**：可暂停（`await`）、可恢复，暂停时不阻塞线程，是用户态的“轻量级线程”；

- **与线程的区别**：

    - 线程：内核调度，切换成本高（需保存寄存器/栈帧）；

    - 协程：用户态调度（事件循环），切换成本仅为函数调用，无内核态开销。

### 2.2 事件循环（Event Loop）：asyncio的“心脏”

- **定义**：`asyncio`的核心调度器，负责管理所有协程的生命周期；

- **核心职责**：
    1. 注册/调度协程/Task；
    
    2. 监听IO事件（网络/文件），触发回调；
    
    3. 切换挂起的协程，实现非阻塞执行；
    
    4. 处理定时器、信号等异步任务；
    
- **底层实现**：基于操作系统的IO多路复用（epoll/kqueue/select），实现“单线程监听多IO事件”。

### 2.3 可等待对象（Awaitable）：`await`的唯一合法操作数

`await`右侧必须是「可等待对象」，包含三类：

1. **协程对象**：`async def`函数调用的返回值（如`async_fetch(url, 2)`）；

2. **Task对象**：协程的可调度封装（`asyncio.create_task()`创建），是事件循环的直接调度单元；

3. **Future对象**：表示“未来完成的异步操作结果”，Task继承自Future，底层用于封装异步IO的结果。

### 2.4 Task vs Future

- **Future**：底层抽象，手动创建需调用`set_result()`/`set_exception()`标记完成，通常无需手动使用；

- **Task**：Future的子类，专为协程设计，`create_task()`自动将协程封装为Task，并交由事件循环调度，是实际开发中最常用的对象。

### 2.5 事件循环策略（Event Loop Policy）

- **定义**：管理事件循环的创建/获取/销毁的规则，默认由`asyncio`提供；

- **进阶优化**：Linux下可替换为`uvloop`（基于libuv实现，性能比默认循环快2-4倍）：

    ```Bash
    pip install uvloop
    ```
    
    ```Python
    import asyncio
    import uvloop
    # 设置uvloop为默认事件循环
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    ```

---

## 模块3：`asyncio`基础语法（核心入门）

### 3.1 协程的定义与执行（基础）

```Python

import asyncio

# 1. 定义协程函数（async def是标志）
async def simple_coroutine(name: str) -> None:
    """简单协程函数示例"""
    print(f"协程 {name} 开始执行")
    # await：暂停协程，等待可等待对象完成
    await asyncio.sleep(1)  # 模拟IO耗时
    print(f"协程 {name} 执行完成")

# 2. 执行协程的三种方式（进阶区分）
def run_coroutine_demo():
    # 方式1：asyncio.run（Python3.7+推荐，自动管理事件循环）
    # 适用于：单协程执行、脚本入口
    asyncio.run(simple_coroutine("方式1"))

    # 方式2：手动管理事件循环（兼容Python3.6-）
    # 适用于：旧版本兼容、自定义事件循环配置
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(simple_coroutine("方式2"))
    finally:
        loop.close()  # 必须手动关闭，避免资源泄漏

    # 方式3：create_task+asyncio.run（并发执行多协程）
    # 适用于：生产环境（体现asyncio核心价值）
    async def main():
        # 创建2个Task，并发执行
        task1 = asyncio.create_task(simple_coroutine("Task1"))
        task2 = asyncio.create_task(simple_coroutine("Task2"))
        # 等待所有Task完成
        await task1
        await task2

    asyncio.run(main())

if __name__ == "__main__":
    run_coroutine_demo()
```

### 3.2 `async/await` 核心规则（必记）

1. `async def`定义的函数只能返回「协程对象」，不能直接执行；

2. `await`仅能在`async def`函数内使用，右侧必须是可等待对象；

3. 未被`await`的协程对象不会执行（仅创建，无调度）；

4. 嵌套协程：`async def`函数内可调用其他`async def`函数，但必须加`await`。

### 3.3 错误示例与修正（避坑）

```Python

import asyncio

# 错误1：普通函数内使用await
def wrong_func():
    await asyncio.sleep(1)  # SyntaxError: 'await' outside async function

# 错误2：await非可等待对象
async def wrong_await():
    await 123  # TypeError: object int can't be used in 'await' expression

# 错误3：未await协程对象（仅创建，不执行）
async def no_await_coro():
    coro = simple_coroutine("未执行")  # 仅创建协程对象，无调度
    await asyncio.sleep(1)  # 协程从未执行

# 正确示例
async def correct_demo():
    # await协程对象
    await simple_coroutine("正确1")
    # await Task对象
    task = asyncio.create_task(simple_coroutine("正确2"))
    await task
```

---

## 模块4：`asyncio`核心`API`（进阶实战）

### 4.1 并发任务管理（核心）

> （1）批量一次性执行多个任务，包含自动和自定义任务；
>
> （2）灵活自定义并发任务；
>
> （3）灵活调试并发任务；

#### 4.1.1 `asyncio.gather()`：批量等待多个任务（推荐）

> 当你向 `asyncio.gather()` 传入**协程对象**时，`gather` 内部会自动调用 `asyncio.create_task()`（或等价的底层方法 `asyncio.ensure_future()`），把协程对象封装成 **Task 对象**（而非直接的 Future），然后将这些 Task 交给事件循环调度执行。

```Python

import asyncio

async def worker(num: int) -> int:
    """模拟耗时任务"""
    await asyncio.sleep(num)
    return num

async def gather_demo():
    """gather：批量管理并发任务"""
    # 1. 创建多个协程
    coros = [worker(1), worker(2), worker(3)]
    # 2. 并发执行，等待所有完成（返回结果列表，顺序与coros一致）
    # return_exceptions=True：单个任务异常时，异常会作为结果返回，不中断其他任务
    results = await asyncio.gather(*coros, return_exceptions=True)
    print(f"gather结果：{results}")  # [1, 2, 3]

    # 进阶：取消gather中的任务
    tasks = [asyncio.create_task(worker(5)) for _ in range(2)]
    gather_task = asyncio.gather(*tasks)
    # 取消所有任务
    gather_task.cancel()
    try:
        await gather_task
    except asyncio.CancelledError:
        print("gather任务已取消")

asyncio.run(gather_demo())
```

#### 4.1.2 `asyncio.wait()`：灵活控制等待策略

```Python

import asyncio

async def wait_demo():
    """wait：灵活控制任务等待方式"""
    tasks = {asyncio.create_task(worker(i)) for i in [1, 2, 3]}
    
    # return_when可选值：
    # - FIRST_COMPLETED：第一个任务完成时返回
    # - FIRST_EXCEPTION：第一个任务异常时返回
    # - ALL_COMPLETED：所有任务完成时返回（默认）
    done, pending = await asyncio.wait(
        tasks,
        timeout=2,  # 超时控制：2秒后强制返回
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"完成的任务数：{len(done)}，未完成的任务数：{len(pending)}")
    # 提取完成任务的结果
    for task in done:
        print(f"任务结果：{task.result()}")
    # 取消未完成的任务（避免资源泄漏）
    for task in pending:
        task.cancel()

asyncio.run(wait_demo())
```

### 4.2 超时控制（进阶：避免任务挂起）

```Python
import asyncio

async def timeout_demo():
    """超时控制：避免协程无限挂起"""
    async def long_task():
        await asyncio.sleep(10)  # 模拟长时间IO
        return "完成"

    # 方式1：asyncio.wait_for（超时抛出TimeoutError）
    try:
        result = await asyncio.wait_for(long_task(), timeout=2)
        print(f"任务结果：{result}")
    except asyncio.TimeoutError:
        print("任务超时（wait_for）")

    # 方式2：asyncio.shield（保护任务不被超时取消）
    try:
        # shield保护long_task不被wait_for的超时取消
        result = await asyncio.wait_for(asyncio.shield(long_task()), timeout=2)
    except asyncio.TimeoutError:
        print("外层超时，但任务仍在后台执行")
        # 等待被保护的任务完成
        await asyncio.sleep(10)

asyncio.run(timeout_demo())
```

### 4.3 异步迭代器与生成器（进阶语法）

#### 4.3.1 异步迭代器（`__aiter__`/`__anext__`）

```Python

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
    async for num in AsyncRange(3):
        print(f"异步迭代获取：{num}")

asyncio.run(async_iter_demo())
```

#### 4.3.2 异步生成器（`async def + yield`）

```Python

import asyncio

async def async_generator(n: int):
    """异步生成器：简化异步迭代器的实现"""
    for i in range(n):
        await asyncio.sleep(0.5)
        yield i + 1  # 异步生成数据

async def async_gen_demo():
    """使用异步生成器"""
    async for num in async_generator(3):
        print(f"异步生成器获取：{num}")

asyncio.run(async_gen_demo())
```

### 4.4 异步上下文管理器（`async with`）

```Python
import asyncio

class AsyncResource:
    """自定义异步上下文管理器：模拟异步资源的获取与释放"""
    async def __aenter__(self):
        """进入上下文：初始化异步资源（如数据库连接）"""
        print("异步资源初始化")
        await asyncio.sleep(1)  # 模拟资源初始化耗时
        return self  # 可返回资源对象

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文：释放异步资源"""
        print("异步资源释放")
        await asyncio.sleep(1)  # 模拟资源释放耗时
        # 返回True：捕获异常，不向外抛出；返回False：向外抛出异常
        return False

async def async_context_demo():
    """使用async with管理异步资源"""
    async with AsyncResource() as res:
        print("使用异步资源")  # 资源初始化完成后执行

asyncio.run(async_context_demo())
```

---

## 模块5：`asyncio`进阶特性（生产级应用）

### 5.1 异步锁（Lock）：解决并发资源竞争

当多个协程访问**共享资源**（如全局变量、文件、数据库连接）时，需用异步锁保证数据一致性：

```Python
import asyncio

# 共享资源
counter = 0
# 创建异步锁（非线程锁，仅用于协程间同步）
lock = asyncio.Lock()

async def increment():
    """递增计数器：需加锁保护共享资源"""
    global counter
    for _ in range(1000):
        # async with自动加锁/释放锁（推荐）
        async with lock:
            # 临界区：仅能有一个协程执行
            temp = counter
            await asyncio.sleep(0.0001)  # 模拟IO，触发协程切换
            counter = temp + 1

async def lock_demo():
    """测试异步锁：不加锁会导致计数器值小于10000"""
    # 并发执行10个协程，每个递增1000次
    tasks = [asyncio.create_task(increment()) for _ in range(10)]
    await asyncio.gather(*tasks)
    print(f"最终计数器值：{counter}")  # 加锁=10000，不加锁<10000

asyncio.run(lock_demo())
```

### 5.2 信号量（Semaphore）：控制并发数

用于限制同时执行的协程数量（如控制并发HTTP请求数，避免压垮目标服务）：

```Python

import asyncio

# 创建信号量：最大并发数=3
sem = asyncio.Semaphore(3)

async def limited_worker(num: int):
    """受信号量限制的协程：同时最多3个执行"""
    async with sem:  # 申请信号量，超过3个则等待
        print(f"Worker {num} 开始执行（当前并发数：{3 - sem._value}）")
        await asyncio.sleep(2)  # 模拟IO耗时
        print(f"Worker {num} 执行完成")

async def semaphore_demo():
    """测试信号量：10个任务，同时最多3个执行"""
    tasks = [asyncio.create_task(limited_worker(i)) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(semaphore_demo())
```

### 5.3 事件（Event）：协程间通信

用于协程间的“通知机制”（如一个协程完成后，通知其他协程继续执行）：

```Python
import asyncio

# 创建异步事件
event = asyncio.Event()

async def waiter():
    """等待事件触发"""
    print("等待事件触发...")
    await event.wait()  # 阻塞直到事件被设置
    print("事件已触发，继续执行")
    # 可选：清除事件（重置为未触发状态）
    event.clear()

async def setter():
    """设置事件（通知等待的协程）"""
    await asyncio.sleep(2)  # 模拟前置任务耗时
    print("设置事件")
    event.set()  # 触发事件，所有等待的协程恢复执行

async def event_demo():
    """测试异步事件"""
    await asyncio.gather(waiter(), setter())

asyncio.run(event_demo())
```

### 5.4 队列（Queue）：异步任务间数据传递

实现“生产者-消费者”模型，是协程间安全传递数据的核心工具：

```Python

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
```

### 5.5 异步网络编程（TCP/UDP）

`asyncio`内置异步网络套接字，可实现高性能的异步服务器/客户端：

```Python

import asyncio

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """处理客户端连接（异步TCP服务器）"""
    # 获取客户端地址
    addr = writer.get_extra_info('peername')
    print(f"客户端 {addr} 连接")

    # 异步读取客户端数据（非阻塞）
    data = await reader.read(1024)
    message = data.decode('utf-8')
    print(f"收到 {addr} 消息：{message}")

    # 异步发送响应
    response = f"服务器已收到：{message}"
    writer.write(response.encode('utf-8'))
    await writer.drain()  # 确保数据发送完成

    # 关闭连接
    print(f"关闭客户端 {addr} 连接")
    writer.close()
    await writer.wait_closed()

async def async_tcp_server():
    """启动异步TCP服务器"""
    # 创建异步服务器
    server = await asyncio.start_server(
        handle_client,  # 客户端连接处理函数
        '127.0.0.1',    # 监听地址
        8888            # 监听端口
    )

    addr = server.sockets[0].getsockname()
    print(f"异步TCP服务器启动：{addr}")

    # 运行服务器直到停止（可按Ctrl+C终止）
    async with server:
        await server.serve_forever()

# 启动服务器（测试：终端执行 telnet 127.0.0.1 8888）
# asyncio.run(async_tcp_server())

# 异步TCP客户端
async def async_tcp_client():
    """异步TCP客户端"""
    # 连接服务器
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    # 发送数据
    message = "Hello Async TCP Server!"
    writer.write(message.encode('utf-8'))
    await writer.drain()

    # 接收响应
    data = await reader.read(1024)
    print(f"收到服务器响应：{data.decode('utf-8')}")

    # 关闭连接
    writer.close()
    await writer.wait_closed()

# 先启动服务器，再运行客户端
# asyncio.run(async_tcp_client())
```

---

## 模块6：asyncio与第三方库结合（实战场景）

### 6.1 异步HTTP请求（aiohttp）

`requests`是同步HTTP库，`aiohttp`是异步替代方案，性能提升10倍以上：

```Bash

pip install aiohttp  # 安装异步HTTP库
```

```Python

import asyncio
import aiohttp

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """异步获取URL数据（生产级写法）"""
    try:
        # 异步GET请求，设置超时（避免无限等待）
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=5)  # 总超时5秒
        ) as response:
            return {
                "url": url,
                "status": response.status,
                "content_length": response.content_length,
                "error": None
            }
    except aiohttp.ClientError as e:
        return {"url": url, "status": None, "content_length": None, "error": str(e)}

async def aiohttp_demo():
    """批量异步HTTP请求"""
    # 创建异步会话（复用连接池，提升性能）
    async with aiohttp.ClientSession() as session:
        urls = [
            "https://www.baidu.com",
            "https://www.python.org",
            "https://www.nonexistent-url.com"  # 无效URL，测试异常
        ]
        # 并发请求（控制并发数=2）
        sem = asyncio.Semaphore(2)
        async def limited_fetch(url):
            async with sem:
                return await fetch_url(session, url)
        
        # 创建任务并执行
        tasks = [asyncio.create_task(limited_fetch(url)) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # 打印结果
        for res in results:
            print(f"URL：{res['url']} | 状态码：{res['status']} | 错误：{res['error']}")

asyncio.run(aiohttp_demo())
```

### 6.2 异步数据库操作（aiomysql）

`pymysql`是同步MySQL驱动，`aiomysql`是异步替代方案：

```Bash

pip install aiomysql  # 安装异步MySQL驱动
```

```Python

import asyncio
import aiomysql

async def async_mysql_demo():
    """异步MySQL操作（生产级：连接池+事务）"""
    # 创建异步连接池（复用连接，避免频繁创建/关闭）
    pool = await aiomysql.create_pool(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        db='test',
        charset='utf8mb4',
        maxsize=10,  # 连接池最大连接数
        minsize=2    # 连接池最小空闲连接数
    )

    # 异步查询（带事务）
    async with pool.acquire() as conn:
        # 开始事务
        await conn.begin()
        try:
            # 创建字典游标（结果返回字典，而非元组）
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # 执行查询
                await cur.execute("SELECT * FROM user LIMIT 5")
                results = await cur.fetchall()
                print("异步查询结果：", results)

                # 执行更新（事务内）
                await cur.execute("UPDATE user SET status=1 WHERE id=%s", (1,))
                await conn.commit()  # 提交事务
        except Exception as e:
            await conn.rollback()  # 异常回滚
            print(f"数据库操作异常：{e}")

    # 关闭连接池
    pool.close()
    await pool.wait_closed()

asyncio.run(async_mysql_demo())
```

---

## 模块7：性能优化与最佳实践（生产级）

### 7.1 核心性能优化技巧

1. **避免同步阻塞调用**：

    - 严禁在协程中使用`time.sleep()`/`requests.get()`/`pymysql`等同步阻塞函数；

    - 若必须使用，通过`loop.run_in_executor()`提交到线程池/进程池：

        ```Python
        
        import asyncio
        import time
        
        def blocking_func():
            """同步阻塞函数（无法替换为异步）"""
            time.sleep(2)
            return "完成"
        
        async def executor_demo():
            loop = asyncio.get_running_loop()
            # 提交到线程池执行（不阻塞事件循环）
            result = await loop.run_in_executor(None, blocking_func)
            print(f"阻塞函数结果：{result}")
        
        asyncio.run(executor_demo())
        ```

2. **复用连接池**：

    - 异步HTTP/数据库操作必须使用连接池（`aiohttp.ClientSession`/`aiomysql.Pool`），避免频繁创建/关闭连接；

3. **控制并发数**：

    - 使用`Semaphore`限制最大并发数（如HTTP请求并发数=50-100），避免目标服务拒绝连接；

4. **使用高性能事件循环**：

    - Linux下替换为`uvloop`（性能提升2-4倍），Windows无此优化；

5. **避免细粒度协程**：

    - 细粒度协程（如单次IO操作）会增加切换开销，尽量合并为大协程。

### 7.2 最佳实践

1. **异常处理全覆盖**：

    - 捕获`TimeoutError`/`ConnectionError`/`CancelledError`等异步异常；

    - `gather`使用`return_exceptions=True`时，需检查结果是否为异常对象；

2. **资源自动释放**：

    - 使用`async with`/`async for`自动释放异步资源（连接/锁/队列）；

3. **任务取消与清理**：

    - 未完成的Task必须调用`cancel()`取消，避免资源泄漏；

    - 程序退出前等待所有Task完成或取消；

4. **调试与日志**：

    - 开启异步调试模式：`PYTHONASYNCIODEBUG=1 python script.py`；

    - 为Task命名（`create_task(coro, name="task-1")`），便于日志排查；

5. **避免过度异步**：

    - CPU密集型任务优先使用`multiprocessing`，结合`asyncio`实现“多进程+异步”；

    - 简单场景（单IO操作）无需异步，同步代码更易维护。

### 7.3 常见坑点

1. **遗漏** **`await`**：忘记在可等待对象前加`await`，导致返回协程对象而非结果；

2. **同步阻塞混入**：协程中调用同步阻塞函数，导致事件循环卡住；

3. **Task未等待**：创建Task后未`await`，程序退出时Task被强制终止；

4. **资源未释放**：未关闭连接池/文件，导致句柄泄漏；

5. **锁使用不当**：异步锁未正确释放，导致死锁；

6. **忽略队列** **`task_done()`**：`queue.join()`会永久阻塞，直到所有元素被`task_done()`标记。

---

## 模块8：总结（核心知识点回顾）

1. **asyncio核心价值**：解决IO密集型任务的并发问题，通过“协程+事件循环”实现单线程高并发，耗时≈最长IO任务耗时，资源占用远低于多线程；

2. **核心语法**：`async def`定义协程，`await`暂停协程，`asyncio.run()`管理事件循环，`create_task()`实现并发；

3. **核心API**：

    - 并发管理：`gather()`（批量等待）、`wait()`（灵活等待）；

    - 同步控制：`Lock`（资源竞争）、`Semaphore`（并发控制）、`Event`（协程通信）、`Queue`（数据传递）；

    - 超时控制：`wait_for()`、`timeout`参数；

4. **最佳实践**：

    - 避免同步阻塞，复用连接池，控制并发数；

    - 全覆盖异常处理，自动释放资源，合理取消Task；

    - IO密集型用`asyncio`，CPU密集型结合多进程。

`asyncio`是Python异步编程的标准库，掌握上述内容可覆盖从入门到生产级应用的全维度需求，也是FastAPI、Tornado等高性能异步Web框架的核心底层依赖。