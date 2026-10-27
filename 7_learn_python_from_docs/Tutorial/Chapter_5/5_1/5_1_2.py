deq = []
print(f"[初始队列] >>> {deq}")
# 模拟push
# 时间复杂度是 O(1)
deq.append(123)
deq.append(456)
deq.append(789)
print(f"[入队操作] >>> {deq}")
# 模拟pop
# 时间复杂度是 O(n)
deq.pop(0)
deq.pop(0)
print(f"[出队操作] >>> {deq}")
deq.clear()
print(f"[清空操作] >>> {deq}")
