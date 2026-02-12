# 5_Python 数据处理：字符串和日期时间模块

---

## 模块1：字符串进阶处理（正则表达式基础 + re模块）

​	字符串处理是数据清洗的核心环节，正则表达式（`Regex`）是处理复杂字符串匹配/提取的“利器”，Python通过`re`模块提供正则支持，适合提取文本中的结构化信息（如手机号、邮箱）。

### 1.1 正则表达式核心基础（新手必懂）

正则表达式是「匹配字符串的规则集」，核心元字符及含义：

|元字符|含义|示例|
|---|---|---|
|`\d`|匹配任意数字（0-9）|`\d{11}` 匹配11位数字|
|`\w`|匹配字母/数字/下划线|`\w+` 匹配多个字母/数字|
|`\s`|匹配空白字符（空格/制表符）|`\s+` 匹配多个空白|
|`@`|匹配@符号（普通字符）|`\w+@` 匹配“xxx@”|
|`{n}`|匹配前一个字符n次|`\d{11}` 固定11位数字|
|`{n,}`|匹配前一个字符至少n次|`\w{6,}` 至少6位字母/数字|
|`^`|匹配字符串开头|`^1` 匹配以1开头的字符串|
|`$`|匹配字符串结尾|`\d$` 匹配以数字结尾的字符串|
|`|`|或逻辑|
|`()`|分组（提取匹配内容）|`(\d{11})` 提取11位数字|
### 1.2 re模块常用方法

|方法|作用|适用场景|
|---|---|---|
|`re.compile()`|编译正则表达式（重复使用时提升效率）|多次匹配同一规则|
|`re.findall()`|提取所有匹配的内容，返回列表|提取所有手机号/邮箱|
|`re.search()`|匹配第一个符合规则的内容，返回匹配对象|验证字符串是否包含目标|
|`re.sub()`|替换匹配的内容|脱敏处理（隐藏手机号中间4位）|
### 1.3 实战案例：提取文本中的手机号/邮箱

```Python
import re

# 待处理的原始文本
raw_text = """
客户联系信息：
张三：13812345678，邮箱：zhangsan@example.com
李四：13998765432，邮箱：lisi_123@test.cn
王五：18876543210（备用：17788889999），邮箱：wangwu@company.com
无效号码：12345678901（位数不对）、138123456789（超11位）
无效邮箱：wangwu@、@test.com、lisi#test.cn
"""

# ---------------------- 步骤1：提取手机号 ----------------------
# 手机号正则规则：以1开头，第二位为3/4/5/7/8/9，后接9位数字（共11位）
phone_pattern = re.compile(r"1[345789]\d{9}")
# 提取所有符合规则的手机号
phone_list = phone_pattern.findall(raw_text)
print("提取的手机号：", phone_list)  # 输出：['13812345678', '13998765432', '18876543210', '17788889999']

# ---------------------- 步骤2：提取邮箱 ----------------------
# 邮箱正则规则：用户名（字母/数字/下划线）+@+域名（字母/数字）+.+后缀（2-4位）
email_pattern = re.compile(r"\w+@[a-zA-Z0-9]+\.[a-zA-Z]{2,4}")
# 提取所有符合规则的邮箱
email_list = email_pattern.findall(raw_text)
print("提取的邮箱：", email_list)  # 输出：['zhangsan@example.com', 'lisi_123@test.cn', 'wangwu@company.com']

# ---------------------- 扩展：手机号脱敏（替换中间4位为*） ----------------------
desensitized_text = phone_pattern.sub(lambda x: x.group()[:3] + "****" + x.group()[7:], raw_text)
print("\n手机号脱敏后的文本：\n", desensitized_text)
```

### 1.4 关键解释

- `re.compile()`：编译正则表达式，避免重复解析规则，提升多次匹配效率；

- 手机号正则`1[345789]\d{9}`：严格匹配国内有效手机号（1开头，第二位限定号段，后9位数字）；

- 邮箱正则`\w+@[a-zA-Z0-9]+.[a-zA-Z]{2,4}`：覆盖大部分常见邮箱格式（用户名支持字母/数字/下划线，域名支持字母/数字，后缀2-4位如com/cn/net）；

