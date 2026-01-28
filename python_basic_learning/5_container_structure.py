"""=== 容器类型 ==="""

# 1.列表 list
# 定义
alist = list()
blist = [1, 2, 3, 4, 5, 6]
print(alist, blist)
# 查找:按照下标查找元素，按照元素查找下标
index_2_value = blist[2]
print(index_2_value)
# 增加:在末尾增加元素，或者在任意位置增加元素
clist = [1, 2, 4, 5, 6]
# O（1）在末尾增加元素使用append(增加元素对象)
clist.append(7)
print("append >>> ", clist)
# O（n）在任意位置添加元素使用insert(添加位置，添加元素对象)
clist.insert(2, 3)
print("insert >>> ", clist)
# 列表扩展 目标对象1.extend(目标对象2) 将目标对象2先拆解，然后逐个添加到目标对象1之后
dlist = [1, 2, 3]
elist = [4, 5, 6]
dlist.extend(elist)
print(dlist)
# 修改 根据下标修改元素
flist = [1, 2, 3, 0, 5, 6]
flist[3] = 4
print("update:", flist)
# 删除 （1）.按照索引删除 （2）按照值对象删除 （3）删除末尾最后的一个元素
print(f"flist删除之前为:{flist}")
del flist[4]
print(f"flist删除之后为:{flist}")
flist.remove(6)
print(f"remove 之后的结果为:{flist}")
res = flist.pop()
print(f"pop value is {res},pop之后的结果为:{flist}")
# 常用方法：切片，统计个数、反转、排序
glist = [12, 3, 4, 52, 3, 5, 1, 2, 5, 12, 5, 12, 241, 34123]
# 得到index=1 to index=6 结束之前的元素 [起始下标:终止下标]
split_obj = glist[1:7]
print(split_obj)
# 统计个数 被统计对象.count(被统计元素)
c5 = glist.count(5)
print(f"在{glist}之中存在{c5}个5")
# reverse 反转函数
hlist = [3, 2, 1]
hlist.reverse()
print("排序之前的结果为:", glist)
glist.sort(key=lambda x: x, reverse=True)
print(glist)
print("===" * 30)
# 2.元组 tuple
# 定义
atuple = tuple()
btuple = (1, 2, 3, 4, 5, 1)
print(atuple, btuple)
# 查找 按照下标查找
index_4_value = btuple[4]
print(index_4_value)
# 常用方法：切片，统计
some = btuple[1:4]
print("切片结果为:", some)
print("1元素的个数为:", btuple.count(1))
print("===" * 30)
# 3.字典 dict
# 定义
adict = dict()
bdict = {"name": "jom", "age": 18}
print(adict, bdict)
# 查找 列表和元组查找元素，通常通过下标查找元素，但字典不同，字典通过key查找
name = bdict["name"]  # 字典对象["key"] 》》》 key对应的value
print(f"name is {name}")
# 增加
bdict["details"] = "详细信息"  # 字典对象["增加的key"]="增加的key对应的value"
print(bdict)
# 修改:通过key进行修改
bdict["details"] = "这是修改之后的结果"
print(bdict)
# 删除
del bdict["name"]
print(bdict)
# 常用方法：获取所有键、获取所有值，获取所有键值对
# 获取所有的键 keys()
keys = bdict.keys()
print(f"bdict字典的所有key:{keys}")
# 获取所有的值 values()
values = bdict.values()
print(f"bdict字典的所有value:{values}")
# 获取所有的键值对 items()
items = bdict.items()
print(f"bdict字典的所有键值对:{items}")
for key, value in bdict.items():
    print(key, value)
print("===" * 30)
# 4.集合 set
# 定义
aset = set()
bset = {1, 2, 3, 4, 5, 6, 7, 8, 9, 1}
print(aset, bset)  # 对元素进行自动去重处理
# 查找 无索引结构，不可以根据下标查找
# 无序性的体现
cset = set()
cset.add(1)
cset.add(5)
cset.add(99)
print(cset)
print(5 in cset)
print(2 in cset)
# 增加 在列表之中，在末尾增加元素使用append(添加元素对象)，在集合之中，在末尾添加元素使用add(添加元素对象)
cset.add(0)
print(cset)
# 删除：针对集合删除，使用数值对应删除remove
cset.remove(1)
print(cset)
# 常用方法：常见的集合运算：交集 并集 差集 对称差集
dset = {1, 2, 3, 4, 5, 6}
eset = {4, 5, 6, 7, 8, 9}
print(f"交集运算(&):{dset & eset}")  # 哪些元素同时在d之中，也在e之中
print(f"并集运算(|):{dset | eset}")  # d和e的所有元素
print(f"差集运算(-):{dset - eset}")  # dset中去除d和e的共同值之后，还剩下哪些元素
print(f"差集运算(-):{eset - dset}")
print(f"对称差集运算(^):{dset ^ eset}")  # 对称差集运算
#
#
#
#
