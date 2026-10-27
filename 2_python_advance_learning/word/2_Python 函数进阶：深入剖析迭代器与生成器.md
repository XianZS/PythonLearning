# 2_Python 函数进阶：深入剖析迭代器、生成器、闭包、装饰器

## 模块1：迭代器（Iterator）—— 可迭代对象的“遍历工具”

迭代器是Python中实现「遍历」功能的底层核心，生成器、列表、字符串等可遍历对象都依赖迭代器的逻辑，先掌握迭代器，才能更好理解后续的生成器。

### 1.1 先分清两个概念：可迭代对象 vs 迭代器

很多新手会混淆这两个概念，我们先明确区分，这是理解迭代器的关键。

#### （1）可迭代对象（`Iterable`）

- **定义**：只要对象实现了 `__iter__()` ii方法，或者是「序列类型」（列表、元组、字符串）、「集合类型」（`set`、`dict`）、「文件对象」，都称为「可迭代对象」。

- **通俗理解**：可以用 `for` 循环遍历的对象，就是可迭代对象（如 `[1,2,3]`、`"hello"`、`{1:2}`）。

- **判断方法**：使用 `collections.abc.Iterable` （`Python3.3`+）进行类型判断。

#### （2）迭代器（Iterator）

- **定义**：同时实现了 `__iter__()` 方法和 `__next__()` 方法的对象，称为「迭代器」。

- **通俗理解**：一个「可以逐个取出元素的工具」，它持有一个「指针」，指向可迭代对象的当前元素，调用 `next()` 方法会让指针后移，返回下一个元素，直到没有元素时抛出 `StopIteration` 异常。

- **判断方法**：使用 `collections.abc.Iterator` （`Python3.3`+）进行类型判断。

- **核心特性**：

    1. 惰性求值：只有调用 `next()` 时，才会返回下一个元素，不会提前加载所有元素到内存。

    2. 一次性遍历：遍历到末尾后，无法回溯，只能重新创建迭代器。

    3. 节省内存：无需一次性存储所有元素，适合处理大数据集。

#### （3）两者的关系

1. 所有迭代器 **都是** 可迭代对象（因为实现了 `__iter__()` 方法）。
2. 并非所有可迭代对象 **都** 是迭代器（如列表 `[1,2,3]` 是可迭代对象，但不是迭代器）。
3. 可通过 `iter()` 函数，将「可迭代对象」转换为「迭代器」。

#### 示例：区分可迭代对象和迭代器

```Python
# 导入判断所需的类
from collections.abc import Iterable, Iterator

# 1. 定义常见对象
my_list = [1, 2, 3]  # 列表（可迭代对象，非迭代器）
my_str = "hello"     # 字符串（可迭代对象，非迭代器）
my_iter = iter(my_list)  # 用 iter() 转换为迭代器

# 2. 判断是否为可迭代对象
print("my_list 是否是 Iterable：", isinstance(my_list, Iterable))  # True
print("my_str 是否是 Iterable：", isinstance(my_str, Iterable))    # True
print("my_iter 是否是 Iterable：", isinstance(my_iter, Iterable))  # True

# 3. 判断是否为迭代器
print("my_list 是否是 Iterator：", isinstance(my_list, Iterator))  # False
print("my_str 是否是 Iterator：", isinstance(my_str, Iterator))    # False
print("my_iter 是否是 Iterator：", isinstance(my_iter, Iterator))  # True
```

### 1.2 迭代器的核心方法

迭代器的行为由两个魔法方法（内置方法）控制，手动实现这两个方法，就能自定义迭代器。

#### （1）核心方法说明

|方法|作用|调用方式|
|---|---|---|
|`__iter__()`|返回迭代器对象本身（用于让迭代器支持 `for` 循环）|直接调用 `obj.__iter__()` 或 `iter(obj)`|
|`__next__()`|返回可迭代对象的下一个元素，无元素时抛出 `StopIteration` 异常|直接调用 `obj.__next__()` 或 `next(obj)`|
#### （2）手动实现一个迭代器

我们实现一个「遍历1到n的整数迭代器」，理解迭代器的底层逻辑：

