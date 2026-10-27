# nums = []
# for x in range(1, 101):
#     nums.append(x)
# print(nums)
import math

nums = [x for x in range(1, 101)]
# print(nums)

# [迭代元素 for 迭代序列 判断语句（可选参数内容）]
xs = [1, 2, 34, 3, 1, 23, 1, 2]
ys = [22, 2, 343, 3, 431, 2343, 1, 212]
# 判断xs和ys之中不同的元素
result = [(x, y) for x in xs for y in ys if x != y]
# print(result)
result = [(xs[index], ys[index]) for index in range(len(xs)) if xs[index] != ys[index]]
print(result)

infs = [math.inf for _ in range(9)]
print(infs)
