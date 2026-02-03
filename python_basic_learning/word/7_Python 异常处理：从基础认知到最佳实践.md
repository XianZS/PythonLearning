# 7_Python 异常处理：从基础认知到最佳实践

## 模块1：基础认知——什么是异常？

### 1.1 异常的定义

简单来说，**异常是程序运行过程中发生的意外错误（不是语法错误），会导致程序正常流程中断并退出**。

比如你想读取一个不存在的文件、用数字除以0、访问列表中不存在的索引，这些操作在代码语法上没有问题，但运行时会触发错误，这些错误就是「异常」。

### 1.2 异常与语法错误的区别

很多新手容易混淆两者，这里明确区分：

- **语法错误**：代码书写不符合Python语法规则（比如少写冒号、缩进错误、括号不匹配），程序**无法启动运行**。

示例：

```Python

# 语法错误：if 语句后少写冒号
if 1 > 0
    print("这是语法错误")
```

- **异常**：代码语法正确，程序可以启动运行，但运行到某一步时出现逻辑/资源错误，程序**被迫中断**。

示例：

```Python

# 语法正确，运行时触发异常（除以零）
a = 10
b = 0
print(a / b)
```

### 1.3 Python中常见的内置异常

Python内置了很多异常类，用于描述不同类型的运行错误，新手最常遇到的有这些：

|异常类|中文说明|常见触发场景|
|---|---|---|
|`ZeroDivisionError`|除以零异常|用数字除以0|
|`FileNotFoundError`|文件未找到异常|读取一个不存在的文件|
|`IndexError`|索引越界异常|访问列表/元组中不存在的索引|
|`KeyError`|键不存在异常|访问字典中不存在的键|
|`NameError`|变量未定义异常|使用一个未声明/未赋值的变量|
|`TypeError`|类型错误|对不同类型的数据执行不支持的操作（比如字符串加数字）|
|`ValueError`|值错误|数据类型正确，但值不符合要求（比如用`int("abc")`转换非数字字符串）|
示例：查看常见异常的触发效果

```Python
# 1. IndexError：列表索引越界
my_list = [1, 2, 3]
# print(my_list[10])  # 运行报错：IndexError: list index out of range

# 2. KeyError：字典键不存在
my_dict = {"name": "Python"}
# print(my_dict["age"])  # 运行报错：KeyError: 'age'

# 3. TypeError：类型错误
# print("hello" + 123)  # 运行报错：TypeError: can only concatenate str (not "int") to str
```

### 1.4 异常的默认处理行为

当程序触发异常且未做任何处理时，Python会执行「默认异常处理流程」：

1. 中断当前程序的正常运行流程。

2. 在控制台打印异常信息（包括异常类型、错误信息、出错位置）。

3. 程序终止，后续代码不再执行。

这也是为什么未处理异常时，程序会直接“崩溃”的原因。

## 模块2：核心基础——异常捕获与处理（`try...except`）

异常处理的核心目的是：**捕获程序运行时的异常，避免程序直接崩溃，同时可以自定义异常处理逻辑（比如提示用户、记录日志、修复错误）**。

Python中最基础的异常处理语法是 `try...except`，这是异常处理的核心。

### 2.1 基本语法结构

```Python

try:
    # 块1：尝试执行的代码（可能触发异常的代码）
    可能出错的代码段
except:
    # 块2：异常捕获与处理代码（当块1触发任何异常时，执行此处代码）
    异常发生时的处理逻辑（比如提示、日志等）
```

### 2.2 基本工作流程

1. 程序先执行 `try` 块中的代码。

2. 如果 `try` 块中代码**正常执行无异常**，则跳过 `except` 块，继续执行后续代码。

3. 如果 `try` 块中代码**触发异常**，则立即中断 `try` 块的剩余代码，跳转到 `except` 块执行处理逻辑。

4. `except` 块执行完毕后，程序继续执行后续代码（不会终止）。

