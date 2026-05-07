"""
multiprocessing 标准库学习
"""

import multiprocessing
import os
import time


# 基础-1：multiprocessing创建方式
# 直接实例化Process类
def task(name, delay):
    """
    进程执行的任务
    print>>>
        [进程名]:B，启动（PID：26272，父进程PID:28824）
        [进程名]:A，启动（PID：24964，父进程PID:28824）
    """
    print(f"[进程名]:{name}，启动（PID：{os.getpid()}，父进程PID:{os.getppid()}）")
    time.sleep(delay)
    print(f"[{name}]进程执行结束")


def test1():
    p1 = multiprocessing.Process(target=task, args=("A", 2))
    p2 = multiprocessing.Process(target=task, args=("B", 3))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("所有进程执行完毕")


# 继承Process类，重写run()方法
class MyProcess(multiprocessing.Process):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        print(f"[进程-name]:{self.name},[进程-PID]:{os.getpid()}")
        time.sleep(self.delay)
        print(f"进程{self.name}执行结束")


def test1_1():
    p1 = MyProcess("A", 2)
    p2 = MyProcess("B", 3)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


# 基础-2：进程的启动方法
# multiprocessing.set_start_method() 三种
# spawn：比较适合跨平台
# fork：Linux
# forkserver：Linux
def test2():
    multiprocessing.set_start_method("spawn")
    print(str(multiprocessing.get_start_method))


# 基础-3：核心基础属性与方法
def test3():
    now_obj = multiprocessing.current_process()
    print(f"[当前执行的进程对象]:{now_obj}")
    p = MyProcess(name="A", delay=3)
    p.start()
    print(f"[当前进程的PID]:{p.pid}")
    print(f"[当前进程的name]:{p.name}")
    print(f"[当前进程是否存活]:{p.is_alive()}")


# 进阶-1：通过IPC方式通信
# 队列
"""模拟生产者和消费者的过程"""


def producer(q):
    """生产者"""
    for i in range(5):
        q.put(i)
        print(f"生产者放入数据:{i}")


def consumer(q):
    """消费者"""
    while True:
        data = q.get()
        if data is None:
            break
        print(f"消费者取出数据:{data}")


# if __name__ == "__main__":
#     q = multiprocessing.Queue()
#     p_prod = multiprocessing.Process(target=producer, args=(q,))
#     p_cons = multiprocessing.Process(target=consumer, args=(q,))
#     p_prod.start()
#     p_cons.start()
#     p_prod.join()
#     q.put(None)  # None 表示消费者结束标记
#     p_cons.join()


# 进阶-2：通过双向管道实现进程之间的通信
def sender(conn):
    """发送方逻辑实现"""
    conn.send("Hello from sender!")
    conn.send([1, 2, 3])
    conn.close()


def receiver(conn):
    """接收方逻辑实现"""
    while True:
        try:
            data = conn.recv()
            print(f"接收方接收到数据:{data}")
        except EOFError:
            break
        except Exception as e:
            print(f"[ERROR]:{e}")


# if __name__ == "__main__":
#     parent_conn, child_conn = multiprocessing.Pipe(duplex=True)
#     p_sender = multiprocessing.Process(target=sender, args=(child_conn,))
#     p_receiver = multiprocessing.Process(target=receiver, args=(parent_conn,))
#     p_sender.start()
#     p_receiver.start()
#     p_sender.join()
#     p_receiver.join()
#     print("管道通信结束")


# 进阶-3：通过共享对象实现进程之间的通信
def modify_list(shared_list, lock):
    """共享对象操作函数"""
    with lock:
        shared_list.append(multiprocessing.current_process().name)
        print(f"当前共享列表为:{shared_list}")


# if __name__ == "__main__":
#     # 创建manager对象
#     with multiprocessing.Manager() as manager:
#         # 创建共享列表和锁
#         shared_list = manager.list()
#         lock = multiprocessing.Lock()
#         # 创建多个进程来修改共享列表
#         processes = []
#         for i in range(9):
#             p = multiprocessing.Process(
#                 target=modify_list, args=(shared_list, lock), name=f"进程-{i + 1}"
#             )
#             processes.append(p)
#             p.start()
#         for i in processes:
#             i.join()
#         print(f"最终共享列表为:{shared_list}")


# 进阶-4：通过lock解决共享资源竞争问题
def increment(share_value, lock):
    """通过对共享变量进行累加操作"""
    for _ in range(100000):
        with lock:
            share_value.value += 1


# if __name__ == "__main__":
#     share_value = multiprocessing.Value("i", 0)
#     lock = multiprocessing.Lock()
#     p1 = multiprocessing.Process(target=increment, args=(share_value, lock))
#     p2 = multiprocessing.Process(target=increment, args=(share_value, lock))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     print("Lock加锁机制测试成功")
#     print(f"[share_value]:{share_value}")


# 进阶-5：进程池
# 避免进程创建和进程销毁的开销，实现进程的复用
def square(x):
    """计算平方：模拟CPU密集型任务"""
    time.sleep(0.1)
    return x * x


if __name__ == "__main__":
    # 创建进程池
    # 语法规范：multiprocessing.Pool(processes=number:int) 指明最大容量进程数，默认为CPU核心数
    with multiprocessing.Pool(processes=4) as pool:
        # === pool.map 模拟批量提交任务 ===
        start_time = time.time()
        res_map = pool.map(square, range(10))
        print(f"map结果为:{res_map},耗时:{time.time() - start_time:.2f}s")
        # === pool.apply_async 单个提交任务，异步获取结果，不是按照原顺序 ===
        start_time = time.time()
        res_async = [pool.apply_async(square, args=(i,)) for i in range(10)]
        res_async = [res.get() for res in res_async]
        print(f"apply_async结果为:{res_async},耗时:{time.time() - start_time:.2f}s")
        # === pool.imap_unordered 批量提交，结果按照完成顺序返回 ===
        start_time = time.time()
        res_unordered = pool.imap_unordered(square, range(10))
        print(
            f"imap_unordered结果为:{list(res_unordered)},耗时:{time.time() - start_time}s"
        )
