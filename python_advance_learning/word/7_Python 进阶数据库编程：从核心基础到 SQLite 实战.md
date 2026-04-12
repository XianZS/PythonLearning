# 7_Python 进阶数据库编程：从核心基础到 SQLite 实战

---

## 模块1：Python数据库编程核心基础（底层逻辑）

### 1.1 数据库编程核心模型

Python操作数据库的核心是「客户端-服务器」架构（特殊的C/S）：

- **Python程序**：数据库客户端，通过数据库驱动发送SQL指令；

- **数据库服务**：如MySQL/PostgreSQL服务端，接收并执行SQL，返回结果；

- **核心桥梁**：数据库驱动（实现Python与数据库的通信协议），需遵循Python官方的「DB-API 2.0」标准（PEP 249）。

### 1.2 DB-API 2.0标准（核心规范）

DB-API 2.0是Python数据库编程的统一接口标准，所有主流数据库驱动（如`pymysql`/`psycopg2`）都遵循该规范，保证了不同数据库操作语法的一致性。核心组件：

|组件/方法|作用|通用语法示例|
|---|---|---|
|`connect()`|创建数据库连接（返回Connection对象）|`conn = driver.connect(host="127.0.0.1", user="root", password="123456", database="test")`|
|`Connection.cursor()`|创建游标（执行SQL的核心对象）|`cursor = conn.cursor()`|
|`Cursor.execute(sql)`|执行单条SQL语句|`cursor.execute("SELECT * FROM user WHERE id=%s", (1,))`|
|`Cursor.executemany()`|批量执行SQL语句|`cursor.executemany("INSERT INTO user(name) VALUES(%s)", [("张三",), ("李四",)])`|
|`Cursor.fetchone()`|获取查询结果的下一行|`row = cursor.fetchone()`|
|`Cursor.fetchmany(n)`|获取n行结果|`rows = cursor.fetchmany(10)`|
|`Cursor.fetchall()`|获取所有结果|`rows = cursor.fetchall()`|
|`Connection.commit()`|提交事务（DML操作必须执行）|`conn.commit()`|
|`Connection.rollback()`|事务回滚（出错时恢复数据）|`conn.rollback()`|
|`Connection.close()`|关闭连接|`conn.close()`|
|`Cursor.close()`|关闭游标|`cursor.close()`|
### 1.3 核心注意事项（进阶必知）

1. **参数化查询（防SQL注入）**：严禁字符串拼接SQL（如`f"SELECT * FROM user WHERE id={id}"`），必须使用参数化查询（`%s`/`?`为占位符，驱动自动转义）；

2. **事务机制**：DML操作（INSERT/UPDATE/DELETE）默认在事务中，需显式`commit()`生效，出错时`rollback()`回滚；

3. **资源释放**：连接/游标必须显式关闭（或用`with`语句自动释放），避免资源泄漏；

4. **数据类型映射**：Python类型与数据库类型自动映射（如Python `int` ↔ 数据库`INT`，`datetime` ↔ `DATETIME`）。

---

## 模块2：标准库与轻量级数据库实战（SQLite）

SQLite是嵌入式数据库（无独立服务端），Python内置`sqlite3`模块（遵循DB-API 2.0），适合轻量级应用/测试场景，无需额外安装数据库服务。

### 2.1 核心实战：SQLite进阶操作