- `re.sub()`结合匿名函数：实现手机号脱敏，`x.group()`获取匹配到的手机号，切片替换中间4位。

---

## 模块2：日期时间处理（datetime模块）

数据处理中常需解析/格式化时间（如日志、订单时间）、计算时间差，Python的`datetime`模块是处理日期时间的核心标准库，无需第三方依赖。

### 2.1 datetime模块核心类

|类|作用|常用方法|
|---|---|---|
|`datetime.datetime`|日期+时间（核心类）|`strftime()`（格式化）、`strptime()`（解析）|
|`datetime.date`|仅日期|`today()`（获取今日日期）、`fromisoformat()`（ISO格式解析）|
|`datetime.timedelta`|时间差（天/小时/分钟）|用于计算日期/时间加减|
### 2.2 实战案例1：日志时间格式化

需求：将日志中的“原始时间字符串”解析为标准格式，再转换为易读格式。

```Python
from datetime import datetime

# 模拟原始日志数据（包含不规则时间字符串）
log_data = [
    "2026-02-11 08:30:15 [INFO] 用户登录成功",
    "2026/02/11 09:15:20 [ERROR] 数据库连接失败",
    "20260211 10:20:30 [WARNING] 接口超时"
]

# 定义原始时间的解析格式（对应日志中的时间格式）
parse_formats = [
    "%Y-%m-%d %H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
    "%Y%m%d %H:%M:%S"
]

# 格式化日志时间为「YYYY年MM月DD日 HH时MM分SS秒」
formatted_logs = []
for log in log_data:
    # 提取日志中的时间字符串（前19位）
    time_str = log[:19]
    # 尝试匹配解析格式
    for fmt in parse_formats:
        try:
            # 解析时间字符串为datetime对象
            dt = datetime.strptime(time_str, fmt)
            # 格式化为易读格式
            formatted_time = dt.strftime("%Y年%m月%d日 %H时%M分%S秒")
            # 替换日志中的时间部分
            new_log = log.replace(time_str, formatted_time)
            formatted_logs.append(new_log)
            break
        except ValueError:
            continue

print("格式化后的日志：")
for log in formatted_logs:
    print(log)
```

**输出结果**：

```Plain Text
2026年02月11日 08时30分15秒 [INFO] 用户登录成功
2026年02月11日 09时15分20秒 [ERROR] 数据库连接失败
2026年02月11日 10时20分30秒 [WARNING] 接口超时
```

### 2.3 实战案例2：计算日期差

需求：计算两个日期的间隔天数、距离今日的天数，或N天后的日期。

```Python
from datetime import datetime, date, timedelta

# 案例1：计算两个日期的间隔天数
date1 = date(2026, 2, 1)  # 手动指定日期
date2 = date.today()       # 获取今日日期
delta_days = (date2 - date1).days
print(f"2026-02-01 到今日（{date2}）的间隔天数：{delta_days} 天")

# 案例2：计算10天后的日期
future_date = date2 + timedelta(days=10)
print(f"10天后的日期：{future_date}")

# 案例3：计算两个时间的小时差
time1 = datetime(2026, 2, 11, 8, 30, 0)
time2 = datetime(2026, 2, 11, 10, 45, 0)
delta_hours = (time2 - time1).total_seconds() / 3600
print(f"两个时间的间隔小时数：{delta_hours} 小时")
```

**关键解释**：

- `strptime()`：将「字符串」转为`datetime`对象（需指定匹配格式）；

- `strftime()`：将`datetime`对象转为「自定义格式的字符串」；

- `timedelta`：支持天（days）、小时（hours）、分钟（minutes）等时间差计算，可直接与`date/datetime`对象加减。

### 2.4 常用时间格式符（必记）

|格式符|含义|示例|
|---|---|---|
|`%Y`|4位年份|2026|
|`%m`|2位月份|02|
|`%d`|2位日期|11|
|`%H`|24小时制小时|14|
|`%M`|2位分钟|30|
|`%S`|2位秒|45|
---

## 模块3：数据序列化（json模块）

