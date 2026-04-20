"""
itertools 标准库学习
"""

import itertools as it

# 1、核心概念解读
# 什么是迭代器？
# 是一个可以记住遍历位置的对象，主要是实现了__iter__和__next__方法
# 如果想要逐个返回元素，那么就需要使用next来调用
# 优势：惰性计算，不会占用过多的内存
# itertools标注库的特点
# 函数都是“纯函数”，不修改原本的迭代器对象，而是返回新的迭代器
# 2、无限迭代器
# 永不停歇的序列
# count(start=0,step=1)
counter = it.count(start=100, step=100)
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(f"前5个元素为:{list(it.islice(counter, 5))}")
# 无限循环遍历可迭代对象
# 12小时制度，循环迭代0~11之间的小时显示
datas = it.cycle([x for x in range(0, 12)])
# print(next(datas))
for x in range(15):
    print(f"{next(datas)} ", end="")
print()
# 重复生成某一个对象
# repeat(object,times=None)
# 无限次 重复生成hello
r1 = it.repeat("hello")
# 有限次 重复生成hello
r2 = it.repeat("hello", times=3)
print(f"r1:{r1}")
print(f"r2:{r2}")
for x in range(3):
    print(f"[INFO-{x}]:{next(r2)}")

# 3、有限迭代器
# 处理有限长度的序列
# 1、chain(iterables) 拼接多个迭代器
list1, list2, list3 = [1, 2, 3], ["a", "b", "c"], ["jom", "kom", "lom"]
chained = it.chain(list1, list2, list3)
print(f"chained:{chained},type:{type(chained)}")
print(f"chained-list:{list(chained)}")
list4 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# [1,2,3,4,5,6,7,8,9]
