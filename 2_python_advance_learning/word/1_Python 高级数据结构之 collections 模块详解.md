# 1_Python 高级数据结构

## 模块1：核心基础——`collections` 模块（Python内置高级数据结构核心）

​	`Python`的 `collections` 模块是内置的标准库，无需额外安装，提供了一系列**弥补基础数据结构（列表、字典、元组、集合）不足**的高级数据结构，是日常开发中高频使用的工具，也是高级数据结构的入门核心。

### 1.1 计数器：`Counter`

#### 1.1.1 概念与优势

`Counter` 是一个**字典的子类**，专门用于**统计可迭代对象（字符串、列表、元组等）中元素的出现次数**，相比手动用普通字典统计，它更简洁、更高效，还提供了专属的统计方法。

#### 1.1.2 基本用法与示例

##### 步骤1：导入 `Counter`

```Python

from collections import Counter
```

##### 步骤2：创建 `Counter` 对象

```Python

# 示例1：统计字符串中字符的出现次数
str_data = "hello python, hello world"
str_counter = Counter(str_data)
print("字符串统计结果：", str_counter)

# 示例2：统计列表中元素的出现次数
list_data = [1, 2, 3, 2, 1, 3, 3, 4, 2, 1]
list_counter = Counter(list_data)
print("列表统计结果：", list_counter)
```

运行结果：

```Plain Text

字符串统计结果： Counter({'l': 5, 'o': 4, 'h': 2, 'e': 2, ' ': 4, 'p': 1, 'y': 1, 't': 1, 'n': 1, ',': 1, 'w': 1, 'r': 1, 'd': 1})
列表统计结果： Counter({1: 3, 2: 3, 3: 3, 4: 1})
```

#### 1.1.3 核心常用方法

|方法|说明|示例|
|---|---|---|
|`most_common(n)`|返回出现次数最多的 `n` 个元素，以「(元素, 次数)」元组组成的列表返回；`n` 省略时返回所有元素|`list_counter.most_common(2)` → `[(1, 3), (2, 3)]`|
|`update(iterable)`|新增可迭代对象，更新统计结果（累加次数，而非覆盖）|`list_counter.update([1, 2])` → `Counter({1:4, 2:4, 3:3, 4:1})`|
|`elements()`|返回一个迭代器，包含所有统计元素（按次数重复，无顺序）|`list(str_counter.elements())` → 列出所有统计的字符|
示例：使用核心方法

```Python

from collections import Counter

list_data = [1, 2, 3, 2, 1, 3, 3, 4, 2, 1]
list_counter = Counter(list_data)

# 1. 获取出现次数最多的2个元素
top2 = list_counter.most_common(2)
print("出现次数最多的2个元素：", top2)

# 2. 更新统计结果（累加）
list_counter.update([1, 2, 5])
print("更新后的统计结果：", list_counter)

# 3. 遍历所有统计元素
print("所有统计元素：", list(list_counter.elements()))
```

#### 1.1.4 适用场景

- 文本字符/单词频率统计（如文章关键词提取）。

- 列表/元组中重复元素的次数统计（如统计投票结果）。

- 数据去重后的次数记录（比普通字典更简洁）。

### 1.2 默认值字典：`defaultdict`

#### 1.2.1 概念与优势

`defaultdict` 是**字典的子类**，解决了普通字典的一个痛点：**访问不存在的键时，不会抛出 ** **`KeyError`** ** 异常，而是自动为该键创建一个默认值**。

普通字典访问不存在的键会报错，而 `defaultdict` 可以通过指定「默认值类型」，自动生成默认值（如列表、整数、集合等），简化代码逻辑。

#### 1.2.2 基本用法与示例

##### 步骤1：导入 `defaultdict`

```Python

from collections import defaultdict
```

##### 步骤2：创建 `defaultdict` 对象（指定默认值类型）

```Python

# 示例1：默认值类型为 list（自动创建空列表作为默认值）
dict_list = defaultdict(list)
# 访问不存在的键 "a"，自动创建空列表 []
dict_list["a"].append(1)
dict_list["a"].append(2)
dict_list["b"].append(3)
print("默认值为列表的字典：", dict(dict_list))

# 示例2：默认值类型为 int（自动创建 0 作为默认值）
dict_int = defaultdict(int)
# 访问不存在的键 "count1"，自动创建 0，然后累加
dict_int["count1"] += 1
dict_int["count1"] += 2
dict_int["count2"] += 1
print("默认值为整数的字典：", dict(dict_int))

# 示例3：默认值类型为 set（自动创建空集合作为默认值）
dict_set = defaultdict(set)
dict_set["s1"].add(1)
dict_set["s1"].add(2)
dict_set["s2"].add(3)
print("默认值为集合的字典：", dict(dict_set))
```