```Python

from collections.abc import Iterator

# 自定义迭代器类（实现 __iter__() 和 __next__() 方法）
class MyRangeIterator:
    def __init__(self, n):
        self.n = n  # 遍历上限
        self.current = 1  # 指针，初始指向1

    # 方法1：返回迭代器对象本身
    def __iter__(self):
        return self

    # 方法2：返回下一个元素，抛出终止异常
    def __next__(self):
        if self.current <= self.n:
            result = self.current
            self.current += 1  # 指针后移
            return result
        else:
            # 无元素时，抛出 StopIteration 异常，终止遍历
            raise StopIteration

# 1. 创建迭代器对象
my_iter = MyRangeIterator(5)

# 2. 方式1：用 next() 函数逐个取出元素
print("用 next() 遍历：")
print(next(my_iter))  # 1
print(next(my_iter))  # 2
print(next(my_iter))  # 3

# 3. 方式2：用 for 循环遍历（自动捕获 StopIteration 异常，终止循环）
print("\n用 for 循环遍历：")
for num in MyRangeIterator(5):
    print(num, end=" ")next
```

运行结果：

```Plain Text

用 next() 遍历：
1
2
3

用 for 循环遍历：
1 2 3 4 5 
```

### 1.3 迭代器的优势与适用场景

#### （1）核心优势

- **节省内存**：无需一次性加载所有数据到内存，仅在需要时生成下一个元素（适合处理GB级别的大数据文件、无限序列）。

- **通用遍历逻辑**：统一了所有可迭代对象的遍历方式（无论是列表、字符串还是自定义对象，都可以用相同的 `next()` 或 `for` 循环遍历）。

#### （2）适用场景

- 处理超大文件（如逐行读取`10GB`的日志文件）。

- 生成无限序列（如无限生成奇数、斐波那契数列）。

- 避免一次性加载大量数据导致的内存溢出。 

#### （3）注意事项

- 迭代器是「一次性」的，遍历到末尾后，无法重新遍历，只能重新创建迭代器对象。

- 无法通过索引访问迭代器中的元素，只能按顺序逐个取出。

## 模块2：生成器（Generator）—— 简化版迭代器（yield 关键字核心）

生成器是Python中**创建迭代器的简洁方式**，无需手动实现 `__iter__()` 和 `__next__()` 方法，也无需手动抛出 `StopIteration` 异常，只需使用 `yield` 关键字，就能创建一个迭代器（生成器是特殊的迭代器）。

### 2.1 生成器的定义与核心特性

- **定义**：生成器是一种「惰性求值」的迭代器，分为「生成器表达式」和「生成器函数」两种，核心是 `yield` 关键字（仅用于生成器函数）。

- **核心特性**：

    1. 生成器自动实现 `__iter__()` 和 `__next__()` 方法，可直接用 `next()` 或 `for` 循环遍历。

    2. 生成器函数执行到 `yield` 时，会「暂停执行」，返回 `yield` 后的值，下次调用 `next()` 时，从暂停处继续执行，直到函数结束（自动抛出 `StopIteration`）。

    3. 与迭代器一样，节省内存，一次性遍历，无法回溯。

### 2.2 两种创建生成器的方式

#### （1）方式1：生成器表达式（简单场景）

生成器表达式是「列表推导式」的简化版，只需将列表推导式的 `[]` 改为 `()`，即可创建生成器，适合简单的生成逻辑。

##### 语法与示例

```Python

# 1. 列表推导式（一次性生成所有元素，占用内存）
list_comp = [x * 2 for x in range(5)]
print("列表推导式结果：", list_comp)  # [0, 2, 4, 6, 8]
print("是否是迭代器：", isinstance(list_comp, Iterator))  # False

# 2. 生成器表达式（惰性求值，不立即生成所有元素，占用内存极少）
gen_exp = (x * 2 for x in range(5))
print("生成器表达式结果：", gen_exp)  # <generator object <genexpr> at 0x...>
print("是否是迭代器：", isinstance(gen_exp, Iterator))  # True

# 3. 遍历生成器表达式
print("\n遍历生成器表达式：")
for num in gen_exp:
    print(num, end=" ")

# 4. 一次性遍历后，无法重新遍历（生成器已耗尽）
print("\n\n遍历耗尽后的生成器：")
for num in gen_exp:
    print(num, end=" ")  # 无输出
```

