"""
queue标准库
"""

import queue
import time
import threading

# 基础-1：队列 先进先出的数据结构
# 语法规范：
# 创建时：maxsize最大容量
# 核心方法：put get qsize empty full
q = queue.Queue(maxsize=3)
for x in range(1, 4):
    q.put(x)
print(f"[size]:{q.qsize()}")
if q.empty():
    print("队列为空")
else:
    while not q.empty():
        print(f"[q] >>> {q.get()}")
print(f"[size]:{q.qsize()}")
print("-" * 10)
# 基础-2：LIFO栈 先进后出
lq = queue.LifoQueue()
for x in range(1, 4):
    lq.put(x)

if lq.empty():
    print("栈为空")
else:
    while not lq.empty():
        print(f"[lq] >>> {lq.get()}")
print("-" * 10)
# 基础-3：优先级队列
# child-type:tuple
# child-content:(pri,data)
# 优先级数值越小，优先级越高
pq = queue.PriorityQueue()
pq.put((3, "user"))
pq.put((5, "kom"))
pq.put((1, "root"))
pq.put((2, "admin"))
pq.put((9, "lom"))
while not pq.empty():
    print(f"[pq] >>> {pq.get()}")
print("-" * 10)

# 进阶-1：阻塞和非阻塞操作
# block=True/False
# True：可以设置阻塞时间，超出时间之后会抛出满/空异常
# False：立刻抛出异常
# timeout=number:int (单位：秒)
q = queue.Queue(maxsize=3)
q.put(1)
q.put(2)
q.put(3)
try:
    q.put(4, block=False, timeout=3)
except queue.Full:
    print("队列-满")
except queue.Empty:
    print("队列-空")


# 进阶-2：任务同步
# put默认调用task_done()方法
def worker(q):
    while True:
        item = q.get()
        print(f"任务{item}正在执行")
        time.sleep(0.5)
        print(f"任务{item}执行结束")
        q.task_done()
        # 通知任务完成


q = queue.Queue()

# 创建守护线程 （threading）
t = threading.Thread(target=worker, args=(q,), daemon=True)
# 启动守护线程
t.start()

# 提交任务
for i in range(3):
    q.put(f"[任务 - {i}]")
print("等待任务执行结束")
q.join()
print("全部任务执行结束")

# 进阶-3：多线程安全
# 主要来自于互斥锁和条件变量
# 互斥锁：每次put/get都会自动获取锁，然后执行结束之后释放
# 条件变量：线程之间的通信