运行结果：

```Plain Text

默认值为列表的字典： {'a': [1, 2], 'b': [3]}
默认值为整数的字典： {'count1': 3, 'count2': 1}
默认值为集合的字典： {'s1': {1, 2}, 's2': {3}}
```

#### 1.2.3 核心要点

- 创建 `defaultdict` 时，必须指定「默认值工厂函数」（即默认值类型），常用的有 `list`、`int`、`set`、`str` 等。

- 默认值仅在「访问不存在的键」时自动创建，若键已存在，直接使用现有值。

- 它的其他用法与普通字典完全一致（支持 `keys()`、`values()`、`items()` 等方法）。

#### 1.2.4 适用场景

- 分组统计（如将列表中的元素按某个规则分组，存入字典的列表中）。

- 计数统计（无需手动判断键是否存在，直接累加，比普通字典简洁）。

- 避免 `KeyError` 异常，简化代码逻辑（无需额外写 `if key not in dict` 判断）。

### 1.3 命名元组：`namedtuple`

#### 1.3.1 概念与优势

`namedtuple` 是一个**工厂函数**，用于创建「具名元组」—— 一种**不可变的、可以通过属性名访问元素的元组**，弥补了普通元组的不足：

普通元组只能通过「索引」访问元素（如 `t[0]`、`t[1]`），可读性差；而 `namedtuple` 可以通过「属性名」访问元素（如 `t.name`、`t.age`），同时保留元组的不可变性，且比自定义类更轻量（无需编写 `__init__` 方法）。

#### 1.3.2 基本用法与示例

##### 步骤1：导入 `namedtuple`

```Python

from collections import namedtuple
```

##### 步骤2：创建具名元组类（指定类名和字段名）

```Python

# 格式：namedtuple(类名, 字段名列表/字符串)
# 方式1：字段名用列表传入
Person = namedtuple("Person", ["name", "age", "gender"])

# 方式2：字段名用空格分隔的字符串传入（更简洁）
Student = namedtuple("Student", "name id grade")
```

##### 步骤3：创建具名元组实例并使用

```Python

# 1. 创建 Person 实例
p1 = Person(name="张三", age=20, gender="男")
p2 = Person("李四", 22, "女")  # 也可以按字段顺序传入参数

# 2. 访问元素（两种方式：属性名 或 索引）
print("p1 姓名：", p1.name)  # 推荐：属性名访问，可读性强
print("p1 年龄：", p1.age)
print("p1 性别（索引访问）：", p1[2])

# 3. 具名元组不可变（与普通元组一致，无法修改属性值）
# p1.age = 25  # 报错：AttributeError: can't set attribute

# 4. 常用方法：_asdict() → 转换为有序字典（Python3.7+）
print("p1 转换为字典：", p1._asdict())

# 5. 常用方法：_replace() → 创建一个新实例，替换指定字段值（不修改原实例）
p3 = p1._replace(age=21, gender="未知")
print("原实例 p1：", p1)
print("新实例 p3：", p3)
```

运行结果：

```Plain Text

p1 姓名： 张三
p1 年龄： 20
p1 性别（索引访问）： 男
p1 转换为字典： {'name': '张三', 'age': 20, 'gender': '男'}
原实例 p1： Person(name='张三', age=20, gender='男')
新实例 p3： Person(name='张三', age=21, gender='未知')
```

#### 1.3.3 适用场景

- 存储固定结构的不可变数据（如配置信息、数据记录、坐标点等）。

- 替代轻量级类（无需编写复杂的类，仅需存储数据，无额外方法）。

- 提高代码可读性（用属性名替代索引，避免记混元素顺序）。

### 1.4 双端队列：`deque`

#### 1.4.1 概念与优势

`deque`（double-ended queue，双端队列）是一个**高效的双端操作队列**，弥补了列表的不足：

列表的 `append()`（尾部添加）和 `pop()`（尾部删除）效率很高，但**头部插入（** **`insert(0, x)`** **）和头部删除（** **`pop(0)`** **）效率极低**（因为列表是连续内存，头部操作需要移动所有元素）；而 `deque` 专门优化了双端操作，**头部和尾部的添加/删除操作效率都为 O(1)**，且支持线程安全。

#### 1.4.2 基本用法与示例

##### 步骤1：导入 `deque`

```Python

from collections import deque
```

##### 步骤2：创建 `deque` 对象

```Python

# 1. 创建空双端队列
d1 = deque()

# 2. 从可迭代对象创建双端队列
d2 = deque([1, 2, 3, 4])
d3 = deque("hello")
print("d2 初始值：", d2)
print("d3 初始值：", d3)
```

##### 步骤3：核心双端操作方法