```Python

import sqlite3
from datetime import datetime

# 1. 连接数据库（不存在则创建），启用行工厂（返回字典格式结果，进阶特性）
def get_db_connection():
    conn = sqlite3.connect("test.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    # 进阶：将游标结果转为字典（默认是元：：组，可读性差）
    conn.row_factory = sqlite3.Row
    return conn

# 2. 初始化表（含索引、约束，进阶设计）
def init_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 创建用户表（含主键、非空、唯一约束，索引优化查询）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status INTEGER NOT NULL DEFAULT 1  -- 1:正常 0:禁用
            )
        """)
        # 创建索引（进阶：优化username查询）
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_username ON user(username)")
        conn.commit()
        print("表初始化成功")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"表初始化失败：{e}")
    finally:
        cursor.close()
        conn.close()

# 3. 进阶CRUD操作（含事务、参数化、批量操作）
class SQLiteDB:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    # 新增（单条+批量）
    def add_user(self, users):
        try:
            # 单条插入
            if isinstance(users, dict):
                self.cursor.execute(
                    "INSERT INTO user(username, password, create_time) VALUES(?, ?, ?)",
                    (users["username"], users["password"], users.get("create_time", datetime.now()))
                )
            # 批量插入（进阶：提升效率）
            elif isinstance(users, list):
                self.cursor.executemany(
                    "INSERT INTO user(username, password, create_time) VALUES(?, ?, ?)",
                    [(u["username"], u["password"], u.get("create_time", datetime.now())) for u in users]
                )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            print(f"插入失败（唯一约束冲突）：{e}")
            return False
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"插入失败：{e}")
            return False

    # 查询（进阶：条件过滤、分页、字典结果）
    def query_user(self, username=None, page=1, page_size=10):
        try:
            sql = "SELECT * FROM user WHERE 1=1"
            params = []
            if username:
                sql += " AND username LIKE ?"
                params.append(f"%{username}%")
            # 分页（进阶：LIMIT/OFFSET）
            sql += " LIMIT ? OFFSET ?"
            params.extend([page_size, (page-1)*page_size])
            
            self.cursor.execute(sql, params)
            # 转为字典列表（Row对象可通过key访问）
            results = [dict(row) for row in self.cursor.fetchall()]
            return results
        except sqlite3.Error as e:
            print(f"查询失败：{e}")
            return []

    # 更新（进阶：条件更新，返回影响行数）
    def update_user(self, user_id, update_data):
        try:
            # 动态构建更新SQL（进阶：避免硬编码）
            update_fields = []
            params = []
            for k, v in update_data.items():
                if k in ["password", "status"]:  # 仅允许更新指定字段
                    update_fields.append(f"{k}=?")
                    params.append(v)
            if not update_fields:
                return 0
            params.append(user_id)
            sql = f"UPDATE user SET {','.join(update_fields)} WHERE id=?"
            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.rowcount  # 返回影响行数
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"更新失败：{e}")
            return 0

    # 关闭资源
    def close(self):
        self.cursor.close()
        self.conn.close()

# 测试代码
if __name__ == "__main__":
    init_table()
    db = SQLiteDB()
    
    # 批量新增
    db.add_user([
        {"username": "zhangsan", "password": "123456"},
        {"username": "lisi", "password": "654321"}
    ])
    
    # 查询（分页+模糊查询）
    users = db.query_user(username="zhang", page=1, page_size=10)
    print("查询结果：", users)
    
    # 更新
    rows_updated = db.update_user(1, {"status": 0})
    print(f"更新行数：{rows_updated}")
    
    db.close()
```

### 2.2 进阶特性：SQLite上下文管理器

```Python
# 进阶：自定义上下文管理器（自动提交/回滚/关闭资源）
class SQLiteContextManager:
    def __enter__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
            print(f"事务回滚：{exc_val}")
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
        # 返回True表示捕获异常（不向外抛出）
        return False

# 使用示例
with SQLiteContextManager() as db:
    db.cursor.execute("INSERT INTO user(username, password) VALUES(?, ?)", ("wangwu", "111111"))
    # 模拟异常（触发回滚）
    # raise ValueError("测试异常")
```

---

## 模块3：关系型数据库实战（MySQL/PostgreSQL）

### 3.1 MySQL进阶编程（pymysql驱动）

#### 3.1.1 环境准备

```shell
# 安装驱动
pip install pymysql
```

#### 3.1.2 核心进阶特性

```sql
-- 创建test数据库，指定字符集为utf8mb4（和代码中charset参数一致）
CREATE DATABASE IF NOT EXISTS test DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```Python
# 导入pymysql库，这是Python操作MySQL数据库的核心驱动库
import pymysql
# 从pymysql的游标模块导入DictCursor（字典游标），查询结果会以字典形式返回（key为字段名，value为字段值）
# 相比默认的元组游标，字典游标更直观，便于通过字段名获取值
from pymysql.cursors import DictCursor  # 进阶：返回字典游标
# 导入contextmanager装饰器，用于实现上下文管理器，简化资源（如数据库连接）的申请和释放
from contextlib import contextmanager

