d1 = dict()
d2 = {
    "name": "jom",
    "age": 12,
}
print(d1)
print(d2)
del d2["name"]
print(d2)

address = d2.get("address", "default address")
print(address)
# 添加新的键值对
# 字典对象["key"]=value
# key 当key不存在时，直接将value加入
# 当key存在时，覆盖操作
d2["details"] = "详细信息"
print(d2)
# list化
result = list(d2)
print(result)
print("---" * 10)
# 得到所有的key
keys = d2.keys()
print(keys)
values = d2.values()
print(values)

if "address" in d2:
    print("存在")
else:
    print("不存在")

# 通过二元元组形式创建
# (a,b) 元组之中仅有两个元素
nums = [
    ("name", "kom"),
    ("age", 11),
    ("address", "ShangHai"),
    ("details", "详细信息"),
]
somethings = dict(nums)
print(somethings)


some = dict(number=123, number2=456, number3=789)
print(some)