|方法|说明|示例|
|---|---|---|
|`append(x)`|尾部添加元素 `x`|`d2.append(5)` → `deque([1,2,3,4,5])`|
|`appendleft(x)`|头部添加元素 `x`|`d2.appendleft(0)` → `deque([0,1,2,3,4,5])`|
|`pop()`|尾部删除元素，返回该元素|`d2.pop()` → 返回 5，`d2` 变为 `deque([0,1,2,3,4])`|
|`popleft()`|头部删除元素，返回该元素|`d2.popleft()` → 返回 0，`d2` 变为 `deque([1,2,3,4])`|
|`extend(iterable)`|尾部扩展可迭代对象|`d2.extend([5,6])` → `deque([1,2,3,4,5,6])`|
|`extendleft(iterable)`|头部扩展可迭代对象（元素顺序反转）|`d2.extendleft([0,-1])` → `deque([-1,0,1,2,3,4,5,6])`|
|`clear()`|清空双端队列|`d2.clear()` → `deque([])`|
示例：使用核心方法

```Python

from collections import deque

d = deque([1, 2, 3])

# 1. 双端添加元素
d.append(4)  # 尾部添加
d.appendleft(0)  # 头部添加
print("添加元素后：", d)

# 2. 双端删除元素
last_elem = d.pop()  # 尾部删除
first_elem = d.popleft()  # 头部删除
print("删除的尾部元素：", last_elem)
print("删除的头部元素：", first_elem)
print("删除元素后：", d)

# 3. 扩展元素
d.extend([4, 5])  # 尾部扩展
d.extendleft([-1, 0])  # 头部扩展（顺序反转）
print("扩展元素后：", d)
```

运行结果：

```Plain Text

添加元素后： deque([0, 1, 2, 3, 4])
删除的尾部元素： 4
删除的头部元素： 0
删除元素后： deque([1, 2, 3])
扩展元素后： deque([0, -1, 1, 2, 3, 4, 5])
```

#### 1.4.3 适用场景

- 需要频繁在头部和尾部进行操作的场景（如队列、栈、缓存等）。

- 替代列表实现栈（`append()` + `pop()`）或队列（`append()` + `popleft()`）。

- 滑动窗口问题（如字符串匹配、数据过滤的滑动窗口）。

---

## 模块2：其他内置高级数据结构

除了 `collections` 模块，Python还内置了一些其他高级数据结构，用于解决特定场景的问题，同样具有很高的实用价值。

### 2.1 不可变集合：`frozenset`

#### 2.1.1 概念与优势

`frozenset` 是**不可变的集合**，与普通集合（`set`）的区别在于：

- 普通集合（`set`）是可变的，支持 `add()`、`remove()` 等修改方法。

- `frozenset` 是不可变的，创建后无法修改（无添加、删除方法），支持集合的所有查询/运算方法（如 `union()`、`intersection()` 等）。

核心优势：`frozenset` 可以作为**字典的键**、可以**嵌套在其他集合中**，而普通集合不行。

#### 2.1.2 基本用法与示例

```Python

# 1. 创建 frozenset 对象
# 方式1：从可迭代对象创建
fs1 = frozenset([1, 2, 3, 4])
fs2 = frozenset("hello")

# 方式2：创建空 frozenset
fs3 = frozenset()

print("fs1：", fs1)
print("fs2：", fs2)

# 2. 支持集合运算（与普通集合一致）
fs4 = frozenset([3, 4, 5, 6])
# 并集
print("并集：", fs1.union(fs4))
# 交集
print("交集：", fs1.intersection(fs4))
# 差集
print("差集：", fs1.difference(fs4))

# 3. 不可修改（无 add()、remove() 方法）
# fs1.add(5)  # 报错：AttributeError: 'frozenset' object has no attribute 'add'

# 4. 可以作为字典的键
my_dict = {fs1: "这是一个不可变集合作为键"}
print("字典：", my_dict)
```

运行结果：

```Plain Text

fs1： frozenset({1, 2, 3, 4})
fs2： frozenset({'h', 'e', 'l', 'o'})
并集： frozenset({1, 2, 3, 4, 5, 6})
交集： frozenset({3, 4})
差集： frozenset({1, 2})
字典： {frozenset({1, 2, 3, 4}): '这是一个不可变集合作为键'}
```

#### 2.1.3 适用场景

- 需要将集合作为字典键或嵌套在其他集合中的场景。

- 需要保证集合数据不可被修改的场景（如配置集合、常量集合）。

### 2.2 堆队列：`heapq` 模块（优先队列）

#### 2.2.1 概念与优势

`heapq` 模块实现了**小顶堆（最小堆）**数据结构，堆是一种完全二叉树，具有「父节点值小于等于子节点值」的特性，核心优势是：