# 进阶：连接池（避免频繁创建/关闭连接，提升性能）
# 从DBUtils库导入PooledDB，用于创建数据库连接池，企业级开发中必备的性能优化手段
from DBUtils.PooledDB import PooledDB

# 1. 创建连接池（企业级必备）
# 连接池的核心作用：复用数据库连接，避免频繁创建/关闭连接带来的性能损耗
# 初始化连接池对象，配置连接池参数和数据库连接信息
pool = PooledDB(
    creator=pymysql,  # 指定使用的数据库驱动为pymysql
    maxconnections=10,  # 连接池允许的最大连接数，超出则等待（根据业务并发量调整）
    mincached=2,  # 连接池初始化时创建的空闲连接数，提前预热连接，减少首次请求延迟
    maxcached=5,  # 连接池最大空闲连接数，避免闲置连接过多占用资源
    host="127.0.0.1",  # 数据库服务器地址（本地测试用127.0.0.1，生产环境替换为真实地址）
    port=3306,  # MySQL数据库默认端口号
    user="root",  # 数据库登录用户名
    password="123456",  # 数据库登录密码（生产环境建议通过环境变量/配置文件管理，避免硬编码）
    database="test",  # 要操作的目标数据库名
    charset="utf8mb4",  # 数据库字符集，utf8mb4兼容emoji等特殊字符，比utf8更全面
    cursorclass=DictCursor  # 设置默认游标类型为字典游标，全局查询结果均为字典格式
)

# 2. 上下文管理器封装连接池（进阶）
# 使用@contextmanager装饰器封装数据库连接的获取、使用、释放逻辑
# 调用者只需通过with语句即可自动管理连接，无需手动处理提交/回滚/关闭
@contextmanager
def get_db_cursor():
    # 从连接池获取一个数据库连接（并非新建连接，而是复用池中的空闲连接）
    conn = pool.connection()  # 从连接池获取连接
    # 创建游标对象，用于执行SQL语句
    cursor = conn.cursor()
    try:
        # 生成器返回游标对象，将控制权交给with语句块中的代码
        yield cursor
        # 若with块中无异常，执行到此处则提交事务，确保数据持久化
        conn.commit()
    except Exception as e:
        # 若with块中执行SQL出现异常，回滚事务，撤销所有未提交的操作，保证数据一致性
        conn.rollback()
        # 抛出异常，让上层代码可以捕获并处理（不吞异常，便于问题排查）
        raise e  # 抛出异常供上层处理
    finally:
        # 无论是否发生异常，最终都会执行finally块，确保资源释放
        cursor.close()  # 关闭游标，释放游标资源
        conn.close()  # 归还连接到连接池（并非真正关闭连接，仅标记为空闲状态）

# 3. 进阶操作：事务、批量插入、存储过程
# 封装MySQL高级操作示例，包含批量插入、存储过程调用、复杂JOIN查询
def mysql_advanced_operations():
    # 批量插入（高效）
    # 使用上下文管理器获取游标，自动管理连接和事务
    with get_db_cursor() as cursor:
        # 禁用自动提交模式（默认autocommit=1，每条SQL执行后自动提交）
        # 批量操作时禁用自动提交，可减少提交次数，大幅提升插入效率
        cursor.execute("SET autocommit=0")
        # 定义批量插入的数据列表，每个元素是一个元组，对应SQL中的占位符
        users = [("zhaoliu", "222222"), ("qianqi", "333333")]
        # executemany批量执行插入语句，比循环调用execute效率高（减少网络交互次数）
        # %s是参数占位符，防止SQL注入，必须使用占位符而非字符串拼接
        cursor.executemany("INSERT INTO user(username, password) VALUES(%s, %s)", users)
        
        # 调用存储过程（进阶）
        # callproc方法用于调用MySQL存储过程，第一个参数是存储过程名，第二个参数是传入的参数元组
        # 示例：调用sp_update_user_status存储过程，传入参数(1, 1)（比如更新id=1的用户状态为1）
        cursor.callproc("sp_update_user_status", (1, 1))  # 存储过程名+参数
        
        # 高级查询：JOIN+分组+排序
        # 执行复杂的多表关联查询，包含左连接、条件筛选、分组、排序
        cursor.execute("""
            SELECT u.id, u.username, o.order_no 
            FROM user u
            LEFT JOIN `order` o ON u.id = o.user_id  # 左连接user和order表，关联条件为用户id
            WHERE u.status = %s  # 筛选状态为1的用户（参数化查询，防止SQL注入）
            GROUP BY u.id  # 按用户id分组，避免重复数据
            ORDER BY u.create_time DESC  # 按用户创建时间降序排列
        """, (1,))  # 传入WHERE条件的参数，元组形式（即使只有一个参数也要加逗号）
        # 获取所有查询结果（列表形式，每个元素是字典，对应一条记录）
        results = cursor.fetchall()
        # 打印查询结果，便于调试查看
        print("JOIN查询结果：", results)

