def add(a, b):
    return a + b


def fact(number):
    if number < 0:
        raise ValueError("n必须是非负整数")
    result = 1
    for i in range(2, number + 1):
        result *= i
    return result
