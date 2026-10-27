"""
sqlite3 标准库学习
"""

import sqlite3


# 1、核心概念和基础连接
# 整个数据库就是一个db文件，test.db：这就是一个数据库
# 不需要安装任何额外的东西，支持SQL原生语法
# 步骤一：连接数据库
conn = sqlite3.connect("test.db")
# 步骤二：创建游标
cursor = conn.cursor()
# 步骤三：通过游标对象，来执行sql
cursor.execute(
    """
    create table if not exists people(
    id integer primary key autoincrement,
    name text not null,
    age int
    )
    """
)
# 步骤四：通过连接对象，来提交事务
conn.commit()
# 步骤五：关闭连接
cursor.close()
conn.close()
# 2、增删查改 CRUD操作
# 数据插入
# 最好使用？占位符，不要使用字符串拼接操作
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    # 插入单条数据
    # 通过？占位符的形式插入数据，类型是元组
    cursor.execute("insert into people (name,age) values (?,?)", ("jom", 25))
    # 通过命名参数的形式插入数据，类型是字典
    cursor.execute(
        "insert into people (name,age) values (:key_1,:key_2)",
        {"key_1": "kom", "key_2": 33},
    )
    # 如何进行批量插入
    users = [("lom", 22), ("pom", 33), ("iom", 44)]
    cursor.executemany("insert into people (name,age) values (?,?)", users)
    print("批量插入成功")
# 数据查找
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    # 如何查询所有的数据
    cursor.execute("select * from people")
    all_users = cursor.fetchall()
    print(all_users, type(all_users))
    for cho in all_users:
        print(f"name:{cho[1]},age:{cho[2]}")
    # 找到某一个特定数据
    # 第一种操作：先查询出所有的数据，然后在所有的数据之中进行筛选，最后再输出目标数据。
    # 第二种操作：直接查询出目标数据，然后再输出。
    # 查询id=9
    cursor.execute("select * from people where id=?", (9,))
    user1 = cursor.fetchall()
    print(f"id=9的数据修改之前为:{user1}")
# 数据的更新
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("update people set age=? where id=?", (100, 9))
    cursor.execute("select * from people where id=?", (9,))
    user2 = cursor.fetchall()
    print(f"id=9的数据修改之后为:{user2}")
# 数据的删除
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    # 删除id=1的这条数据
    cursor.execute("delete from people where id = ?", (1,))
    cursor.execute("select * from people")
    all_users = cursor.fetchall()
    print(all_users)


# fetchall() 查询所有的结果
# fetchone() 查询单条结果
# fetchmany(n) 查询前n条结果
# 3、进阶实用技巧
# 让查询结果返回为字典
# 默认查询格式：[(9, 'pom', 100)]
# [{id:9,name:pom,age:100}]
# 不需要关心下标，只需要知道咱们所需要查询的键值对是如何组成的？
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


with sqlite3.connect("test.db") as conn:
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("select * from people")
    all_users = cursor.fetchall()
    print(f"字典格式的用户:{all_users}")
    # 列表+元组 all_users[0][1]
    # 列表+字典 all_users[0]["name"]

# 快速查询最后一条数据的id信息
with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("insert into people (name,age) values (?,?)", ("qom", 99))
    last_id = cursor.lastrowid
    print(f"得到在当前事务之中，最后一次插入时的id:{last_id}")

# 4、常见应用场景
# 桌面化软件本地存储
# 快速检查产品的存储
# 移动端应用
# 支持小型网站的后台
