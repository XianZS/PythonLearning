# 5_Python 四大核心容器类型

## 一、四大核心数据结构基础用法

### 1. 列表（List）

**核心特性**：有序、可变、可重复，是最常用的“动态数组”。

#### 基础操作

```Python

# 1. 定义
fruits = ["苹果", "香蕉", "橙子", "苹果"]  # 支持重复元素
empty_list = []  # 空列表

# 2. 查：索引（从0开始）、切片、成员判断
print(fruits[0])       # 取第一个元素：苹果
print(fruits[1:3])     # 切片（左闭右开）：['香蕉', '橙子']
print("香蕉" in fruits) # 成员判断：True

# 3. 增：append(末尾加)、insert(指定位置加)、extend(批量加)
fruits.append("葡萄")   # 末尾添加：['苹果', '香蕉', '橙子', '苹果', '葡萄']
fruits.insert(1, "草莓")# 索引1位置添加：['苹果', '草莓', '香蕉', '橙子', '苹果', '葡萄']
fruits.extend(["芒果", "梨"]) # 批量添加：['苹果', '草莓', '香蕉', '橙子', '苹果', '葡萄', '芒果', '梨']

# 4. 改：通过索引赋值
fruits[0] = "红苹果"   # 修改第一个元素

# 5. 删：del(按索引删)、remove(按值删)、pop(删并返回)
del fruits[5]          # 删除索引5的元素
fruits.remove("苹果")  # 删除第一个匹配的"苹果"
fruits.pop()           # 删除最后一个元素并返回

# 6. 常用方法
print(len(fruits))     # 长度：6
fruits.sort()          # 排序（字符串按拼音/字母）
fruits.reverse()       # 反转
print(fruits.count("香蕉")) # 统计元素出现次数：1
```

### 2. 元组（Tuple）

**核心特性**：有序、不可变、可重复，适合存储固定数据（如坐标、配置）。

#### 基础操作

```Python

# 1. 定义（单个元素必须加逗号）
point = (10, 20)       # 坐标
single_tuple = (5,)    # 单个元素的元组
empty_tuple = ()       # 空元组
# 简化定义（无括号）
colors = "红", "绿", "蓝"

# 2. 查：索引、切片、成员判断（和列表一致）
print(point[0])        # 10
print(point[1:])       # (20,)
print(20 in point)     # True

# 3. 不可改/增/删（修改会报错）
# point[0] = 15  # 报错：TypeError: 'tuple' object does not support item assignment

# 4. 常用方法
print(len(point))      # 长度：2
print(colors.count("红")) # 统计：1
print(colors.index("绿")) # 找索引：1
```

### 3. 字典（Dict）

**核心特性**：无序（Python3.7+默认有序）、可变、键值对结构，键唯一且不可变（字符串/数字/元组）。

#### 基础操作

```Python

# 1. 定义
student = {
    "name": "小明",
    "age": 18,
    "score": {"语文": 90, "数学": 85}
}
empty_dict = {}        # 空字典

# 2. 查：[]取值（键不存在报错）、get取值（键不存在返回默认值）
print(student["name"]) # 小明
print(student.get("gender", "未知")) # 键不存在，返回默认值：未知

# 3. 增：直接赋值（键不存在则新增）
student["gender"] = "男"
student.setdefault("city", "北京") # 新增（键存在则不修改）

# 4. 改：直接赋值（键存在则修改）
student["age"] = 19

# 5. 删：del(按键删)、pop(删并返回)、popitem(删最后一个键值对)
del student["city"]
student.pop("score")   # 删除"score"键并返回对应值
student.popitem()      # 删除最后一个键值对

# 6. 常用方法
print(student.keys())  # 所有键：dict_keys(['name', 'age'])
print(student.values())# 所有值：dict_values(['小明', 19])
print(student.items()) # 所有键值对：dict_items([('name', '小明'), ('age', 19)])
student.update({"height": 175}) # 批量更新/新增
```

### 4. 集合（Set）

**核心特性**：无序、可变、无重复元素，适合去重、集合运算（交集/并集）。

#### 基础操作

```Python

# 1. 定义（空集合必须用set()，{}是空字典）
nums = {1, 2, 3, 3, 4} # 自动去重：{1,2,3,4}
empty_set = set()      # 空集合
# 从列表/元组转集合（去重）
fruit_set = set(["苹果", "香蕉", "苹果"]) # {'苹果', '香蕉'}

# 2. 查：成员判断（无索引，因为无序）
print(2 in nums)       # True

# 3. 增：add(加单个)、update(批量加)
nums.add(5)            # {1,2,3,4,5}
nums.update([6,7])     # {1,2,3,4,5,6,7}

# 4. 删：remove(删不存在报错)、discard(删不存在不报错)、pop(随机删)
nums.remove(7)         # 删除7
nums.discard(8)        # 删除8（不存在，无报错）
nums.pop()             # 随机删除一个元素

# 5. 集合运算（核心用法）
a = {1,2,3,4}
b = {3,4,5,6}
print(a & b)           # 交集：{3,4}
print(a | b)           # 并集：{1,2,3,4,5,6}
print(a - b)           # 差集：{1,2}
print(a ^ b)           # 对称差集（互不包含）：{1,2,5,6}
```

