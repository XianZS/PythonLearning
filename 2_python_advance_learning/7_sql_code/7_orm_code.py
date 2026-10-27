# （第一步）初始化连接池对象
# 【解读】：在sqlalchemy之中，通过“引擎”对象，初始化ORM映射连接池
from sqlalchemy import create_engine, update
from sqlalchemy.sql.functions import session_user


# 创建引擎对象engine
engine = create_engine(
    # 【URL的设置】："数据库对象+连接桥梁://用户名:密码@IP:端口/数据库名?charset=utf8mb4"
    url="mysql+pymysql://root:123456789@127.0.0.1:3306/test?charset=utf8mb4",
    # 【核心连接数】：连接池常驻连接对象数量
    pool_size=10,
    # 【最大溢出数量】：达到该阈值之后，会自动销毁掉不再使用的连接
    max_overflow=20,
    # 【最大延迟回收时间】：假设连接远程数据库，延迟的最大数值
    pool_recycle=3600,
    # 【关闭自动输出】：开发环境和生产环境，关闭ORM框架翻译SQL语句之后的自动输出
    echo=False,
)

# （第二步）创建ORM基类
# 【解读】：ORM框架的作用：将你的CRUD的编程语言，翻译成SQL查询语句。
from sqlalchemy.ext.declarative import declarative_base

# 成功创建了BASEMODEL基类
BaseModel = declarative_base()

# （第三步）创建数据库模型，基类BASEMODEL基类
# 数据库表 === [ORM] === 类
from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, Index, func


# 类（数据库表）
class User(BaseModel):
    # 必须存在的私有属性 __tablename__
    __tablename__ = "User"
    # 字段名=Column(字段类型，其他的参数按照键值对的形式传参)
    user_id = Column(
        Integer, primary_key=True, nullable=False, unique=True, comment="用户编号"
    )
    user_name = Column(String(50), nullable=False, comment="用户姓名")
    user_address = Column(String(50), nullable=True, comment="用户地址")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_address": self.user_address,
        }


class Admin(BaseModel):
    __tablename__ = "Admin"
    admin_id = Column(
        Integer, nullable=False, unique=True, primary_key=True, comment="管理员编号"
    )
    admin = Column(String(50), nullable=False, comment="管理员账号")
    password = Column(String(50), nullable=False, comment="管理员密码")

    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "admin": self.admin,
            "password": self.password,
        }


# （第四步）初始化数据库表
# 【解读】：自动查看基类模型BaseModel对象所绑定的数据库表（类），然后进行数据库的迁移。
def init_table():
    try:
        BaseModel.metadata.create_all(engine)
        return True
    except Exception as e:
        print(e)
        return False


# （第五步）绑定引擎和会话
from sqlalchemy.orm import scoped_session, session, sessionmaker

# scoped_session:包装会话工厂，实现线程安全
# sessionmaker:创建会话工厂，将会话工厂绑定到之前的连接引擎
SessionORM = scoped_session(sessionmaker(bind=engine))

# （第六步）上下文管理器的封装
# 实现内容：自动提交/回滚事务/自动关闭
from contextlib import contextmanager


# 生成器对象 get_session_orm
@contextmanager
def get_session_orm():
    # 先需要从会话工厂SessionORM获取一个SessionORM的实例对象
    session_orm = SessionORM()
    try:
        yield session_orm  # 通过yeild关键字，创建生成器对象
        session_orm.commit()  # 自动提交事务
    except Exception as e:
        session_orm.rollback()
        raise e
    finally:
        session_orm.close()


# （第七步）进阶CRUD操作，ORM实现增删查改的操作
# 非ORM框架：使用原生的SQL语句
# ORM框架：使用编程查询语句


# 插入数据
def orm_insert_code():
    # 单条插入
    with get_session_orm() as db:
        user1 = User(user_id=10003, user_name="jom", user_address="A城市")
        db.add(user1)
        # 按照引擎所绑定的BASEMODEL之中的所有数据库表模型，
        # 它首先会进行自动匹配，
        # 然后找到对应的数据库表
        # 最后将user1这条数据插入其中

    # 多条插入
    with get_session_orm() as db:
        datas = []
        for x in range(10001, 10004):
            datas.append(
                Admin(admin_id=x, admin="admin" + str(x), password="admin" + str(x))
            )
        print(datas)
        db.add_all(datas)


# 查找
def orm_select_code():
    with get_session_orm() as db:
        # db.query(表对应的BASEMODEL数据模型).filter().all()
        # db.query(表对应的BASEMODEL数据模型).filter().order_by(排序方式).offset(0).all()
        # select * from User where user_id>10001
        res = db.query(User).filter(User.user_id > 10001).all()
        print(res)
        datas = []
        for cho in res:
            datas.append(cho.to_dict())
        print(datas)


# 修改
# 首先从数据库之中读取你所要修改的数据对象
# 然后在本地的缓存之中进行修改
# 最后将缓存之中的修改，合并merge到你的数据库之中
def orm_update_code():
    with get_session_orm() as db:
        # 得到我所要修改的数据对象
        update_obj = db.query(Admin).filter(Admin.admin_id == 10002).first()
        print(update_obj)
        if update_obj:
            # 在本地缓存之中修改它
            update_obj.password = "3135"  # type:ignore
            # 将本地缓存之中的修改，合并到数据库之中
            db.merge(update_obj)
            return True
        else:
            return False


# 删除
# 软删除：通过给数据对象设置状态字段，想要删除时，只需要将数据对象的状态字段设置为0
# 物理删除：直接删除
def orm_delete_code():
    with get_session_orm() as db:
        db.query(Admin).filter(Admin.admin_id == 10003).delete()


if __name__ == "__main__":
    judge = init_table()
    print(f"[INFO]:{judge}")

    try:
        orm_insert_code()
    except Exception as e:
        print(e)

    try:
        orm_select_code()
    except Exception as e:
        print(e)

    try:
        orm_update_code()
    except Exception as e:
        print(e)

    try:
        orm_delete_code()
    except Exception as e:
        print(e)

