# （1）初始化连接池对象
from sqlalchemy import create_engine

engine = create_engine(
    url="mysql+pymysql://root:123456789@127.0.0.1:3306/test?charset=utf8mb4",
    pool_size=10,
    # max_overflow=20,
    pool_recycle=3600,
    echo=False,
)
print(engine, type(engine))

# （2）创建ORM模型基类

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# （3）创建数据库模型，基于Base基类
from sqlalchemy import Column, String, Integer, DateTime


class SuperBase(Base):
    __tablename__ = "SuperBase"
    super_base_id = Column(Integer, primary_key=True, autoincrement=True)
    super_base_number = Column(String(50), nullable=False)
    super_base_name = Column(
        String(50), nullable=False, unique=False, comment="项目名称"
    )


# （4）数据库初始化
def init_table():
    try:
        Base.metadata.create_all(engine)
        return True
    except Exception as e:
        print(f"[Error]:{e}")
        raise e


if __name__ == "__main__":
    init_table()
