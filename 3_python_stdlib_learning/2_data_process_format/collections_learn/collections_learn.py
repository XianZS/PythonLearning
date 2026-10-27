"""
collections 增强型数据结构
"""

import collections


# Counter：元素计数器
# 对可迭代对象之中的子元素进行计数处理
names = [
    "jom",
    "kom",
    "lom",
    "lom",
    "kom",
    "jom",
    "lom",
    "lom",
    "kom",
    "jom",
    "lom",
    "lom",
    "kom",
    "jom",
    "lom",
]
# 普通情况下
res = dict()
for name in names:
    if name in res:
        res[name] += 1
    else:
        res[name] = 1
print(res)
# 借助Counter元素计数器
res1 = collections.Counter(names)
print(res1, type(res1))


print("-" * 10)
# 2、带着自定义默认值的字典

names = [
    "jom",
    "kom",
    "lom",
    "lom",
    "kom",
    "jom",
    "lom",
    "lom",
    "kom",
    "jom",
    "lom",
    "lom",
    "kom",
    "jom",
    "lom",
]
# 普通情况下
res = dict()
for name in names:
    # 不判断
    # res[name] += 1
    # KeyError 不存在key
    # 不能确定初始值，所以解释器不能识别，那么就会报错。
    # if name in res:
    #     res[name] += 1
    # else:
    #     res[name] = 1
    pass

# 自定义一个默认值
# 如果key存在，那么就是用已经存在的数值
# 如果key不存在，那么就使用不存在的数值
# collections.defaultdict(<class type>)
# <class type>:int 0
# <class type>:list []
# <class type>:tuple ()
# <class type>:Bool False
res2 = collections.defaultdict(list)
for name in names:
    res2[name].append(name)
print(res2)

print("-" * 10)
# 3、namedtuple 命名元组
# 普通元组，只能通过下标进行访问，可读性差
# (name,age,address)
# example_data:(jom,11,A城市),(kom,22,B城市)
data = [("jom", 11, "A城市"), ("kom", 22, "B城市"), ("lom", 33, "C城市")]
for cho in data:
    print(f"{cho[2]} ", end="")
print()
# namedtuple：可以通过key-value的形式进行访问，可读性高
# 第一步：创建namedtuple子类，其实相当于只有属性的类对象
Point = collections.namedtuple("Point", ["x", "y"])
# 第二步：创建实例对象
p1 = Point(10, 20)
print(f"下标进行访问:x={p1[0]},y={p1[1]}")
print(f"通过键值对访问:x={p1.x},y={p1.y}")
print(type(p1))

# 4、deque双端队列
deq = collections.deque([])
print(deq, type(deq))
deq.append(1)
deq.append(2)
deq.append(3)

print(deq, type(deq))
# 从0开始打印，给队列头部添加0这个元素
deq.appendleft(0)
print(deq, type(deq))
# 从2开始打印，弹出0和1这两个元素
res_0 = deq.popleft()
res_1 = deq.popleft()
print(f"弹出的第一个元素为:{res_0},弹出的第二个元素为:{res_1}")
print(f"弹出之后的结果为:{deq}")
