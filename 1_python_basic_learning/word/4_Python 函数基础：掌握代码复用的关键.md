# 4_Python 函数基础：掌握代码复用的关键

你想要全面且详细地了解Python函数的基础知识点，包括函数的定义、调用、参数、返回值等核心内容，以便掌握代码复用的核心方式，能独立定义和使用自定义函数。

函数是Python中**代码复用**的核心机制，把一段完成特定功能的代码封装成可调用的“代码块”，需要时直接调用即可。下面从“认知-定义-调用-参数-返回值-进阶基础”的逻辑，详细拆解函数基础的所有核心内容：

## 一、函数的基本认知

### 1. 什么是函数？

函数是具有特定功能、可重复使用的代码段，相当于一个“工具”。

- 内置函数：Python自带的现成工具（如`print()`、`len()`、`max()`）；

- 自定义函数：你根据需求编写的专属工具（如计算平均值、验证手机号）。

### 2. 为什么要用函数？

- 减少冗余：重复逻辑只需写一次，多次调用，避免复制粘贴代码；

- 提高可读性：函数名可直观体现功能（如`calculate_average`）；

- 便于维护：修改逻辑只需改函数内部，无需改所有调用处；

- 解耦：将复杂程序拆分成多个小函数，每个函数负责一个功能，降低复杂度。

## 二、函数的定义与调用（最基础）

### 1. 函数定义的语法

核心关键字是`def`，完整结构如下（缩进是Python区分代码块的核心，必须遵守）：

```Python

def 函数名(参数列表):
    """文档字符串（可选，说明函数功能）"""
    函数体（实现功能的代码）
    [return 返回值]  # 可选，无return则默认返回None
```

**关键规则**：

- `def`后必须跟函数名+括号+冒号`:`；

- 函数名命名规则：和变量一致（字母/数字/下划线，不以数字开头，建议小写+下划线分隔，如`get_user_info`）；

- 函数体必须缩进（通常4个空格）。

### 2. 函数调用的语法

定义函数后不会自动执行，需要“调用”才会执行：

```Python
函数名(参数值列表)
```

### 3. 基础示例（无参数、无返回值）

```Python

# 定义函数：打印欢迎语
def print_welcome():
    """打印欢迎语的函数（文档字符串）"""
    print("欢迎学习Python函数！")
    print("函数是代码复用的核心～")

# 调用函数（执行函数体代码）
print_welcome()
# 多次调用（重复使用）
print_welcome()
```

**执行结果**：

```Plain Text

欢迎学习Python函数！
函数是代码复用的核心～
欢迎学习Python函数！
函数是代码复用的核心～
```

## 三、函数的参数（核心重点）

参数是函数的“输入”，让函数能处理不同数据，分为**形参**（定义时括号里的参数）和**实参**（调用时传入的参数）。参数是函数基础的核心，以下是6类常用参数：

### 1. 位置参数（必选参数）

- **定义**：最基础的参数，调用时必须按“形参顺序”传入对应数量的实参，缺一不可。

- **示例**：

```Python

# 定义：计算两个数的和（a、b是形参）
def calculate_sum(a, b):
    return a + b

# 调用：按位置传值（1对应a，2对应b）
result = calculate_sum(1, 2)
print(result)  # 3

# 错误示例1：参数数量不匹配（少传1个）
# calculate_sum(1)  # 报错：TypeError: calculate_sum() missing 1 required positional argument: 'b'

# 错误示例2：顺序错误（结果不符合预期）
result_wrong = calculate_sum(2, 1)
print(result_wrong)  # 3（语法无错，但逻辑可能不符合预期）
```

- **应用场景**：参数数量固定、顺序明确的简单场景（如数值计算）。

### 2. 关键字参数

- **定义**：调用时通过“参数名=值”传值，无需严格按位置顺序，可读性更高。

- **示例**：

```Python

def calculate_sum(a, b):
    return a + b

# 关键字参数调用（顺序可换）
result = calculate_sum(b=2, a=1)
print(result)  # 3
```

- **应用场景**：参数较多时，避免记混位置（如`print_user_info(name="小明", age=18)`）。

### 3. 默认参数

- **定义**：定义函数时给参数指定默认值，调用时若不传该参数则用默认值，传值则覆盖。

- **关键规则**：默认参数必须放在**位置参数之后**（否则语法报错）。

- **示例**：

```Python

# 定义：计算a+b，b默认值为0
def calculate_sum(a, b=0):
    return a + b

# 调用1：只传a，b用默认值
result1 = calculate_sum(5)
print(result1)  # 5

# 调用2：传a和b，覆盖默认值
result2 = calculate_sum(5, 3)
print(result2)  # 8
```

- **应用场景**：参数值大多固定、少数需要调整（如分页查询的默认页码`page=1`）。

### 4. 可变位置参数（*args）

- **定义**：接收任意数量的位置参数，传入的参数会被打包成**元组**（args是约定俗成的名称）。

- **示例**：

```Python

# 定义：计算任意多个数的和
def calculate_total(*args):
    total = 0
    for num in args:
        total += num
    return total

# 调用1：传3个参数
result1 = calculate_total(1, 2, 3)
print(result1)  # 6

# 调用2：传0个参数（args为空元组）
result2 = calculate_total()
print(result2)  # 0
```

- **应用场景**：参数数量不确定（如求和、求平均值，支持任意个数的数值）。

### 5. 可变关键字参数（**kwargs）

- **定义**：接收任意数量的关键字参数，传入的参数会被打包成**字典**（kwargs是约定俗成的名称）。

- **示例**：