数据序列化是将Python对象（列表/字典）转为可存储/传输的格式（如JSON），`json`模块是Python处理JSON的标准库，支持「Python对象↔JSON字符串」的双向转换。

### 3.1 json模块核心方法

|方法|作用|适用场景|
|---|---|---|
|`json.dumps()`|将Python对象转为JSON字符串|内存中处理JSON数据|
|`json.dump()`|将Python对象写入文件（JSON格式）|保存数据到JSON文件|
|`json.loads()`|将JSON字符串转为Python对象|解析接口返回的JSON字符串|
|`json.load()`|从文件读取JSON数据并转为Python对象|读取JSON文件|
### 3.2 实战案例：通讯录数据转为JSON保存

需求：将通讯录字典数据保存为JSON文件，再读取并解析。

```Python
import json
from pathlib import Path

# 步骤1：定义通讯录数据（Python字典）
contacts = [
    {
        "姓名": "张三",
        "手机号": "13812345678",
        "邮箱": "zhangsan@example.com",
        "创建时间": "2026-02-11"
    },
    {
        "姓名": "李四",
        "手机号": "13998765432",
        "邮箱": "lisi_123@test.cn",
        "创建时间": "2026-02-10"
    }
]

# 步骤2：将数据保存为JSON文件
json_file = Path("./contacts.json")
# ensure_ascii=False：保留中文（否则会转为Unicode编码）；indent=2：格式化输出，增强可读性
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(contacts, f, ensure_ascii=False, indent=2)

print(f"通讯录已保存到 {json_file}")

# 步骤3：读取JSON文件并解析为Python对象
with open(json_file, "r", encoding="utf-8") as f:
    loaded_contacts = json.load(f)

print("\n读取的通讯录数据：")
for contact in loaded_contacts:
    print(f"姓名：{contact['姓名']}，手机号：{contact['手机号']}")
```

**JSON文件输出内容**（contacts.json）：

```JSON

[
  {
    "姓名": "张三",
    "手机号": "13812345678",
    "邮箱": "zhangsan@example.com",
    "创建时间": "2026-02-11"
  },
  {
    "姓名": "李四",
    "手机号": "13998765432",
    "邮箱": "lisi_123@test.cn",
    "创建时间": "2026-02-10"
  }
]
```

**关键解释**：

- `ensure_ascii=False`：必须设置，否则中文会被转为`\uXXXX`格式的Unicode编码；

- `indent=2`：格式化JSON输出，便于人工阅读（生产环境可省略，减少文件体积）；

- `json.load()`/`json.dump()`：直接操作文件，无需手动转换字符串，是最常用的方式。

---

## 模块4：实操练习：批量提取文本中的联系方式并保存为JSON

### 4.1 需求说明

- 输入：包含多个联系人信息的文本文件（contact.txt）；

- 处理：提取文本中的「姓名、手机号、邮箱」；

- 输出：将提取的信息保存为JSON文件（extracted_contacts.json），并添加「提取时间」字段。

### 4.2 完整实现代码

