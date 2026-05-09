"""
多线程：生产者消费者模型
- 2个厨师（生产者）随机生成菜品
- 3个服务员（消费者）取餐并且配送
- 队列最大容量为5，避免菜品堆积
"""

import queue
import threading
import time
import random


class Chef(threading.Thread):
    """生产者：厨师"""

    def __init__(self, name, dish_queue):
        super().__init__()
        self.name = name
        self.dish_queue = dish_queue

    def run(self):
        for _ in range(3):
            dish = f"{random.choice(['豆腐皮', '鸡肉', '牛肉'])}"
            try:
                self.dish_queue.put(dish, timeout=10)
                print(f"{self.name} 制作了 :{dish}")
            except queue.Full:
                print("队列-满")
            time.sleep(random.uniform(0.5, 1.5))


class Waiter(threading.Thread):
    """消费者"""

    def __init__(self, name, dish_queue):
        super().__init__()
        self.name = name
        self.dish_queue = dish_queue

    def run(self):
        while True:
            try:
                dish = self.dish_queue.get(timeout=10)
                print(f"{self.name} 配送了 :{dish}")
                time.sleep(random.uniform(1, 2))
                self.dish_queue.task_done()
            except queue.Empty:
                print("没有现成的菜品")
                break


if __name__ == "__main__":
    dish_queue = queue.Queue(maxsize=5)
    # 创建生产者
    chefs = [Chef(f"厨师-{i}", dish_queue) for i in range(2)]
    # 创建消费者
    waiters = [Waiter(f"服务员-{i}", dish_queue) for i in range(3)]
    for chef in chefs:
        chef.start()
    for waiter in waiters:
        waiter.start()
    # 等待所有的厨师做完菜
    for chef in chefs:
        chef.join()
    # 等待所有菜品配送完成
    dish_queue.join()
    print("=== 圆满结束 ===")