# 4. 异常处理（进阶：细分异常类型）
# 封装精细化的MySQL异常处理示例，区分不同类型的数据库异常，便于精准定位和处理问题
def mysql_exception_handling():
    try:
        # 使用上下文管理器获取游标，执行插入操作
        with get_db_cursor() as cursor:
            # 插入单条数据，参数化查询
            cursor.execute("INSERT INTO user(username, password) VALUES(%s, %s)", ("zhangsan", "123456"))
    # 捕获完整性错误（如主键重复、唯一索引冲突）
    except pymysql.err.IntegrityError as e:
        print(f"主键/唯一约束冲突：{e}")  # 比如username设为唯一索引，重复插入会触发
    # 捕获操作错误（如数据库连接失败、端口错误、数据库宕机）
    except pymysql.err.OperationalError as e:
        print(f"连接/操作错误：{e}")
    # 捕获编程错误（如SQL语法错误、表/字段不存在、存储过程不存在）
    except pymysql.err.ProgrammingError as e:
        print(f"SQL语法错误：{e}")
    # 捕获其他未预判的异常（兜底处理，避免程序崩溃）
    except Exception as e:
        print(f"未知错误：{e}")

# 程序入口（主函数）
# 当该脚本被直接运行时，执行以下代码；若被导入为模块，则不执行
if __name__ == "__main__":
    # 执行高级操作函数
    mysql_advanced_operations()
    # 执行异常处理示例函数
    mysql_exception_handling()
```

### 3.2 PostgreSQL进阶编程（psycopg2驱动）

#### 3.2.1 环境准备

```shell
pip install psycopg2-binary
```

#### 3.2.2 核心进阶特性（与MySQL差异点）

```Python
import psycopg2
import psycopg2.extras  # 进阶：字典游标、批量操作

# 1. 连接（PostgreSQL占位符为%s，与MySQL一致，但类型适配不同）
conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    user="postgres",
    password="123456",
    database="test"
)

# 2. 进阶游标：DictCursor（返回字典）
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# 3. 批量插入（进阶：execute_batch 比 executemany 更高效）
users = [("sunba", "444444"), ("zhoujiu", "555555")]
psycopg2.extras.execute_batch(
    cursor,
    "INSERT INTO user(username, password) VALUES(%s, %s)",
    users,
    page_size=100  # 批量大小（进阶：控制内存占用）
)

# 4. 数组类型操作（PostgreSQL特有，进阶）
cursor.execute("INSERT INTO test_array(id, tags) VALUES(%s, %s)", (1, ["python", "database"]))
cursor.execute("SELECT * FROM test_array WHERE tags @> %s", (["python"],))  # 数组包含查询
result = cursor.fetchone()
print("数组查询结果：", dict(result))

