"""
# 流程控制

1.分支结构
    if-else if-elif-else
2.循环结构
    for while 嵌套循环
3.循环控制结构
    continue break pass
"""

name = "jack"
# name = input()
if name == "admin":
    print("管理员")
else:
    print("普通用户")

if name == "admin":
    print("管理员")
else:
    if name == "user":
        print("普通用户")
    else:
        print("游客")

if name == "admin":
    print("admin")
elif name == "user":
    print("普通用户")
else:
    print("游客")

# for 循环
# 根据下标循环
nums = [123, 321, 5, 42, 5, 4, 23125, 124, 6432]
L = len(nums)
# range(起始下标，终止下标，步长) range(1,10) [1,10) 1,2,3,...,9
print("下标循环:", end="")
for index in range(0, L):
    print(nums[index], " ", end="")
print()
print("元素循环:", end="")
# 根据元素循环
for child in nums:
    print(child, " ", end="")
print()

# while 循环条件：
#     当循环条件成立时，继续执行while之中的代码
# 1~100
sum_number = 0
now_number = 1
while now_number <= 100:
    sum_number += now_number
    now_number += 1
print(sum_number)
# 嵌套循环
for x in range(1, 10):
    for y in range(1, x + 1):
        print(f"{x}*{y}={x * y}   ", end="")
    print()
# 循环控制结构
# continue:不执行当前循环所剩的任何语句，直接进行下一次循环
for x in range(1, 10):
    if x % 2 == 0:
        # 偶数
        continue
    else:
        print(f"奇数{x} ", end="")
# break: 直接跳出当前循环，并且不执行当前循环之后的所有循环
# 循环内跳出，就需要使用break
number = 0
now_number = 1
while True:
    number += now_number
    now_number += 1
    if now_number > 100:
        break
print(number)

# pass:不影响当前循环的执行，只充当一个占位符的作用
for x in range(1, 10):
    if x % 2 == 0:
        pass
    else:
        print(f"奇数:{x} ", end="")
    print("=== test ===")

# 猜数字 猜到53算胜利
number = int(input())
while True:
    if number == 53:
        print("恭喜你，猜中了，答案就是53!!!")
        break
    else:
        if number > 53:
            print("恭喜你才错误，需要重新猜数字，猜测一个小数字: ", end="")
        else:
            print("恭喜你猜错误，需要重新猜数字，猜测一个更大的数字: ", end="")
        number = int(input())


#
#
#
#
#
#
