# （导入）
# 导入pymysql
import pymysql

# 连接池对象的创建：with+DBUtils
# 上下文管理器
from contextlib import contextmanager

# 连接池对象
from dbutils.pooled_db import PooledDB

# 导入DictCursor
from pymysql.cursors import DictCursor

# 创建数据库连接池
pool = PooledDB(
    # （使用什么连接？）指定数据库连接驱动
    creator=pymysql,
    # （池子有多大？）最多可以连接多少个对象
    maxconnections=10,
    # （如何实现打开即用？）热加载连接对象
    mincached=2,
    # （如何管理空闲连接？）指定最大空闲连接数
    maxcached=5,
    # （连到哪里？）指定host，以及port
    host="127.0.0.1",
    port=3306,
    # （如何连接？）指定user_name，以及user_password
    user="root",
    password="123456789",
    # （连接什么？）指定连接的数据库，需要保证被连接的数据库对象存在
    database="test",
    charset="utf8mb4",
    # （得到什么？）指定返回值类型，设置默认游标类型为字典类型，全局查询的结果会变为字典格式
    cursorclass=DictCursor,
)


# 使用上下文管理器的作用
# 自动实现：事务的提交、异常出现时的数据库回滚、异常的捕捉
@contextmanager
def get_mysql_db():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        yield cursor
        # 设置自动提交事务
        conn.commit()
    except Exception as e:
        print(e)
        # 设置数据库自动回滚
        conn.rollback()
        raise e
    finally:
        # 实现数据库对象的自动管理
        cursor.close()
        conn.close()


def create_table():
    """
    通过上下文管理器和连接池对象
    实现创建数据库表
    不需要关心：游标在什么时候被创建？事务在什么时候被提交？
    只需要关心：执行语句
    """
    with get_mysql_db() as db:
        ct_stu = """
            create table stu(
                stu_id      int     primary key,
                stu_name    text    not null,
                stu_age     int     not null    default 18,
                stu_address text    not null
            )
        """
        db.execute(ct_stu)


def insert_data():
    """
    插入数据
    """
    try:
        with get_mysql_db() as db:
            db.execute("set autocommit = 0")
            id_stu = """
                insert into stu
                (stu_id,stu_name,stu_age,stu_address)
                values
                (%s,%s,%s,%s)
            """
            datas = []
            names = ["aom", "som", "dom"]
            ages = [12, 16, 20]
            address = ["A市", "B市", "C市"]
            ids = [4, 5, 6]
            for index in range(1, len(names) + 1):
                datas.append(
                    (
                        10000 + ids[index - 1],
                        names[index - 1],
                        ages[index - 1],
                        address[index - 1],
                    )
                )
            print(f"datas:{datas}")
            db.executemany(id_stu, datas)
    except pymysql.err.IntegrityError as e:
        print(f"[{e}]:主键冲突错误")
    except pymysql.err.OperationalError as e:
        print(f"[{e}]:连接/缓冲池错误")
    except pymysql.err.ProgrammingError as e:
        print(f"[{e}]:SQL语法错误")
    except Exception as e:
        print(f"[{e}]:其它错误")


if __name__ == "__main__":
    # create_table()
    insert_data()