conn.commit()
cursor.close()
conn.close()
```

---

## 模块4：进阶特性：ORM框架（SQLAlchemy）

​	ORM（对象关系映射）是进阶数据库编程的核心，将数据库表映射为Python类，避免手写SQL，提升开发效率和代码可维护性。SQLAlchemy是Python最主流的ORM框架，支持多数据库、灵活的查询构造、事务管理。

### 4.1 环境准备

```Bash
pip install sqlalchemy
```

### 4.2 `SQLAlchemy`进阶实战

> （第一步）：初始化连接池
>
> （第二步）：创建ORM模型基类
>
> （第三步）：创建数据库模型，基于Base基类
>
> （第四步）：初始化数据库表
>
> （第五步）：绑定引擎和会话
>
> （第六步）：上下文管理器的封装
>
> （第七步）：CRUD操作-ORM实现增删查改操作

```Python
# 导入SQLAlchemy核心模块：create_engine用于创建数据库连接引擎，Column/Integer/String等用于定义表字段类型
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Index, func
# 导入declarative_base：创建ORM模型的基类，所有自定义模型都继承该基类
from sqlalchemy.ext.declarative import declarative_base
# 导入sessionmaker（创建会话工厂）、scoped_session（实现线程安全的会话）
from sqlalchemy.orm import sessionmaker, scoped_session
# 导入datetime：处理时间字段
from datetime import datetime
# 导入上下文管理器：封装会话的自动管理逻辑
from contextlib import contextmanager

# 1. 初始化（进阶：连接池配置）
# MySQL连接字符串格式：mysql+pymysql://用户名:密码@主机:端口/数据库名?连接参数
# create_engine：创建数据库连接引擎，SQLAlchemy的核心入口，内置连接池管理
engine = create_engine(
    "mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8mb4",
    pool_size=10,  # 连接池常驻连接数（核心连接数，默认5）
    max_overflow=20,  # 连接池最大溢出连接数（超出pool_size的临时连接，用完回收）
    pool_recycle=3600,  # 连接回收时间（秒），避免MySQL的wait_timeout导致连接失效
    echo=False  # 是否打印生成的SQL语句（开发环境可设为True调试，生产环境必须禁用）
)

# 2. 创建ORM模型基类
# declarative_base()：生成一个基类，所有自定义的ORM模型都需要继承该类
# 基类会自动管理模型与数据库表的映射关系
Base = declarative_base()

# 3. 定义ORM模型（映射数据库user表，进阶：索引、约束）
# 模型类名建议使用大驼峰，对应数据库表名（通过__tablename__指定）
class User(Base):
    __tablename__ = "user"  # 明确指定模型对应的数据库表名（必填）
    
    # 字段定义：Column(字段类型, 约束参数)
    # primary_key=True：主键；autoincrement=True：自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # String(50)：字符串类型（长度50）；nullable=False：非空约束；unique=True：唯一约束；comment：字段注释
    username = Column(String(50), nullable=False, unique=True, comment="用户名")
    password = Column(String(100), nullable=False, comment="密码")
    # DateTime：时间类型；default=datetime.now：默认值为当前时间（插入时自动填充）
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    # default=1：默认值为1；comment说明字段含义（1正常 0禁用）
    status = Column(Integer, default=1, comment="状态：1正常 0禁用")
    
    # 进阶：表级参数（索引、外键约束等）
    __table_args__ = (
        # 创建复合索引：索引名idx_user_status_create_time，包含status和create_time两个字段
        # 复合索引可提升多字段联合查询的效率
        Index("idx_user_status_create_time", "status", "create_time"),
    )
    
    # 进阶：自定义实例方法（方便模型数据转换）
    def to_dict(self):
        """将ORM模型对象转换为字典（便于接口返回、打印等场景）"""
        # 遍历模型对应的表字段，将字段名作为key，字段值作为value
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 4. 创建数据库表（首次执行时触发）
# Base.metadata.create_all(engine)：扫描所有继承Base的模型，自动创建对应的数据库表
# 注意：仅当表不存在时创建，已存在的表不会修改结构（如需修改表结构需用迁移工具如alembic）
Base.metadata.create_all(engine)

# 5. 会话管理（进阶：线程安全的scoped_session）
# sessionmaker(bind=engine)：创建会话工厂，绑定到之前创建的连接引擎
# scoped_session：包装会话工厂，实现线程安全（每个线程独立一个会话，避免并发问题）
# 会话（Session）是ORM操作的核心，所有CRUD都通过会话执行
Session = scoped_session(sessionmaker(bind=engine))