```Python

import re
import json
from datetime import datetime
from pathlib import Path

# ---------------------- 步骤1：准备测试文本文件 ----------------------
# 生成模拟的contact.txt文件
contact_text = """
客户档案：
1. 姓名：张三，电话：13812345678，邮箱：zhangsan@example.com，备注：2026-02-01 录入
2. 姓名：李四，电话：13998765432，邮箱：lisi_123@test.cn，备注：2026-02-02 录入
3. 姓名：王五，电话：18876543210（备用：17788889999），邮箱：wangwu@company.com，备注：2026-02-03 录入
4. 姓名：赵六，电话：15911112222，邮箱：zhaoliu@test.com，备注：2026-02-04 录入
无效信息：姓名：钱七，电话：1234567890，邮箱：qianqi@，备注：2026-02-05 录入
"""
with open("./contact.txt", "w", encoding="utf-8") as f:
    f.write(contact_text)

# ---------------------- 步骤2：定义正则规则 ----------------------
# 姓名正则：匹配「姓名：XXX」格式
name_pattern = re.compile(r"姓名：([^，,]+)")
# 手机号正则：提取有效11位手机号（取第一个有效号码）
phone_pattern = re.compile(r"1[345789]\d{9}")
# 邮箱正则
email_pattern = re.compile(r"\w+@[a-zA-Z0-9]+\.[a-zA-Z]{2,4}")

# ---------------------- 步骤3：读取文本并提取数据 ----------------------
text_file = Path("./contact.txt")
with open(text_file, "r", encoding="utf-8") as f:
    text = f.read()

# 按行分割文本（逐行处理，避免无效信息干扰）
lines = text.split("\n")
extracted_data = []
extract_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 提取时间

for line in lines:
    line = line.strip()
    if not line or "无效信息" in line:
        continue  # 跳过空行和无效信息行
    
    # 提取姓名
    name_match = name_pattern.search(line)
    name = name_match.group(1) if name_match else "未知姓名"
    
    # 提取手机号（取第一个有效号码）
    phone_match = phone_pattern.search(line)
    phone = phone_match.group() if phone_match else "无"
    
    # 提取邮箱
    email_match = email_pattern.search(line)
    email = email_match.group() if email_match else "无"
    
    # 整理数据
    extracted_data.append({
        "姓名": name,
        "手机号": phone,
        "邮箱": email,
        "提取时间": extract_time
    })

# ---------------------- 步骤4：保存为JSON文件 ----------------------
json_file = Path("./extracted_contacts.json")
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=2)

print(f"提取完成！共提取 {len(extracted_data)} 条有效联系人信息，已保存到 {json_file}")

# ---------------------- 步骤5：验证读取结果 ----------------------
with open(json_file, "r", encoding="utf-8") as f:
    result = json.load(f)

print("\n验证提取结果：")
for item in result:
    print(f"姓名：{item['姓名']}，手机号：{item['手机号']}，邮箱：{item['邮箱']}")
```

### 4.3 输出结果

- `extracted_contacts.json` 文件内容：

```JSON

[
  {
    "姓名": "张三",
    "手机号": "13812345678",
    "邮箱": "zhangsan@example.com",
    "提取时间": "2026-02-11 15:30:00"
  },
  {
    "姓名": "李四",
    "手机号": "13998765432",
    "邮箱": "lisi_123@test.cn",
    "提取时间": "2026-02-11 15:30:00"
  },
  {
    "姓名": "王五",
    "手机号": "18876543210",
    "邮箱": "wangwu@company.com",
    "提取时间": "2026-02-11 15:30:00"
  },
  {
    "姓名": "赵六",
    "手机号": "15911112222",
    "邮箱": "zhaoliu@test.com",
    "提取时间": "2026-02-11 15:30:00"
  }
]
```

- 控制台输出：

```Plain Text

提取完成！共提取 4 条有效联系人信息，已保存到 extracted_contacts.json

验证提取结果：
姓名：张三，手机号：13812345678，邮箱：zhangsan@example.com
姓名：李四，手机号：13998765432，邮箱：lisi_123@test.cn
姓名：王五，手机号：18876543210，邮箱：wangwu@company.com
姓名：赵六，手机号：15911112222，邮箱：zhaoliu@test.com
```

### 4.4 核心逻辑总结

1. 按行处理文本：跳过空行和无效信息行，减少匹配干扰；

2. 正则`search()`而非`findall()`：针对单行提取单个目标（如姓名、第一个手机号）；

3. 异常兜底：提取失败时赋值为“未知姓名”/“无”，避免程序报错；

4. 新增「提取时间」：结合`datetime`模块丰富数据维度，符合实际数据处理需求。

---

### 总结

1. **字符串处理**：`re`模块是提取结构化信息的核心，重点掌握`compile()`（编译规则）、`findall()`（批量提取）、`search()`（单个提取），手机号/邮箱正则需记住核心规则；

2. **日期时间**：`datetime`模块的`strptime()`（解析）和`strftime()`（格式化）是双向转换关键，`timedelta`用于时间差计算；

3. **JSON序列化**：`json.dump()`/`json.load()`是文件操作的首选，`ensure_ascii=False`是保留中文的必设参数；

4. **综合应用**：数据处理的核心流程是「读取原始数据→正则提取→格式转换→序列化保存」，需注意异常兜底和数据完整性。
