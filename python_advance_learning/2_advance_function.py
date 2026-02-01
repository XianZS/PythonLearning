"""
1.迭代器
"""

# 创建可迭代对象 iterable
nums = [1, 2, 3]
print(nums, type(nums))
# 创建迭代器 iterator
res = iter(nums)
print(res, type(res))

# iterator特性1:通过next求值
print(res.__next__())  # next(res)
# iterator特性2:指针的不可逆性，每次指针会向后移动一位
print(res.__next__())
print(next(res))
# iterator特性3:只可以进行一次访问，当访问越界时，会触发StopIteration错误
# print(res.__next__())


# 需要自定义实现一个iterator对象 迭代器
# 需要实现 __iter__ __next__ 这两个方法
class MyIterator:
    def __init__(self, nums):
        self.nums = nums
        self.current = 1
        self.length = len(nums)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.length:
            res = self.nums[self.current - 1]
            self.current += 1
            return res
        else:
            raise StopIteration


my_iter_obj = MyIterator(
    [3, 123, 123, 4132, 12, 21, 12, 21321123, 1235, 342, 4, 2, 11, 12, 2312]
)
# <class list>:可迭代对象 iterable
# <class list_iterator>:迭代器 iterator
print(my_iter_obj, type(my_iter_obj))
print(next(my_iter_obj))
print("===" * 30)

"""
2.生成器
"""
# 列表推导式
nums = [x for x in range(1, 11)]
print(nums, type(nums))
# 生成器推导式
res = (x for x in range(1, 11))
print(res, type(res))


# 生成器函数 yield
# 对数据进行累加求数值，在上次累加的基础上，进行求数值累加和
def my_gen(number):
    res = 0
    for num in number:
        res += num
        print(f"第一次求和的结果为:{res}")
        yield res


gen_obj = my_gen([1, 2, 3, 4, 5, 6, 7, 8, 9])
next(gen_obj)
next(gen_obj)
next(gen_obj)

# 在创建时指明累加求和对象
# 现在的需求：动态的累加求和
# send() 可以向生成器发送数据
# obj.send(number)
# 发送数值 = yield 返回值


def my_gen_send():
    res = 0
    index = 1
    while True:
        send_number = yield res
        if send_number is None:
            break
        else:
            res += send_number
            print(f"第{index}次累加求和的结果为:{res}")
            index += 1


my_gen_send_obj = my_gen_send()
# 此时需要先让生成器的指针指向接收值处
next(my_gen_send_obj)
try:
    my_gen_send_obj.send(123)
    my_gen_send_obj.send(3123)
    my_gen_send_obj.send(1)
    my_gen_send_obj.send(None)
except StopIteration:
    print("动态累加求和结束")

"""
3.闭包
"""

"""
4.装饰器
"""