```Python

# 定义：打印任意用户信息
def print_user_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 调用：传任意关键字参数
print_user_info(name="小明", age=18, city="北京")
# 输出：
# name: 小明
# age: 18
# city: 北京
```

- **应用场景**：参数名称和数量都不确定（如处理用户信息、配置项）。

### 6. 参数解包

- **定义**：将列表/元组/字典拆分成函数的参数，避免手动拆分数据。

- **示例**：

```Python

def add(a, b):
    return a + b

# 列表解包（*）
nums = [1, 2]
result1 = add(*nums)  # 等价于add(1, 2)
print(result1)  # 3

# 字典解包（**）
num_dict = {"a": 3, "b": 4}
result2 = add(**num_dict)  # 等价于add(a=3, b=4)
print(result2)  # 7
```

## 四、函数的返回值（return）

返回值是函数的“输出”，即函数执行后返回给调用处的结果，核心规则如下：

### 1. 基本用法

- `return`后跟要返回的值，执行到`return`时函数立即终止（后续代码不执行）；

- 无`return`的函数，默认返回`None`。

- **示例**：

```Python

# 有返回值的函数
def multiply(a, b):
    return a * b  # 返回乘积，执行到这里函数结束

result = multiply(3, 4)
print(result)  # 12

# 无返回值的函数（默认返回None）
def print_hello():
    print("Hello")

res = print_hello()
print(res)  # None

# return终止函数执行
def test_return():
    print("第一步")
    return  # 直接终止
    print("第二步")  # 不会执行

test_return()  # 仅输出“第一步”
```

### 2. 多返回值

Python支持函数返回多个值，本质是将多个值打包成**元组**返回，接收时可直接解包成多个变量。

- **示例**：

```Python

# 返回最大值和最小值
def get_max_min(num_list):
    max_num = max(num_list)
    min_num = min(num_list)
    return max_num, min_num  # 等价于return (max_num, min_num)

# 接收多返回值
nums = [1, 5, 3, 9, 2]
max_val, min_val = get_max_min(nums)
print(f"最大值：{max_val}，最小值：{min_val}")  # 最大值：9，最小值：1
```

- **应用场景**：函数需要返回多个关联结果（如坐标的x/y值、成绩的最高分/最低分）。

## 五、函数的文档字符串（Docstring）

- **定义**：函数内部的第一个字符串（通常用三引号），用于说明函数的功能、参数、返回值，是“函数说明书”。

- **查看方式**：`help(函数名)` 或 `函数名.__doc__`。

- **示例**：

```Python

def calculate_sum(a, b=0):
    """
    计算两个数的和
    
    参数：
        a (int/float)：第一个数（必选）
        b (int/float)：第二个数（可选，默认值0）
    
    返回值：
        int/float：两个数的和
    """
    return a + b

# 查看文档字符串
help(calculate_sum)
```

- **应用场景**：团队协作、代码维护时，让他人（或自己）快速了解函数用法。

## 六、函数的作用域

作用域指变量的生效范围，分为**局部作用域**和**全局作用域**：

### 1. 局部变量

在函数内部定义的变量，仅在函数内部生效，外部无法访问：

```Python

def test_local():
    local_var = 10  # 局部变量
    print(local_var)  # 函数内可访问，输出10

test_local()
# print(local_var)  # 外部访问报错：NameError
```

### 2. 全局变量

在函数外部定义的变量，全局生效（函数内可读取，修改需加`global`关键字）：

```Python

global_var = 20  # 全局变量

# 读取全局变量
def test_read():
    print(global_var)  # 输出20

# 修改全局变量（需加global）
def test_modify():
    global global_var
    global_var = 30

test_modify()
print(global_var)  # 输出30
```

- **注意**：尽量避免修改全局变量，易导致代码混乱，建议通过参数/返回值传递数据。

## 七、匿名函数（lambda表达式）

- **定义**：无需定义函数名的极简函数，仅适用于单行简单逻辑。

- **语法**：`lambda 参数列表: 表达式`（表达式结果就是返回值，无需写return）。

- **示例**：

```Python

# 定义：计算两数之和
add = lambda a, b: a + b
print(add(3, 5))  # 8

# 常用场景：结合sorted排序
students = [("小明", 18), ("小红", 16), ("小刚", 20)]
# 按年龄排序（lambda指定按元组第二个元素排序）
students_sorted = sorted(students, key=lambda x: x[1])
print(students_sorted)  # [('小红', 16), ('小明', 18), ('小刚', 20)]
```

- **应用场景**：简单逻辑的临时函数（如排序的key、map/filter参数）。

## 八、综合实战示例（简易计算器）

```Python

def calculator(num1, num2, op="+"):
    """
    简易计算器，支持加减乘除
    
    参数：
        num1 (int/float)：第一个数
        num2 (int/float)：第二个数
        op (str)：运算符，默认+，可选：+、-、*、/
    
    返回值：
        int/float：计算结果；异常时返回提示字符串
    """
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 == 0:
            return "错误：除数不能为0"
        return num1 / num2
    else:
        return f"错误：不支持的运算符{op}"

# 调用测试
print(calculator(10, 5))        # 15（默认加法）
print(calculator(10, 5, "-"))   # 5（减法）
print(calculator(10, 0, "/"))   # 错误：除数不能为0
```

### 总结

1. 函数基础核心包括**定义调用**（def+缩进）、**参数体系**（位置/关键字/默认/可变参数）、**返回值**（return支持多返回值）三大模块；

2. 作用域区分局部变量（函数内生效）和全局变量（全局生效，修改需加global），匿名函数（lambda）适用于单行简单逻辑；

3. 函数的核心价值是**代码复用**和**逻辑解耦**，定义时建议写文档字符串，提高代码可读性和可维护性。