# 6. 上下文管理器封装会话（自动提交/回滚/关闭）
# 用@contextmanager装饰器封装会话的生命周期，调用者无需手动处理提交/回滚/关闭
@contextmanager
def get_session():
    # 从线程安全的会话工厂获取一个会话实例
    session = Session()
    try:
        # 生成器返回会话对象，将控制权交给with语句块中的代码
        yield session
        # 若with块中无异常，提交事务（持久化数据）
        session.commit()
    except Exception as e:
        # 若出现异常，回滚事务（撤销所有未提交的操作）
        session.rollback()
        # 抛出异常供上层处理（不吞异常，便于问题排查）
        raise e
    finally:
        # 无论是否异常，最终关闭会话（释放连接，归还到连接池）
        session.close()

# 7. 进阶CRUD操作（ORM风格，无需手写SQL）
def orm_advanced_operations():
    # ========== 新增操作 ==========
    with get_session() as session:
        # 单条新增：创建User模型实例，通过session.add()添加
        user1 = User(username="orm_zhangsan", password="123456")
        session.add(user1)
        
        # 批量新增：创建多个模型实例，通过session.add_all()批量添加（效率高于多次add）
        user2 = User(username="orm_lisi", password="654321")
        user3 = User(username="orm_wangwu", password="111111")
        session.add_all([user2, user3])
    
    # ========== 查询操作（进阶：过滤、分页、排序、聚合） ==========
    with get_session() as session:
        # 构建查询：session.query(模型类) 相当于 SELECT * FROM 表
        # filter()：添加查询条件（支持多条件链式调用）
        # - User.username.like("%orm%")：模糊查询用户名包含"orm"的记录
        # - User.status == 1：筛选状态为1的用户
        # order_by(User.create_time.desc())：按创建时间降序排列
        # offset(0)：跳过前0条（分页起始位置）；limit(10)：最多返回10条（分页大小）
        # all()：获取所有符合条件的结果（返回模型实例列表）
        users = session.query(User).filter(
            User.username.like("%orm%"),
            User.status == 1
        ).order_by(User.create_time.desc()).offset(0).limit(10).all()
        # 调用to_dict()将模型实例转为字典，方便打印查看
        print("ORM查询结果：", [u.to_dict() for u in users])
        
        # 聚合查询：统计符合条件的记录数
        # func.count(User.id)：相当于SQL中的COUNT(id)
        # scalar()：获取聚合查询的单个结果（替代all()，更高效）
        count = session.query(func.count(User.id)).filter(User.status == 1).scalar()
        print("正常用户数：", count)
        
        # 关联查询示例（假设有Order表，需先定义Order模型）
        # join(Order, User.id == Order.user_id)：相当于SQL中的INNER JOIN
        # users_with_orders = session.query(User, Order).join(Order, User.id == Order.user_id).all()
    
    # ========== 更新操作（进阶：批量更新） ==========
    with get_session() as session:
        # 单条更新：先查询到目标实例，修改属性后通过session.merge()更新
        user = session.query(User).filter(User.username == "orm_zhangsan").first()  # first()获取第一条结果
        if user:  # 判空，避免None对象操作报错
            user.status = 0  # 修改实例属性
            session.merge(user)  # 合并更新（将内存中的修改同步到数据库）
        
        # 批量更新：直接通过查询条件更新，无需查询实例（效率更高）
        # update({"status": 1})：相当于SQL中的UPDATE user SET status=1 WHERE username LIKE '%orm%'
        session.query(User).filter(User.username.like("%orm%")).update({"status": 1})
    
    # ========== 删除操作（进阶：软删除替代物理删除） ==========
    with get_session() as session:
        # 软删除：不执行DELETE语句，而是更新status字段为0（保留数据，便于恢复/审计）
        # 物理删除可用：session.delete(user) 或 session.query(User).filter(User.id == 1).delete()
        # 生产环境优先使用软删除，避免数据丢失
        session.query(User).filter(User.id == 1).update({"status": 0})

# 程序入口：直接运行脚本时执行ORM高级操作
if __name__ == "__main__":
    orm_advanced_operations()