### 2.3 基础示例（捕获所有异常）

```Python

# 示例：处理除以零异常
try:
    a = 10
    b = 0
    result = a / b  # 可能触发ZeroDivisionError的代码
    print(f"计算结果：{result}")  # 异常触发后，这行代码不会执行
except:
    # 异常发生时的处理逻辑
    print("出错了！无法完成除法运算（可能是除数为零）")

# 后续代码正常执行（程序不会崩溃）
print("程序继续运行...")
```

运行结果：

```Plain Text
出错了！无法完成除法运算（可能是除数为零）
程序继续运行...
```

### 2.4 捕获「指定类型」的异常（推荐）

上面的 `except` 不带任何参数，会捕获 `try` 块中的**所有类型**异常，这种写法不够精准（不利于排查具体问题），实际开发中更推荐「捕获指定类型的异常」。

#### 语法格式

```Python

try:
    可能出错的代码段
except 异常类型1:
    处理异常类型1的逻辑
except 异常类型2:
    处理异常类型2的逻辑
```

#### 示例（捕获指定异常）

```Python

try:
    a = 10
    b = 0
    result = a / b
    print(f"计算结果：{result}")
# 只捕获「除以零异常」，其他异常不会被捕获
except ZeroDivisionError:
    print("出错了！除数不能为零，请修改除数后重试")

print("程序继续运行...")
```

### 2.5 捕获「多个指定类型」的异常

如果 `try` 块可能触发多种不同的异常，可通过两种方式处理：

#### 方式1：多个 `except` 块（分别处理不同异常，推荐，逻辑清晰）

```Python

try:
    my_list = [1, 2, 3]
    # 可能触发两种异常：IndexError（索引越界）、ZeroDivisionError（除以零）
    print(my_list[10])  # 先触发IndexError
    result = 10 / 0
except IndexError:
    print("出错了！列表索引超出范围")
except ZeroDivisionError:
    print("出错了！除数不能为零")

print("程序继续运行...")
```

#### 方式2：一个 `except` 块+异常元组（统一处理多种异常）

```Python

try:
    my_list = [1, 2, 3]
    print(my_list[10])
    result = 10 / 0
# 用元组指定多个异常，触发任意一个都会执行此处理逻辑
except (IndexError, ZeroDivisionError) as e:
    print(f"出错了！错误信息：{e}")

print("程序继续运行...")
```

### 2.6 获取异常详情（`as e`）

在 `except` 后添加 `as e`，可以捕获异常的具体信息（错误描述、堆栈等），方便调试和日志记录。

```Python

try:
    int("abc")  # 触发ValueError：无法将字符串"abc"转换为整数
except ValueError as e:
    # e 是异常对象，打印e可以获取具体错误信息
    print(f"异常类型：{type(e)}")
    print(f"错误详情：{e}")
```

运行结果：

```Plain Text

异常类型：<class 'ValueError'>
错误详情：invalid literal for int() with base 10: 'abc'
```

## 模块3：扩展语法——`else` 和 `finally`

除了 `try...except`，Python还提供了 `else` 和 `finally` 两个扩展子句，用于丰富异常处理的逻辑，让代码更严谨。

### 3.1 `else` 子句：无异常时执行

`else` 子句可选，位于 `except` 之后，**只有当 ** **`try`** ** 块中无异常正常执行完毕时，才会执行 ** **`else`** ** 块中的代码**。

#### 语法格式

```Python

try:
    可能出错的代码段
except 异常类型 as e:
    异常处理逻辑
else:
    无异常时的执行逻辑（try块代码正常完成后执行）
```

#### 示例

```Python

try:
    a = 10
    b = 2
    result = a / b
except ZeroDivisionError as e:
    print(f"出错了：{e}")
else:
    # 只有try块无异常时，才会执行此处
    print(f"除法运算正常完成，结果：{result}")

print("程序继续运行...")
```

运行结果：

```Plain Text

除法运算正常完成，结果：5.0
程序继续运行...
```