运行结果：

```Plain Text

列表推导式结果： [0, 2, 4, 6, 8]
是否是迭代器： False
生成器表达式结果： <generator object <genexpr> at 0x7f8b1c0b7eb0>
是否是迭代器： True

遍历生成器表达式：
0 2 4 6 8 

遍历耗尽后的生成器：
```

#### （2）方式2：生成器函数（复杂场景，核心）

当生成逻辑较复杂时，使用生成器函数，函数中包含 `yield` 关键字（而非 `return`），调用该函数不会立即执行函数体，而是返回一个生成器对象。

##### 核心区别：`yield` vs `return`

|关键字|作用|执行逻辑|
|---|---|---|
|`return`|返回值，终止函数执行|执行到 `return` 时，返回值并终止函数，下次调用重新执行函数体|
|`yield`|返回值，暂停函数执行|执行到 `yield` 时，返回值并暂停函数，下次调用从暂停处继续执行|
##### 示例1：简单生成器函数（遍历1到n的整数）

```Python

from collections.abc import Iterator

# 生成器函数（包含 yield 关键字）
def my_range_gen(n):
    current = 1
    while current <= n:
        # 暂停执行，返回 current 的值，下次调用从这里继续
        yield current
        current += 1

# 1. 调用生成器函数，返回生成器对象（不立即执行函数体）
gen = my_range_gen(5)
print("生成器对象：", gen)
print("是否是迭代器：", isinstance(gen, Iterator))  # True

# 2. 用 for 循环遍历生成器
print("\n遍历生成器：")
for num in gen:
    print(num, end=" ")

# 3. 重新创建生成器，用 next() 逐个取出元素
print("\n\n用 next() 遍历生成器：")
gen2 = my_range_gen(3)
print(next(gen2))  # 1
print(next(gen2))  # 2
print(next(gen2))  # 3
# print(next(gen2))  # 无元素，抛出 StopIteration 异常
```

运行结果：

```Plain Text

生成器对象： <generator object my_range_gen at 0x7f8b1c0b7f50>
是否是迭代器： True

遍历生成器：
1 2 3 4 5 

用 next() 遍历生成器：
1
2
3
```

##### 示例2：进阶生成器函数（斐波那契数列，无限序列）

生成器可以轻松实现无限序列（无需担心内存溢出，因为是惰性求值）：

```Python

# 生成器函数：无限生成斐波那契数列
def fib_gen():
    a, b = 0, 1
    while True:
        yield b  # 暂停执行，返回当前斐波那契数
        a, b = b, a + b

# 1. 创建生成器对象
fib = fib_gen()

# 2. 取出前10个斐波那契数（无限序列，需手动终止遍历）
print("前10个斐波那契数：")
for _ in range(10):
    print(next(fib), end=" ")
```

运行结果：

```Plain Text

前10个斐波那契数：
1 1 2 3 5 8 13 21 34 55 
```

##### 示例3：生成器的 `send()` 方法（向生成器传值）

`send()` 方法不仅可以获取生成器的下一个值，还能向生成器的暂停处传递一个值，进一步增强生成器的交互性。

- 语法：`gen.send(value)`，`value` 是传递给生成器暂停处的值。

- 注意：第一次调用生成器时，若使用 `send()`，只能传递 `None`（因为生成器尚未暂停在 `yield` 处）。

```Python

# 生成器函数：接收外部传入的值，进行累加
def accumulator_gen():
    total = 0
    while True:
        # 接收外部传入的值，赋值给 num，同时返回 total
        num = yield total
        if num is None:
            break
        total += num

# 1. 创建生成器对象
acc_gen = accumulator_gen()

# 2. 第一次调用：send(None) 或 next()，让生成器执行到第一个 yield 处
print(next(acc_gen))  # 0（初始 total=0）

# 3. 用 send() 向生成器传值，并获取返回结果
print(acc_gen.send(10))  # 10（total=0+10）
print(acc_gen.send(20))  # 30（total=10+20）
print(acc_gen.send(30))  # 60（total=30+30）

# 4. 传递 None，终止生成器
acc_gen.send(None)
```

运行结果：

```Plain Text

0
10
30
60
```

### 2.3 生成器的优势与适用场景

#### （1）核心优势

