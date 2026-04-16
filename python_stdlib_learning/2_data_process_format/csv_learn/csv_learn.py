"""
CSV标准库学习
"""

import csv

# 1、CSV的基本结构和基础读取
# 基本结构：每一行代表一条数据，行内使用逗号进行分隔
# name,age,address
# jom,11,A城市
# kom,12,B城市
# lom,13,C城市
with open("./stus.csv", mode="r", encoding="utf-8", newline="") as f:
    # 返回一个迭代器对象，每次返回它的行数据
    reader = csv.reader(f)
    # 通过next(迭代器对象)，避免将表头作为数据进行处理
    headers = next(reader)
    print(headers)
    for row in reader:
        print(f"行数据:{row}")
        print(f"姓名:{row[0]};年龄:{row[1]};城市:{row[2]}")

print("-" * 10)
# 2、如何按照列名进行读取
# [name,age,address]
with open("./stus.csv", mode="r", encoding="utf-8", newline="") as f:
    # 创建一个dictreader对象
    reader = csv.DictReader(f)
    print(reader)
    print(type(reader))
    # 读取表头
    headers = reader.fieldnames
    print(f"表头:{headers}")
    for row in reader:
        print(row, type(row))
        print(f"年龄:{row['age']}")

print("-" * 10)
# 3、基础写入操作
headers = ["product", "price", "stock"]
# 数据单元封装在列表之中，每一个数据单元都是一个列表
data = [["python入门", 11, 100], ["CSV学习", 22, 200], ["XML学习", 33, 300]]
with open("products.csv", mode="w", encoding="utf-8-sig", newline="") as f:
    writer_obj = csv.writer(f)
    # 写入csv表头，因为表头肯定只有一行，那么在这里只需要调用单行写入
    writer_obj.writerow(headers)
    # 写入csv数据，因为数据肯定有多行，那么在这里需要调用多行写入方式
    writer_obj.writerows(data)
print("文件写入成功")

# 4、如何按照字典进行写入
# 每一个数据单元都是一个字典 数据单元=数据行
data = [
    {"name": "dom", "age": 88, "city": "H市"},
    {"name": "hom", "age": 44, "city": "A市"},
    {"name": "gom", "age": 122, "city": "B市"},
]
headers = ["name", "age", "city"]
with open("new_stu.csv", mode="w", encoding="utf-8-sig", newline="") as f:
    writer_obj = csv.DictWriter(f, fieldnames=headers)
    writer_obj.writeheader()
    writer_obj.writerows(data)
print("已经写入成功")

print("-" * 10)
# 5、自定义分隔符的设置
data = [["a", "b", "c"], ["1", "2", "3"]]
with open("example_data.csv", mode="w", encoding="utf-8", newline="") as f:
    # 假设分隔符变为tab \t
    w = csv.writer(f, delimiter="\t")
    w.writerows(data)


with open("./example_data.csv", mode="r", encoding="utf-8", newline="") as f:
    r = csv.reader(f, delimiter="\t")
    for row in r:
        print(row)


# 6、实战案例
