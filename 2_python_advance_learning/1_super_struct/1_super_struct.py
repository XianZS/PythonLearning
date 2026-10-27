# [collections]Counter, defaultdict, deque, namedtuple, deque
# [附加]frozenset, heapq
# [来自于第三方包之中]numpy pandas


# 1.collections
import collections


# (1)Counter:对可迭代对象进行分类计数处理
print("=== Counter ===")
names = ["aom", "som", "dom", "som", "kom", "hom", "kom", "aom", "aom", "aom"]
res = collections.Counter(names)
print(res)  # Counter({'aom': 4, 'som': 2, 'kom': 2, 'dom': 1, 'hom': 1})
print(res["kom"])  # 2
# (2)defaultdict
print("=== defaultdict ===")
adict = {"name": "jom", "age": 18, "details": "详细信息"}
print(adict["name"])  # 根据存在的key，去访问value
# print(adict["address"])  # 根据不存在key，去访问value，KeyError: 'address'
bdict = collections.defaultdict(list)
cdict = collections.defaultdict(int)
print(bdict, cdict)
print(bdict["address"], cdict["address"])
# 针对高级字典defaultdict而言，当访问不存在的key时，会根据创建类型返回不同的结果
# list >>> []; int >>> 0; tuple: ()
# defaultdict访问不存在key，会执行哪些操作？
# （1）检查key是否存在
# （2）当key存在时，返回对应的value
# （3）当key不存在时，检查创建类型，假设创建类型是int，那么就会创建一个key-value
#   key：不存在的key，这里面就可以是address
#   value：根据创建类型，这里面就是0
print(bdict, cdict)
names = ["aom", "som", "dom", "som", "kom", "hom", "kom", "aom", "aom", "aom"]
edict = dict()
for name in names:
    if name in edict.keys():
        edict[name] += 1
    else:
        edict[name] = 1
print(edict)
fdict = collections.defaultdict(int)
for name in names:
    fdict[name] += 1
print(fdict)

# (3)双端队列deque
print("=== deque ===")
# deque 和 list 区别
alist = ["a", "b", "c"]
alist.append("d")  # 时间复杂度是 O(1)
print(f"append >>> {alist}")
alist.pop()  # 时间复杂度是 O(1)
print(f"pop >>> {alist}")
alist.insert(0, "q")
print(f"insert >>> {alist}")  # 时间复杂度是0(n)
alist.pop(0)
print(f"pop >>> {alist}")  # 时间复杂度是O(n)
bdeque = collections.deque([])
# 双端队列：在末尾进行操作，时间复杂度都是O(1)
bdeque.append("a")
bdeque.append("b")
# 双端队列：在头部进行操作，时间复杂度也是O(1)
bdeque.appendleft("c")
bdeque.appendleft("d")
print(f"bdeque >>> {bdeque}")
res_2 = bdeque.pop()
print(res_2)
res_3 = bdeque.popleft()
print(res_3)
print(bdeque)

# (4)namedtuple 命名元组
print("=== namedtuple ===")
atuple = (1, 2, 3)  # 有序，不可变，可hash
# 只能根据下标访问，不可以根据key/字段/属性来访问
print(atuple[0])
# 语法规范，本质上说，namedtuple其实就是只有属性字段的类，并不具备任何方法
Person = collections.namedtuple("Person", ["name", "age", "details"])
p1 = Person(name="jom", age=18, details="命名元组-详细信息")
Stu = collections.namedtuple("Stu", "name age details address")
stu1 = Stu(name="jom", age=19, details="相信信息", address="地址")
print(stu1)
print(p1)
print(p1[0])
print(p1.name)
# p1.age = 20

# 2.其它的附加数据结构
# (1)不可变集合 frozenset
print("=== frozenset ===")
aset = {1, 2, 3}  # 无序性，无重复元素
print(aset, type(aset))
# 缺点：可变的
af = frozenset()
bf = frozenset("hello")
print(af, bf)
# bf.add("k")
# print(bf)
# 抛弃了普通集合的可变性，将其变为不可变性

# (2)heapq堆
import heapq

# 初始化一个堆对象
some = [3, 1, 4, 2]
heapq.heapify(some)
print(some)
heapq.heappush(some, 0)
print(some)
res = heapq.heappop(some)
print(res, some)
# 要求弹出一个序列之中，前n大的数字
nums = [3, 2, 32, 5, 123, 5, 132, 5, 123, 234543, 123, 312, 51]
# 前3个大的数字
heapq.heapify(nums)
res = heapq.nlargest(3, nums)
print(res)
# 前3个小的数字
res1 = heapq.nsmallest(3, nums)
print(res1)
print(nums)

# 3.来自第三方包的高级数据结构
import numpy as np

array1 = np.array([1, 2, 3])
print(array1, type(array1))

import pandas as pd

array2 = pd.array([1, 2, 3])
print(array2)
print(type(array2))


if __name__ == "__main__":
    pass
