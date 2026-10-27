import traceback


# 进阶-2：异常链
# 显式异常链
# raise ... from ... 来指明显式异常
def load_config():
    try:
        with open("config.ini", mode="r") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError("配置文件加载失败") from e


try:
    load_config()
except RuntimeError as e:
    print(f"[Error]:{e}")
    traceback.print_exc()


# 隐式异常链
def process_data(data):
    try:
        return int(data)
    except ValueError:
        raise RuntimeError("数据处理失败")


try:
    process_data("abc")
except RuntimeError as e:
    print(f"=== [Error]:{e} ===")
    traceback.print_exc()
