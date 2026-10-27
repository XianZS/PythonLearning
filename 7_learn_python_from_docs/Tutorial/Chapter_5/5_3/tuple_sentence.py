# 初始化空元组：tuple()
# 变量=(var1,var2,var3,...,varn)
# t1 = tuple()
# print(t1)
# 不可变性
t2 = (1, 2, 3)
print(t2)
# 可以通过下标访问
print(t2[1])
# 第二种创建方式
t3 = 123, 456, 789
print(t3)

"""
对象 是否可变性 是否可以通过下标访问    能否作为字典对象的key
元组    不可变      可以                    可以
列表    可变        不可以                  不可以
"""

t4 = (1,)
print(t4)

stus = (
    ("jom", 21, "ShangHai"),
    ("kom", 22, "HeBei"),
    ("lom", 23, "Xi'an"),
)
print(stus)
print("---" * 10)
for name, age, address in stus:
    print(f"[{name}] >>> {age}")