- **极简代码**：无需手动实现迭代器的两个魔法方法，大幅简化迭代器的创建逻辑。

- **节省内存**：惰性求值，仅在需要时生成元素，适合处理大数据集。

- **支持交互**：通过 `send()` 方法实现与生成器的双向通信，增强灵活性。

#### （2）适用场景

- 处理超大文件（如逐行读取日志文件、`CSV`文件）。

- 生成无限序列（如斐波那契数列、随机数序列）。

- 分步执行复杂任务（如数据清洗、分批处理数据库数据）。

- 替代列表推导式，避免大数据集导致的内存溢出。

## 模块3：闭包（Closure）—— 保存状态的嵌套函数

闭包是Python中实现「数据封装」和「状态保存」的重要方式，也是装饰器的底层基础，理解闭包是掌握装饰器的关键。

### 3.1 闭包的定义与核心条件

#### （1）通俗定义

​	闭包是指：“嵌套函数中，内部函数引用了外部函数的变量，且外部函数返回了内部函数，此时内部函数及其引用的外部变量共同构成一个「闭包」”。

​	简单理解：闭包就像一个「带记忆的函数」，它可以记住外部函数的变量状态，即使外部函数已经执行完毕，内部函数依然可以访问和使用这些变量。

#### （2）核心条件（3个缺一不可）

1. 存在**嵌套函数**（一个函数定义在另一个函数内部）。

2. 内部函数**引用了外部函数的变量**（非全局变量）。

3. 外部函数**返回了内部函数**（返回的是函数对象，而非函数执行结果）。

#### （3）示例：实现一个简单闭包

```Python

# 外部函数：接收一个初始值 base
def outer_func(base):
    # 定义内部函数（嵌套函数）
    def inner_func(num):
        # 内部函数引用了外部函数的变量 base（核心条件2）
        return base + num
    
    # 外部函数返回内部函数对象（核心条件3，不执行内部函数）
    return inner_func

# 1. 调用外部函数，返回内部函数对象，赋值给 add5
add5 = outer_func(5)
# 2. 调用内部函数，此时 outer_func 已执行完毕，但 inner_func 仍能访问 base=5
print("5 + 10 =", add5(10))  # 15
print("5 + 20 =", add5(20))  # 25

# 3. 重新调用外部函数，创建新的闭包（base=10）
add10 = outer_func(10)
print("10 + 30 =", add10(30))  # 40
```

运行结果：

```Plain Text

5 + 10 = 15
5 + 20 = 25
10 + 30 = 40
```

#### （4）闭包的核心特性：保存外部变量状态

在上面的示例中，当 `outer_func(5)` 执行完毕后，它的局部变量 `base=5` 并没有被销毁，而是被闭包（`inner_func`）保存下来，后续调用 `add5()` 时，依然可以访问这个 `base=5`。

我们可以通过 `__closure__` 属性查看闭包保存的变量：

```Python
# 查看闭包保存的变量
print("add5 的闭包变量：", add5.__closure__)
print("闭包变量的值：", add5.__closure__[0].cell_contents)  # 5
```

运行结果：

```Plain Text

add5 的闭包变量： (<cell at 0x7f8b1c0a7a90: int object at 0x7f8b1c1e2160>,)
闭包变量的值： 5
```

### 3.2 进阶：带参数的闭包

闭包可以支持多层参数传递，既可以在外部函数传递参数，也可以在内部函数传递参数，甚至可以在更外层嵌套函数传递参数，满足复杂场景的需求。

示例：实现一个“自定义乘法系数”的闭包

```Python

# 外层函数：接收乘法系数 factor1
def outer_func(factor1):
    # 中层函数：接收乘法系数 factor2
    def middle_func(factor2):
        # 内层函数：接收待乘数字 num
        def inner_func(num):
            # 引用外层和中层函数的变量
            return num * factor1 * factor2
        # 中层函数返回内层函数
        return inner_func
    # 外层函数返回中层函数
    return middle_func

# 1. 逐层调用，创建闭包（factor1=2，factor2=3）
mul_2_3 = outer_func(2)(3)

# 2. 调用内层函数，执行乘法运算
print("10 * 2 * 3 =", mul_2_3(10))  # 60
print("20 * 2 * 3 =", mul_2_3(20))  # 120

# 3. 重新创建闭包（factor1=5，factor2=4）
mul_5_4 = outer_func(5)(4)
print("10 * 5 * 4 =", mul_5_4(10))  # 200
```