```

---

## 模块5：异步数据库编程（进阶：asyncio）

Python 3.7+支持异步数据库编程，适合高并发场景（如Web框架FastAPI），主流异步驱动：

- MySQL：`aiomysql`

- PostgreSQL：`asyncpg`

- SQLAlchemy 2.0+：支持异步ORM

### 5.1 异步MySQL实战（aiomysql）

```Bash
pip install aiomysql
```

```Python

import asyncio
import aiomysql

# 进阶：异步连接池
async def create_async_pool():
    pool = await aiomysql.create_pool(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123456",
        db="test",
        charset="utf8mb4",
        maxsize=10,  # 连接池最大连接数
        minsize=2    # 最小空闲连接数
    )
    return pool

# 异步CRUD
async def async_mysql_operations():
    pool = await create_async_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # 新增
            await cur.execute("INSERT INTO user(username, password) VALUES(%s, %s)", ("async_zhang", "123456"))
            await conn.commit()
            
            # 查询
            await cur.execute("SELECT * FROM user WHERE username LIKE %s", ("%async%",))
            results = await cur.fetchall()
            print("异步查询结果：", results)
    
    pool.close()
    await pool.wait_closed()

# 运行异步函数
if __name__ == "__main__":
    asyncio.run(async_mysql_operations())
```

---

## 模块6：数据库编程最佳实践（进阶）

### 6.1 核心最佳实践

1. **连接池必用**：避免频繁创建/关闭连接（性能损耗），生产环境必须使用连接池（DBUtils/PooledDB/SQLAlchemy连接池）；

2. **参数化查询**：杜绝SQL注入（所有用户输入必须通过占位符传递）；

3. **事务管理**：DML操作必须包裹在事务中，出错时回滚，避免数据不一致；

4. **资源自动释放**：使用`with`语句/上下文管理器自动关闭连接/游标；

5. **软删除替代物理删除**：通过`status`字段标记删除，保留数据溯源能力；

6. **索引优化**：为高频查询字段创建索引（避免全表扫描），但避免过度索引（影响写入性能）；

7. **分页查询**：大数据量查询必须分页（LIMIT/OFFSET），避免内存溢出；

8. **异常细分处理**：针对不同异常类型（约束冲突/连接错误/SQL语法错误）做差异化处理；

9. **日志记录**：记录所有执行的SQL（生产环境脱敏），便于问题排查；

10. **异步编程**：高并发场景（如API服务）使用异步数据库驱动，提升吞吐量。

### 6.2 性能优化技巧（进阶）

1. **批量操作**：使用`executemany()`/`execute_batch()`替代循环单条插入；

2. **禁用自动提交**：批量操作时禁用自动提交（`SET autocommit=0`），减少事务开销；

3. **游标类型选择**：大结果集使用`SSCursor`（服务器端游标），避免加载所有数据到内存；

4. **查询优化**：避免`SELECT *`，只查询需要的字段；使用`EXPLAIN`分析SQL执行计划；

5. **连接池参数调优**：根据业务QPS调整`pool_size`/`max_overflow`，避免连接数过多/过少。

---

### 总结

1. **核心底层**：Python数据库编程遵循DB-API 2.0标准，核心是「连接-游标-执行SQL-提交/回滚-关闭资源」；

2. **实战分层**：

    - 轻量场景：SQLite（内置`sqlite3`，无需服务端）；

    - 生产场景：MySQL/PostgreSQL（`pymysql`/`psycopg2`+连接池）；

    - 高效开发：ORM框架（SQLAlchemy，避免手写SQL）；

    - 高并发场景：异步编程（`aiomysql`/`asyncpg`）；

3. **进阶特性**：连接池、事务管理、参数化查询、上下文管理器、ORM、异步编程是企业级开发的核心；

4. **最佳实践**：安全（防注入）、性能（连接池/批量操作）、可靠性（事务/异常处理）是数据库编程的三大核心原则。

这些内容覆盖了Python数据库编程从底层到进阶的全维度知识，符合工业界生产环境的使用标准，是Python进阶语法中数据库板块的核心内容。