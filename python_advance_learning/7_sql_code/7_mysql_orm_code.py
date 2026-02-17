# 创建会话引擎
from sqlalchemy import create_engine

# 导入自定义表字段类型
from sqlalchemy import Column, Integer, String, DateTime

# 导入ORM基类，所有的ORM数据库模型都必须继承该基类
from sqlalchemy.ext.declarative import declarative_base

# 导入sessionmaker（创建会话工厂），scoped_session（实现线程安全的会话）
from sqlalchemy.orm import sessionmaker, scoped_session

# 导入时间处理库
from datetime import datetime

# 导入上下文管理器，封装会话的自动管理逻辑
from contextlib import contextmanager


# （第一步）初始化连接池对象
engine = create_engine(
    url="mysql+pymysql://root:123456789@127.0.0.1:3306/test?charset=utf8mb4",
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=False,
)


# （第二步）创建ORM模型基类
Base = declarative_base()


# （第三步）创建数据库模型，基于BASE基类
class People(Base):
    __tablename__ = "people"
    p_id = Column(Integer, primary_key=True, autoincrement=True)
    p_name = Column(String(50), nullable=False, unique=False, comment="用户名")
    p_age = Column(Integer, nullable=True, unique=False, comment="年龄")
    create_time = Column(DateTime, default=datetime.now(), comment="数据创建时间")


# （第四步）创建数据库表
def init_table():
    try:
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(f"[ERROR]:{e}")
        return False


# （第五步）会话管理
# 绑定引擎和会话，确保线程的安全性
session_orm = scoped_session(sessionmaker(bind=engine))


# （第六步）上下文管理器的封装
@contextmanager
def get_session():
    session = session_orm()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[Error]:{e}")
        raise e
    finally:
        session.close()


# （第七步）进阶CRUD操作
def orm_advanced_operations():
    with get_session() as session:
        people_1 = People()


if __name__ == "__main__":
    print(type(declarative_base))
    print(type(Base))
    init_table()