运行结果：

```Plain Text
10 * 2 * 3 = 60
20 * 2 * 3 = 120
10 * 5 * 4 = 200
```

### 3.3 闭包的优势与适用场景

#### （1）核心优势

- **保存状态**：闭包可以保存外部函数的变量状态，避免使用全局变量，减少变量污染。

- **代码复用**：将通用逻辑封装在外部函数，将具体逻辑封装在内部函数，提高代码复用性。

- **数据封装**：外部函数的变量只能被内部函数访问，无法被外部直接修改，实现数据的私有性。

#### （2）适用场景

- 实现带记忆功能的函数（如缓存函数执行结果、累计计数）。

- 构建装饰器（这是闭包最核心、最广泛的应用场景）。

- 封装复杂逻辑，简化外部调用（如自定义工具函数）。

#### （3）注意事项

- **变量延迟绑定**：闭包中的变量是「延迟绑定」的，即只有在内部函数执行时，才会查找变量的当前值，而非闭包创建时的值。

    - 示例：变量延迟绑定问题

        ```Python
        
        def create_functions():
            funcs = []
            for i in range(3):
                def inner():
                    print(i)
                funcs.append(inner)
            return funcs
        
        # 预期输出：0、1、2，实际输出：2、2、2（延迟绑定，i最终为2）
        funcs = create_functions()
        for f in funcs:
            f()
        ```

    - 解决方法：通过默认参数提前绑定变量

        ```Python
        
        def create_functions():
            funcs = []
            for i in range(3):
                def inner(i=i):  # 默认参数提前绑定 i 的当前值
                    print(i)
                funcs.append(inner)
            return funcs
        
        funcs = create_functions()
        for f in funcs:
            f()  # 输出：0、1、2
        ```

## 模块4：装饰器（Decorator）—— 增强函数功能的“神器”

装饰器是Python中**基于闭包实现的高级功能**，它可以在「不修改原函数代码、不改变原函数调用方式」的前提下，为原函数添加额外的功能（如日志记录、性能统计、权限校验等），符合「开放-封闭原则」（对扩展开放，对修改封闭）。

### 4.1 装饰器的核心思想

- 「包装」：用一个装饰器函数（闭包）包装原函数，在原函数执行前后添加额外逻辑。

- 「透明」：原函数的调用方式不变，使用者无需感知装饰器的存在。

- 「复用」：装饰器可以被多个函数复用，提高代码复用性。

### 4.2 基础装饰器（无参数装饰器）

基础装饰器是最常用的装饰器，它接收「被装饰函数」作为参数，返回一个包装函数（闭包），包装函数中实现额外功能，并调用原函数。

#### （1）实现步骤（3步）

1. 定义装饰器函数（接收被装饰函数 `func` 作为参数）。

2. 定义包装函数（`wrapper`，实现额外功能，调用原函数 `func()`）。

3. 装饰器函数返回包装函数 `wrapper`。

4. （可选）使用语法糖 `@装饰器名`，简化装饰器的调用。

#### （2）示例1：实现一个“日志记录”装饰器

```Python

# 步骤1：定义装饰器函数（接收被装饰函数 func 作为参数）
def log_decorator(func):
    # 步骤2：定义包装函数（wrapper，实现日志记录功能）
    def wrapper(*args, **kwargs):
        # 额外功能：调用原函数前，打印日志
        print(f"[日志] 函数 {func.__name__} 开始执行...")
        
        # 调用原函数，获取返回值（支持接收任意参数）
        result = func(*args, **kwargs)
        
        # 额外功能：调用原函数后，打印日志
        print(f"[日志] 函数 {func.__name__} 执行完毕...")
        
        # 返回原函数的返回值
        return result
    
    # 步骤3：返回包装函数 wrapper
    return wrapper

# 步骤4：使用语法糖 @log_decorator，装饰原函数（等价于：add = log_decorator(add)）
@log_decorator
def add(a, b):
    """两数相加"""
    return a + b

# 步骤5：调用原函数（调用方式不变）
result = add(10, 20)
print("计算结果：", result)
```