## 二、综合示例（学生信息管理）

以下示例几乎覆盖四大数据结构的所有核心用法，模拟一个简易的学生信息管理场景：

```Python

def manage_students():
    """
    学生信息管理示例：整合列表、元组、字典、集合的核心用法
    """
    # 1. 列表：存储所有学生（每个元素是字典）
    students = []
    
    # 2. 元组：存储固定的学科（不可变）
    subjects = ("语文", "数学", "英语")
    
    # 3. 集合：存储所有学生的兴趣标签（自动去重）
    all_hobbies = set()
    
    # 添加学生信息
    print("===== 添加学生信息 =====")
    # 学生1
    stu1 = {
        "id": 101,
        "name": "小明",
        "age": 18,
        "scores": {sub: 90 for sub in subjects},  # 字典推导式
        "hobbies": {"篮球", "编程", "阅读"}       # 集合存兴趣
    }
    students.append(stu1)  # 列表添加元素
    all_hobbies.update(stu1["hobbies"])  # 集合批量添加
    
    # 学生2
    stu2 = {
        "id": 102,
        "name": "小红",
        "age": 17,
        "scores": {"语文": 95, "数学": 88, "英语": 92},
        "hobbies": {"绘画", "编程", "音乐"}
    }
    students.append(stu2)
    all_hobbies.update(stu2["hobbies"])
    
    # 4. 遍历与查询（列表+字典）
    print("\n===== 所有学生信息 =====")
    for stu in students:
        print(f"学号：{stu['id']}，姓名：{stu['name']}，年龄：{stu['age']}")
        print(f"成绩：{stu['scores']}")
        print(f"兴趣：{stu['hobbies']}\n")
    
    # 5. 集合运算：找两个学生的共同兴趣
    common_hobbies = stu1["hobbies"] & stu2["hobbies"]
    print(f"小明和小红的共同兴趣：{common_hobbies}")
    
    # 6. 元组切片：取前两个学科
    print(f"重点学科：{subjects[:2]}")
    
    # 7. 修改学生信息（列表+字典）
    print("\n===== 修改学生信息 =====")
    # 找到小明，修改数学成绩
    for stu in students:
        if stu["name"] == "小明":
            stu["scores"]["数学"] = 95  # 字典修改值
            stu["age"] += 1             # 年龄+1
            print(f"修改后小明的信息：{stu}")
            break
    
    # 8. 删除学生兴趣（集合）
    stu2["hobbies"].remove("音乐")  # 集合删除元素
    print(f"\n小红删除音乐兴趣后：{stu2['hobbies']}")
    
    # 9. 统计所有兴趣标签
    print(f"\n所有学生的兴趣标签（去重）：{all_hobbies}")
    print(f"兴趣标签总数：{len(all_hobbies)}")

# 执行函数
if __name__ == "__main__":
    manage_students()
```

### 运行结果

```Plain Text

===== 添加学生信息 =====

===== 所有学生信息 =====
学号：101，姓名：小明，年龄：18
成绩：{'语文': 90, '数学': 90, '英语': 90}
兴趣：{'阅读', '篮球', '编程'}

学号：102，姓名：小红，年龄：17
成绩：{'语文': 95, '数学': 88, '英语': 92}
兴趣：{'绘画', '编程', '音乐'}

小明和小红的共同兴趣：{'编程'}
重点学科：('语文', '数学')

===== 修改学生信息 =====
修改后小明的信息：{'id': 101, 'name': '小明', 'age': 19, 'scores': {'语文': 90, '数学': 95, '英语': 90}, 'hobbies': {'阅读', '篮球', '编程'}}

小红删除音乐兴趣后：{'绘画', '编程'}

所有学生的兴趣标签（去重）：{'阅读', '绘画', '篮球', '编程', '音乐'}
兴趣标签总数：5
```

### 总结

1. **核心特性区分**：列表（有序可变）、元组（有序不可变）、字典（键值对）、集合（无序无重复）；

2. **核心用法**：列表侧重“有序批量存储”，元组侧重“固定不可变数据”，字典侧重“键值映射”，集合侧重“去重和集合运算”；

3. **实战技巧**：四大结构常组合使用（如列表存字典、字典值为集合），需根据数据特点选择合适的结构。

