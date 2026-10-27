s1 = set()
print(f"[s1] >>> {s1}")
s2 = {1, 2, 3, 1}
print(f"[s2] >>> {s2}")

if 2 in s2:
    print("True")
else:
    print("False")

s3 = set("append")
s4 = set("add")
print(s3, s4)

# 交集
print(s3 & s4)
# 并集
print(s3 | s4)
# 仅存在于s3之中，但不存在于s4之中
print(s3 - s4)
print(s4 - s3)
# 不同时存在于s3和s4之中的对象
print(s3 ^ s4)
