import sqlite3


# （第一步）创建连接connect返回对象
def get_connect():
    conn = sqlite3.connect(database="sqlite_test.db")
    return conn


# （第二步）创建数据库表
def init_table():
    # 得到连接对象和游标对象
    conn = get_connect()
    cursor = conn.cursor()
    print(conn, cursor)
    try:
        sql_text = """
        create table if not exists user(
            user_id     int     primary key     not null,
            user_name   text    not null,
            user_password   text    not null,
            data_insert_time    datetime    not null
        )
        """
        # 执行sql语句
        cursor.execute(sql_text)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# （第三步）实现数据库的增删查改操作
class SQLMake:
    def __init__(self):
        self.conn = get_connect()
        self.cursor = self.conn.cursor()

    # [insert]实现数据的插入操作
    def insert_data(self, data):
        try:
            # 使用问好代替的好处？
            # 避免了字符串的拼接，防止了sql注入
            sql_text = "insert into user (user_id,user_name,user_password,data_insert_time) values (?,?,?,?)"
            self.cursor.execute(
                sql_text,
                (
                    data["user_id"],
                    data["user_name"],
                    data["user_password"],
                    data["data_insert_time"],
                ),
            )
            self.conn.commit()
            print("=== 数据插入成功 ===")
        except sqlite3.Error as e:
            print(e)

    def select_data(self):
        try:
            sql_text = "select * from user where user_id>4"
            self.cursor.execute(sql_text)
            res = self.cursor.fetchall()
            return res
        except sqlite3.Error as e:
            print(e)

    def delete_data(self):
        try:
            sql_text = "delete from user where user_id=8"
            self.cursor.execute(sql_text)
            self.conn.commit()
        except Exception as e:
            print(e)

    def update_data(self):
        try:
            sql_text = "update user set user_name='admin',user_password='admin123' where user_id=1"
            self.cursor.execute(sql_text)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)


if __name__ == "__main__":
    _ = get_connect()
    init_table()
    su = SQLMake()
    try:
        from datetime import datetime

        names = ["aom", "som", "dom", "fom", "gom", "hom", "jom", "kom", "lom"]
        for x in range(1, 10):
            su.insert_data(
                {
                    "user_id": x,
                    "user_name": names[x - 1],
                    "user_password": names[x - 1] + "123",
                    "data_insert_time": datetime.now(),
                }
            )
    except Exception as e:
        print(e)

    try:
        res_datas = su.select_data()
        for cho in res_datas:  # type:ignore
            for child in cho:
                print(f"{child} ", end="")
            print()
    except Exception as e:
        print(e)

    try:
        del_data = su.delete_data()
        print(del_data)
    except Exception as e:
        print(e)

    try:
        update_date = su.update_data()
        print(update_date)
    except Exception as e:
        print(e)
