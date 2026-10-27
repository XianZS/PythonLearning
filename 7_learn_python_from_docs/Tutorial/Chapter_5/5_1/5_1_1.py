s = []
print(f"[空栈] >>> {s}")
s.append(123)
s.append(456)
s.append(789)
print(f"[模拟push] >>> {s}")
s.pop()
print(f"[模拟pop] >>> {s}")
s.clear()
print(f"[模拟clear] >>> {s}")
# 先进后出的数据结构
# push：将元素加入栈顶
# pop：将元素从栈顶弹出
# clear：清空栈内所有元素
