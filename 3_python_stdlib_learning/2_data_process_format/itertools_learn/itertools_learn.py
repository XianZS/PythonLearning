"""
itertools 标准库学习
"""

import operator
import itertools

# 1、核心概念
# 什么是迭代器：本身是一个可以记住遍历位置的对象，这个对象必须要实现__iter__和__next__方法
# 在调用next(迭代器对象)时，可以逐个迭代器对象的元素
# 在itertools里面所有函数的返回值都是迭代器，如果想要查看返回值，那么需要对返回结果进行列表list化。
# 2、无限迭代器
# 永不停歇的生成元素
# counter(start=number,step=number)
# 从100开始，步伐为50的迭代器
c1 = itertools.count(start=100, step=50)
print(next(c1), next(c1), next(c1))
# cycle(iterable)，对iterable进行无限迭代
times = [x for x in range(0, 12)]
print(times)
abled = itertools.cycle(times)
print(type(abled))
for x in range(20):
    print(f"{next(abled)} ", end="")
# repeat(object)：重复生成单一对象
r1 = itertools.repeat("admin")  # 重复生成无限次
r2 = itertools.repeat("root", times=10)  # 重复生成times次
for x in range(5):
    print(f"{next(r2)} ", end="")
print()
# 3、有限迭代器
# 拼接多个迭代器对象 chain(iterables)
iter1 = ["aom", "som", "dom"]
iter2 = [1, 2, 3]
iter3 = ["a", "b", "c"]
res1 = itertools.chain(iter1, iter2, iter3)
print(list(res1), type(res1))
# 不等长迭代器的zip
# zip_longest(iterables,fillvalue=None)
list1 = [1, 2, 3]
list2 = ["a", "b"]
print(f"普通zip返回结果:{list(zip(list1, list2))}")
# 普通zip返回结果:[(1, 'a'), (2, 'b')]
res2 = itertools.zip_longest(list1, list2, fillvalue="填充字段")
print(f"zip_longest返回结果:{list(res2)}")
# 迭代器的切片操作
# islice(iterables,start,stop,step)
# islice(可迭代对象，开始下标，终止下标，步伐)
counter = itertools.count(start=0, step=1)
# 截取从2~7之间的元素，步伐为2
sliced_1 = itertools.islice(counter, 2, 7, 2)
print(f"切片结果为:{list(sliced_1)}")  # [2,4,6]
# 快速生成前缀和（或者累积其它操作）
nums = [1, 2, 3, 4]
pres1 = itertools.accumulate(nums)
print(f"前缀和:{list(pres1)}")

pres2 = itertools.accumulate(nums, operator.mul)
print(f"累乘结果:{list(pres2)}")

pres3 = itertools.accumulate(nums, max)
print(f"累积最大数值:{list(pres3)}")
# 4、组合生成器
# 应用场景：排列组合
# product(iterables,repeat=1)
# 生成多个迭代器的笛卡尔积，repeat参数有表明重复生成的次数
l1 = ["a", "b"]
l2 = [1, 2]
print(f"笛卡尔积运算的结果为:{list(itertools.product(l1, l2, repeat=1))}")
# 生成可迭代对象之中的所有排序，顺序不同算不同
chars = ["a", "b", "c"]
print(f"全排列结果:{list(itertools.permutations(chars))}")
print(f"全排列结果:{list(itertools.permutations(chars, 2))}")
# 组合（不重复）
# 生成可迭代对象种元素的所有组合，（顺序不同算同一个，元素不重复），r是组合的长度
print(f"组合（不重复）:{list(itertools.combinations(chars, 2))}")
# 组合（可重复） 有点类似于combinations函数类似，但是元素是可以重复出现的
print(f"组合（可重复）：{list(itertools.combinations_with_replacement(chars, 2))}")
# 5、常见应用场景
# 数据处理：使用chain来合并数据，使用islice来切片大文件，使用accumulate来累积值
# 组合数学：使用permutations和combination来解决排列组合的问题
# 测试用例生成部分：用product生成所有参数组合的测试用例
# 循环控制部分：使用count来自动计数，使用cycle来循环切换状态
