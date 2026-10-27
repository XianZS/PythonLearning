nums = [1, 2, 3, 3]
print(f"[修改前] >>> {nums}")

nums.append(4)
print(f"[修改后-append] >>> {nums}")

nums.extend([5, 6, 7])
print(f"[修改后-extend] >>> {nums}")

nums.insert(0, -1)
print(f"[修改后-insert] >>> {nums}")
nums.insert(1, 0)
print(f"[修改后-insert] >>> {nums}")

nums.remove(3)
print(f"[修改后-remove] >>> {nums}")

pop_default = nums.pop()
print(f"[默认返回值] >>> {pop_default}")
print(f"[修改后-pop-default] >>> {nums}")
pop_1 = nums.pop(1)
print(f"[弹出下标为1处的元素] >>> {pop_1}")
print(f"[修改后-pop-index_is_1] >>> {nums}")

nums.clear()
print(f"[修改后-clear] >>> {nums}")

nums = [1, 2, 3, 4, 4, 5, 6, 7, 2, 3, 0]
index_2 = nums.index(2)
print(f"元素2出现在{nums}列表之中的位置==={index_2}")

count_0 = nums.count(0)
print(f"元素3在{nums}列表之中出现了{count_0}次")


print(nums)
nums.sort(reverse=True)
print(nums)

some = ["jom", "kom", "lom"]
print(some)
some.reverse()
print(some)

news = some.copy()
news[1] = "pom"
print(some)
