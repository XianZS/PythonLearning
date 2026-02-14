import sqlite3


def get_db_connection():
    conn = sqlite3.connect(database="test.db")
    return conn


def init_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql_text = """
        create table if not exists user (
            user_name text not null unique,
            user_password text not null
        );
        """
        cursor.execute(sql_text)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    init_table()