运行结果：

```Plain Text

[日志] 函数 add 开始执行...
[日志] 函数 add 执行完毕...
计算结果： 30
```

#### （3）示例2：实现一个“性能统计”装饰器

统计函数的运行时间，这是开发中高频使用的装饰器：

```Python

import time

# 定义性能统计装饰器
def time_decorator(func):
    def wrapper(*args, **kwargs):
        # 记录开始时间
        start_time = time.time()
        
        # 调用原函数
        result = func(*args, **kwargs)
        
        # 记录结束时间，计算运行时间
        end_time = time.time()
        run_time = end_time - start_time
        
        # 打印性能统计信息
        print(f"[性能] 函数 {func.__name__} 运行时间：{run_time:.6f} 秒")
        
        # 返回原函数返回值
        return result
    
    return wrapper

# 装饰原函数
@time_decorator
def calculate_sum(n):
    """计算 1 到 n 的和"""
    total = 0
    for i in range(1, n+1):
        total += i
    return total

# 调用原函数
result = calculate_sum(100000)
print("1到100000的和：", result)
```

运行结果：

```Plain Text

[性能] 函数 calculate_sum 运行时间：0.004987 秒
1到100000的和： 5000050000
```

#### （4）关键优化：保留原函数元信息

使用装饰器后，原函数的元信息（如 `__name__`、`__doc__`）会被包装函数 `wrapper` 覆盖，这会影响后续的调试和文档查看，解决方法是使用 `functools.wraps` 装饰器，保留原函数的元信息。

示例：优化装饰器，保留原函数元信息

```Python

import time
from functools import wraps  # 导入 wraps 装饰器

def time_decorator(func):
    # 使用 wraps 装饰 wrapper，保留原函数元信息
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"[性能] 函数 {func.__name__} 运行时间：{run_time:.6f} 秒")
        return result
    
    return wrapper

@time_decorator
def calculate_sum(n):
    """计算 1 到 n 的和"""
    total = 0
    for i in range(1, n+1):
        total += i
    return total

# 查看原函数元信息（未优化前，__name__ 为 wrapper，__doc__ 为 None）
print("函数名：", calculate_sum.__name__)  # calculate_sum
print("函数文档：", calculate_sum.__doc__)  # 计算 1 到 n 的和
```

运行结果：

```Plain Text

函数名： calculate_sum
函数文档： 计算 1 到 n 的和
```

### 4.3 进阶：带参数的装饰器

当我们需要给装饰器本身传递参数时（如指定日志级别、超时时间），就需要使用「带参数的装饰器」，它是「三层嵌套函数」实现的（比基础装饰器多一层，用于接收装饰器参数）。

#### （1）实现步骤（4步）

1. 定义外层函数（接收装饰器参数）。

2. 定义中层函数（接收被装饰函数 `func` 作为参数）。

3. 定义内层函数（`wrapper`，实现额外功能，调用原函数 `func()`）。

4. 外层函数返回中层函数，中层函数返回内层函数 `wrapper`。

#### （2）示例：实现一个“带日志级别”的装饰器

```Python

from functools import wraps

# 步骤1：定义外层函数（接收装饰器参数：log_level）
def log_level_decorator(log_level):
    # 步骤2：定义中层函数（接收被装饰函数 func）
    def decorator(func):
        # 步骤3：定义内层函数（wrapper，实现带级别日志记录）
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 额外功能：根据装饰器参数，打印不同级别的日志
            print(f"[{log_level}] 函数 {func.__name__} 开始执行...")
            
            # 调用原函数
            result = func(*args, **kwargs)
            
            # 额外功能：打印结束日志
            print(f"[{log_level}] 函数 {func.__name__} 执行完毕...")
            
            # 返回原函数返回值
            return result
        
        # 步骤4：中层函数返回内层函数 wrapper
        return wrapper
    
    # 步骤4：外层函数返回中层函数 decorator
    return decorator

# 步骤5：使用语法糖 @装饰器名(参数)，装饰原函数
@log_level_decorator("INFO")  # 装饰器参数：日志级别 INFO
def add(a, b):
    """两数相加"""
    return a + b

@log_level_decorator("ERROR")  # 装饰器参数：日志级别 ERROR
def subtract(a, b):
    """两数相减"""
    return a - b

# 步骤6：调用原函数
print("加法结果：", add(10, 20))
print("减法结果：", subtract(20, 10))
```