### 3.2 `finally` 子句：无论是否有异常都必须执行

`finally` 子句可选，位于整个 `try...except...else` 结构的最后，**无论 ** **`try`** ** 块是否触发异常，** **`finally`** ** 块中的代码都会被执行**。

它的核心用途是：**释放资源**（比如关闭文件、关闭数据库连接、释放网络连接等），避免资源泄露。

#### 语法格式

```Python

try:
    可能出错的代码段
except 异常类型 as e:
    异常处理逻辑
else:
    无异常时的执行逻辑
finally:
    无论是否有异常，都必须执行的逻辑（释放资源等）
```

#### 示例1：基础用法（验证执行逻辑）

```Python

try:
    a = 10
    b = 0
    result = a / b
except ZeroDivisionError as e:
    print(f"出错了：{e}")
else:
    print(f"运算结果：{result}")
finally:
    print("------ 无论是否有异常，我都会执行 ------")

print("程序继续运行...")
```

运行结果：

```Plain Text

出错了：division by zero
------ 无论是否有异常，我都会执行 ------
程序继续运行...
```

#### 示例2：实际用途（释放文件资源）

之前我们学过 `with` 语句自动关闭文件，而 `finally` 是手动释放资源的经典场景（理解这个有助于明白 `with` 语句的底层逻辑）：

```Python

# 手动打开文件，用finally确保文件一定被关闭
f = None
try:
    f = open("test.txt", 'r', encoding='utf-8')
    content = f.read()
    print(f"文件内容：{content}")
except FileNotFoundError as e:
    print(f"出错了：{e}")
finally:
    # 无论是否读取成功，都关闭文件（释放资源）
    if f:  # 避免f为None时调用close()报错
        f.close()
        print("文件已关闭")
```

### 3.3 完整结构执行顺序总结

1. 执行 `try` 块代码。

2. 如果 `try` 块触发异常：

    - 跳转到对应 `except` 块处理异常。

    - 执行 `finally` 块代码。

    - 继续执行程序后续代码。

3. 如果 `try` 块无异常：

    - 跳转到 `else` 块执行代码。

    - 执行 `finally` 块代码。

    - 继续执行程序后续代码。

注意：`finally` 块的代码**即使在 ** **`try`** **/** **`except`** **/** **`else`** ** 中使用了 ** **`return`** **，也会被执行**（优先级极高）。

## 模块4：主动抛出异常——`raise` 语句

前面的异常都是程序运行时自动触发的，而Python也允许我们**主动抛出异常**，用于在满足特定业务逻辑时，中断程序并提示错误（比如用户输入的年龄为负数、密码长度不足等）。

### 4.1 基本语法

```Python

# 格式1：抛出指定类型的异常（无附加信息）
raise 异常类型

# 格式2：抛出指定类型的异常，并附加错误描述信息（推荐）
raise 异常类型("错误描述信息")
```

### 4.2 示例1：主动抛出内置异常

```Python

# 业务场景：校验用户输入的年龄
age = int(input("请输入你的年龄："))

try:
    if age < 0 or age > 150:
        # 主动抛出ValueError异常，提示年龄不合法
        raise ValueError("年龄必须在0到150之间，请输入合法年龄")
    else:
        print(f"你的年龄是：{age}，输入合法")
except ValueError as e:
    print(f"出错了：{e}")
```

测试输入：`-10`，运行结果：

```Plain Text

请输入你的年龄：-10
出错了：年龄必须在0到150之间，请输入合法年龄
```

### 4.3 示例2：自定义异常（进阶）

Python内置的异常类可能无法满足所有业务场景（比如“密码长度不足”“用户不存在”等），这时可以**自定义异常类**，需要满足两个要求：

1. 自定义异常类必须**继承自 ** **`Exception`** **类**（或其子类）。

2. 通常只需要定义类名，如需丰富功能，可重写 `__init__` 方法。

