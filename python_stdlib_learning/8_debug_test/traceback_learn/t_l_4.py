import traceback
import sys


# 进阶-4：自定义异常格式
# 语法规范：通过tracebackexception类来完全自定义异常格式
def custom_print_exception(exc_type, exc_value, exc_traceback):
    """自定义异常打印函数"""
    print("=" * 10)
    print(f"[异常类型]:{exc_type.__name__}")
    print(f"[异常消息]:{exc_value}")
    print("=" * 10)
    print("堆栈跟踪:")
    tb_exc = traceback.TracebackException(exc_type, exc_value, exc_traceback)
    for frame in tb_exc.stack:
        print(f">>>[文件]:{frame.filename};[行]:{frame.lineno};[函数]:{frame.name}")
        print(f">>>[代码]:{frame.line}")
    print("=" * 10)


# 替换默认的异常处理函数
sys.excepthook = custom_print_exception


# 测试异常
def func_a():
    func_b()


def func_b():
    raise ValueError("自定义异常测试函数")


func_a()