运行结果：

```Plain Text

[INFO] 函数 add 开始执行...
[INFO] 函数 add 执行完毕...
加法结果： 30
[ERROR] 函数 subtract 开始执行...
[ERROR] 函数 subtract 执行完毕...
减法结果： 10
```

#### （3）示例2：实现一个“带超时时间”的装饰器

```Python

import time
from functools import wraps

# 带参数的装饰器：指定超时时间，若函数运行超时，抛出异常
def timeout_decorator(timeout):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            run_time = end_time - start_time
            
            # 判断是否超时
            if run_time > timeout:
                raise TimeoutError(f"函数 {func.__name__} 运行超时（超时时间：{timeout} 秒，实际运行时间：{run_time:.6f} 秒）")
            
            print(f"函数 {func.__name__} 运行正常，耗时：{run_time:.6f} 秒")
            return result
        
        return wrapper
    
    return decorator

# 装饰原函数，指定超时时间 0.005 秒
@timeout_decorator(0.005)
def calculate_sum(n):
    total = 0
    for i in range(1, n+1):
        total += i
    return total

# 调用原函数
try:
    result = calculate_sum(100000)
    print("1到100000的和：", result)
except TimeoutError as e:
    print(e)
```

运行结果：

```Plain Text

函数 calculate_sum 运行正常，耗时：0.004992 秒
1到100000的和： 5000050000
```

### 4.4 拓展：多个装饰器叠加使用

一个函数可以被多个装饰器同时装饰，装饰器的执行顺序是「**从上到下装饰，从下到上执行**」（即“就近原则”，离原函数越近的装饰器，越先执行）。

示例：多个装饰器叠加

```Python

from functools import wraps

# 装饰器1：日志记录
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("=== 装饰器1：开始日志记录 ===")
        result = func(*args, **kwargs)
        print("=== 装饰器1：结束日志记录 ===")
        return result
    return wrapper

# 装饰器2：性能统计
def time_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("=== 装饰器2：开始性能统计 ===")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"=== 装饰器2：函数运行时间 {end_time - start_time:.6f} 秒 ===")
        return result
    return wrapper

# 多个装饰器叠加（从上到下装饰：log_decorator → time_decorator）
@log_decorator
@time_decorator
def add(a, b):
    return a + b

# 调用原函数（执行顺序：time_decorator → log_decorator，从下到上）
result = add(10, 20)
print("计算结果：", result)
```

运行结果：

```Plain Text

=== 装饰器1：开始日志记录 ===
=== 装饰器2：开始性能统计 ===
=== 装饰器2：函数运行时间 0.000000 秒 ===
=== 装饰器1：结束日志记录 ===
计算结果： 30
```

### 4.5 装饰器的适用场景

装饰器在实际开发中应用广泛，常见场景包括：

1. **日志记录**：记录函数的调用时间、参数、返回值等。

2. **性能统计**：统计函数的运行时间、调用次数等。

3. **权限校验**：验证用户是否有权限执行某个函数（如接口权限校验）。

4. **缓存处理**：缓存函数的执行结果，避免重复计算（如斐波那契数列缓存）。

5. **参数校验**：校验函数传入参数的合法性、类型等。

6. **异常捕获**：自动捕获函数执行过程中的异常，进行统一处理。

## 总结

1. **迭代器**：实现 `__iter__()` 和 `__next__()` 方法的对象，惰性求值、节省内存，是遍历的底层核心，可通过 `iter()` 转换可迭代对象得到。

2. **生成器**：特殊的迭代器，无需手动实现魔法方法，分为生成器表达式（简单场景）和生成器函数（复杂场景，核心是 `yield` 关键字，支持暂停和传值）。

3. **闭包**：满足「嵌套函数、引用外部变量、返回内部函数」三个条件，核心作用是保存变量状态、实现数据封装，是装饰器的底层基础。

4. **装饰器**：基于闭包实现，分为基础装饰器（无参数，三层嵌套）和带参数装饰器（四层嵌套），可在不修改原函数的前提下增强功能，支持多个装饰器叠加。