- 快速获取并删除最小值（时间复杂度 O(1) 查找，O(log n) 删除）。

- 快速插入元素（时间复杂度 O(log n)）。

`heapq` 模块没有单独的堆类，而是通过操作普通列表来实现堆功能，列表被视为堆的底层存储结构。

#### 2.2.2 基本用法与示例

##### 步骤1：导入 `heapq` 模块

```Python

import heapq
```

##### 步骤2：核心方法使用

|方法|说明|
|---|---|
|`heapq.heappush(heap, item)`|向堆 `heap` 中插入元素 `item`，维持堆的特性|
|`heapq.heappop(heap)`|从堆 `heap` 中弹出并返回最小值，维持堆的特性|
|`heapq.heapify(x)`|将列表 `x` 原地转换为堆（时间复杂度 O(n)）|
|`heapq.nlargest(n, iterable)`|返回可迭代对象中前 `n` 个最大的元素|
|`heapq.nsmallest(n, iterable)`|返回可迭代对象中前 `n` 个最小的元素|
示例：核心方法演示

```Python

import heapq

# 1. 构建堆（方式1：逐个插入）
heap1 = []
heapq.heappush(heap1, 3)
heapq.heappush(heap1, 1)
heapq.heappush(heap1, 4)
heapq.heappush(heap1, 2)
print("逐个插入构建的堆：", heap1)  # 输出：[1, 2, 4, 3]（堆的底层列表，并非完全有序）

# 2. 构建堆（方式2：heapify 原地转换，更高效）
list_data = [3, 1, 4, 2]
heapq.heapify(list_data)
print("heapify 转换的堆：", list_data)  # 输出：[1, 2, 4, 3]

# 3. 弹出最小值
min_elem1 = heapq.heappop(heap1)
print("弹出的最小值1：", min_elem1)
print("弹出后堆1：", heap1)

# 4. 获取前 n 大/前 n 小元素
data = [5, 2, 9, 1, 7, 4]
top3_largest = heapq.nlargest(3, data)
top3_smallest = heapq.nsmallest(3, data)
print("前3个最大元素：", top3_largest)
print("前3个最小元素：", top3_smallest)
```

运行结果：

```Plain Text

逐个插入构建的堆： [1, 2, 4, 3]
heapify 转换的堆： [1, 2, 4, 3]
弹出的最小值1： 1
弹出后堆1： [2, 3, 4]
前3个最大元素： [9, 7, 5]
前3个最小元素： [1, 2, 4]
```

#### 2.2.3 适用场景

- Top N 问题（如获取文章中出现频率最高的10个单词、数据中最大的5个值）。

- 优先队列实现（如任务调度，优先执行优先级高的任务）。

- 排序场景（堆排序，虽然Python中更常用 `sorted()`，但堆排序在大数据场景下有优势）。

---

## 模块3：进阶拓展——自定义/第三方高级数据结构

### 3.1 有序集合（`SortedSet`）

Python内置没有提供有序集合，若需要「有序且不重复」的数据结构，可通过两种方式实现：

1. **使用 ** **`bisect`** ** 模块**：对列表进行二分查找和插入，维持列表的有序性，模拟有序集合。

2. **第三方库 ** **`sortedcontainers`**：提供 `SortedSet`、`SortedDict` 等高效有序数据结构，需要先安装：

    ```Bash
    
    pip install sortedcontainers
    ```

示例：使用 `SortedSet`

```Python

from sortedcontainers import SortedSet

ss = SortedSet([3, 1, 4, 2])
print("有序集合：", ss)  # 输出：SortedSet([1, 2, 3, 4])

# 插入元素（自动维持有序）
ss.add(5)
ss.add(2)  # 重复元素不插入
print("插入后有序集合：", ss)

# 查找元素索引
print("元素 3 的索引：", ss.index(3))

# 切片操作
print("切片 [1:3]：", ss[1:3])
```

### 3.2 队列拓展（`queue` 模块）

`queue` 模块提供了多线程安全的队列结构，用于多线程编程：

- `Queue`：普通队列（先进先出，FIFO）。

- `LifoQueue`：栈（后进先出，LIFO）。

- `PriorityQueue`：优先队列（按优先级排序）。

### 总结

1. 核心高级数据结构集中在 `collections` 模块，`Counter` 用于计数、`defaultdict` 避免 `KeyError`、`namedtuple` 提升数据可读性、`deque` 优化双端操作。

2. 其他内置结构中，`frozenset` 是不可变集合（可作为字典键），`heapq` 实现小顶堆（解决Top N问题）。

3. 进阶场景可使用 `bisect` 模拟有序集合，或第三方库 `sortedcontainers`，`queue` 模块适用于多线程场景。