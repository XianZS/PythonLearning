# for var in iterable任意可迭代对象:
#   ...

# 可迭代对象 iterable
names = ["jom", "kom", "lom"]
for name in names:
    print(name)

some = ["sosm", "dojn", "d1", "djiqj", "djow", "djwo"]
for index in range(len(some)):
    print(some[index])

# 找到some之中的d1元素，将d1替换为-1
# 遍历和修改不能同时出现
some_copy = some.copy()
for index in range(0, len(some_copy)):
    if some_copy[index] == "d1":
        some[index] = -1  # type:ignore
print(some)
