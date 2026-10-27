"""
# 变量和数据类型

1.标量类型
    （1）数值类型:
    int float complex bool
    （2）字符串
    str
    （3）空
    None
2.容器类型
    （1）列表 list
    （2）元组 tuple
    （3）字典 dict
    （4）集合 set
"""

# 标量类型
# int 整数
int_value = 123
print(int_value)
# float 类型 浮点数 无double类型
float_value = 123.4
print(float_value)
# 布尔数值 True or False
bool_value_1 = True
bool_value_2 = False
print(bool_value_1, bool_value_2)
# 复数类型：complex 1+2i
complex_value = complex(1, 2)
print(complex_value)
# 针对一个变量，不知道变量是什么，那么可以调用type()方法
print(type(complex_value), type(int_value))
# str 字符串的数值不可变
str_a = "abcdef1"
print(str_a, type(str_a))
# 将1改为g
# str_a[6] = "g" 错误 不可以通过下标改变str的数值
# print(str_a)
# 下标从0开始 到len-1
print(str_a[0], "=", str_a[1], "=", str_a[2])
print(len(str_a))
None_value = None
print(None_value, type(None_value))

# 列表 list
nums_list = list()
print(nums_list, type(nums_list))
# 有序
nums1 = [1, 2, 3]
print(nums1[1], nums1[2], nums1[0])
# 可变
nums2 = [1, True, "abc"]
print(nums2)
# 可重复
nums3 = [1, 1, 2, 2, 3]
print(nums3)

# 元组 tuple
data = tuple()
print(data, type(tuple))
# 有序 可以通过下标访问
data1 = (1, 2, 3)
print(data1, data1[2], data1[0], data1[1])
# 不可变 元素值不可改变
# data2 = (1, 2, 3)
# data2[2] = 100
# print(data2)
# 可重复 元素可以存在相同的值
data3 = (1, 1, 1, 3, 3, 3, 2, 2, 2)
print(data3)


# 字典 dict key-value的组合
some1 = dict()
print(some1, type(some1))
# 添加数值
# some1["key"]=Value
# dict={key1:value1,key2:value2,key3:value3}
some2 = {"name": "jom", "age": 18}
print(some2)
# 通过key访问字典中的某个元素
print(some2["age"])

# 集合 set()
some = set()
print(some, type(some))
# 无序
some = {1, 2, 3, 4}
print(some)
# 可变
some.add(5)
print(some)
# 无重复 自动进行去重处理
news = {1, 1, 1, 2, 2, 2, 3, 3, 3}
print(news)


if __name__ == "__main__":
    pass
