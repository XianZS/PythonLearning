"""
threading 标准库学习
"""

import threading
import time

#
# # 基础-1：线程创建的两种方式
# # 第一种-直接实例化threading.Thread()类
# def task(name, spend_time):
#     import time
#
#     print(f"Thread {name} is start!")
#     time.sleep(spend_time)
#     print(f"Thread {name} is stop!")
#
#
# # 创建两个线程
# t1 = threading.Thread(target=task, args=("A", 1))
# t2 = threading.Thread(target=task, args=("B", 2))
# # t1.start()
# # t2.start()
# # t1.join()
# # t2.join()
# print("线程运行结束")
#
#
# # 第二种-继承threading.Thread()类，重写run()方法，适合复杂应用场景
# class MyThread(threading.Thread):
#     def __init__(self, name, delay):
#         super().__init__()
#         self.name = name
#         self.delay = delay
#
#     def run(self):
#         """线程执行的逻辑（start()会自动调用run()这个方法）"""
#         import time
#
#         print(f"[Thread]:{self.name} start!")
#         time.sleep(self.delay)
#         print(f"[Thread]:{self.name} stop!")
#
#
# t3 = MyThread("C", 3)
# t4 = MyThread("D", 4)
# # t3.start()
# # t4.start()
#
# # 基础-2：获取thread的基础属性和方法
# # 获取当前执行的线程对象
# now_thread = threading.current_thread()
# print(f"[now_thread]:{now_thread}")
# # 获取当前活跃的线程数量
# active_count_thread = threading.active_count()
# print(f"[active_count_thread]:{active_count_thread}")
# # 获取当前的线程名
# t5 = MyThread("E", 5)
# print(f"[thread-name]:{t5.name}")
# # 判断当前某个线程是否在运行
# print(f"[threading_is_alive]:{t3.is_alive()}")

# # 进阶-1：互斥锁
# # 共享资源
# count = 0
# # 创建互斥锁
# lock = threading.Lock()
#
#
# class MyThread(threading.Thread):
#     def __init__(self):
#         super().__init__()
#
#     def run(self):
#         with lock:
#             global count
#             time.sleep(1)
#             count += 1
#             strs = self.name + " now number is " + str(count)
#             print(strs)
#
#
# def test():
#     for _ in range(5):
#         th = MyThread()
#         th.start()
#
#
# test()
#
# # 进阶-2：可重入锁
# # threading.RLock()
# rlock = threading.RLock()
#
#
# def func1():
#     with rlock:
#         print("func1 get RLock")
#         func2()
#
#
# def func2():
#     with rlock:
#         print("func2 get RLock")
#
#
# t = threading.Thread(target=func1)
# t.start()
# t.join()
#


# 进阶-3：条件变量
# 线程之间的通信
def main():
    import threading
    import queue
    import time

    # 任务队列
    task_queue = queue.Queue(maxsize=5)
    # 创建条件变量（关联锁）
    cond = threading.Condition()

    def producer():
        for i in range(10):
            with cond:
                while task_queue.full():
                    cond.wait()
                task_queue.put(i)
                print(f"生产者执行任务{i}")
                cond.notify()  # 生产者通知消费者
            time.sleep(0.5)

    def consumer():
        for i in range(10):
            with cond:
                while task_queue.empty():
                    cond.wait()
                # 从就绪队列之中拿出一个任务对象
                task = task_queue.get()
                print(f"消费者消费任务 {task}")
                cond.notify()
            time.sleep(1)

    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    t_prod.start()
    t_cons.start()
    t_prod.join()
    t_cons.join()


# main()


# 进阶-4：通过信号量控制并发数量
def main4():
    import threading
    import time

    # threading.Semaphore(number:int) 表示当前最多允许3个线程并发执行
    sem = threading.Semaphore(3)

    def task(name):
        with sem:
            print(f"线程 {name} 正在执行")
            time.sleep(2)
            print(f"线程 {name} 执行完毕")

    threads = [threading.Thread(target=task, args=(i,)) for i in range(0, 6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# main4()


# 进阶-5：守护线程
# 防止主线程自动退出
def main5():
    import threading
    import time

    def daemon_task():
        while True:
            print("守护线程执行过程中......")
            time.sleep(1)

    t = threading.Thread(target=daemon_task, daemon=True)
    t.start()
    time.sleep(3)
    print("主线程执行结束，守护线程将自动退出")


# main5()
# 进阶-6：线程异常处理
def main6():
    class MyThread(threading.Thread):
        def run(self):
            try:
                print("线程开始执行")
                1 / 0
            except Exception as e:
                print(f"[ERROR]:{e}")

    t = MyThread()
    t.start()
    t.join()
    print("主线程继续执行")


main6()
