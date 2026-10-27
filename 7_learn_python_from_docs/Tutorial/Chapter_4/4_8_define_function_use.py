# def 函数名(参数):
#   函数体


def fib(n):
    """
    function details: 实现斐波拉契数列
    return: number(int)
    """
    nums = [0 for _ in range(n)]
    if n == 1:
        return 0
    if n == 2:
        return 1
    nums[0], nums[1] = 0, 1
    for index in range(2, n):
        nums[index] = nums[index - 1] + nums[index - 2]
    return nums[n - 1]


for index in range(1, 11):
    print(fib(index))


def func():
    pass


print(func())

# help(fib)