#### 步骤1：定义自定义异常类

```Python

# 自定义异常类：继承自Exception
class PasswordTooShortError(Exception):
    """自定义异常：密码长度不足"""
    # 可选：重写__init__方法，自定义异常信息
    def __init__(self, min_length, current_length):
        self.min_length = min_length
        self.current_length = current_length
        # 调用父类的__init__方法，设置异常描述
        super().__init__(f"密码长度不足！要求至少{min_length}位，当前仅{current_length}位")

class PasswordContainIllegalCharError(Exception):
    """自定义异常：密码包含非法字符"""
    pass
```

#### 步骤2：主动抛出自定义异常并捕获

```Python

# 业务场景：校验用户输入的密码
password = input("请输入你的密码（至少8位，仅允许字母和数字）：")

try:
    # 校验密码长度
    if len(password) < 8:
        raise PasswordTooShortError(8, len(password))
    # 校验密码字符（仅允许字母和数字）
    if not password.isalnum():
        raise PasswordContainIllegalCharError("密码仅允许包含字母和数字")
    else:
        print("密码校验通过，设置成功！")
except PasswordTooShortError as e:
    print(f"出错了：{e}")
except PasswordContainIllegalCharError as e:
    print(f"出错了：{e}")
```

测试输入：`123abc`（长度不足），运行结果：

```Plain Text

请输入你的密码（至少8位，仅允许字母和数字）：123abc
出错了：密码长度不足！要求至少8位，当前仅6位
```

## 模块5：进阶实践——异常处理的最佳实践

掌握了语法后，更重要的是掌握实际开发中的最佳实践，避免滥用异常处理导致代码可读性差、难以调试。

### 5.1 最佳实践清单

1. **优先捕获具体异常，避免捕获所有异常（** **`except:`** ** 无参数）**

    - 反例（不推荐）：`except:` 会捕获包括 `KeyboardInterrupt`（用户按Ctrl+C）在内的所有异常，不利于排查问题，也可能隐藏严重错误。

    - 正例（推荐）：明确指定需要捕获的异常类型（如 `except ZeroDivisionError:`）。

2. **不要用异常处理替代正常的逻辑判断**

    - 异常处理是用来处理「意外错误」的，不是用来处理「可预见的逻辑判断」的。

    - 反例（不推荐）：

        ```Python
        
        try:
            print(my_list[0])
        except IndexError:
            print("列表为空")
        ```

    - 正例（推荐）：

        ```Python
        
        if len(my_list) > 0:
            print(my_list[0])
        else:
            print("列表为空")
        ```

3. **用 ** **`finally`** ** 释放资源，或优先使用 ** **`with`** ** 语句**

    - 处理文件、数据库连接、网络连接等资源时，优先使用 `with` 语句（自动释放资源），其次用 `finally` 手动释放。

4. **自定义异常类，提升业务逻辑的可读性**

    - 针对特定业务场景自定义异常（如 `UserNotFoundError`），可以让代码的错误意图更清晰，便于后续维护和调试。

5. **异常信息要清晰，便于排查问题**

    - 主动抛出异常时，附加详细的错误描述（如 `raise ValueError("年龄必须在0到150之间")`），避免无意义的异常信息。

6. **避免异常嵌套过深**

    - 过多的 `try...except` 嵌套会导致代码可读性差，尽量将复杂逻辑拆分，减少异常嵌套层级。

---

### 总结

1. 异常是程序运行时的意外错误，与语法错误不同，会导致程序默认中断，常见内置异常有 `ZeroDivisionError`、`FileNotFoundError` 等。

2. 核心异常处理语法是 `try...except`，可捕获指定异常、获取异常详情，`else` 无异常时执行，`finally` 无论是否异常都必须执行（用于释放资源）。

3. 可通过 `raise` 主动抛出异常，也可继承 `Exception` 自定义异常，实际开发中要遵循“捕获具体异常、不替代逻辑判断”等最佳实践。