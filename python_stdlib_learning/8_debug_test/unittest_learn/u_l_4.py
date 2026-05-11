# 进阶-4：异常测试
import unittest


def div(a, b):
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b


class TestDivide(unittest.TestCase):
    # 方式-1：上下文管理器
    def test_div_by_zero_context(self):
        with self.assertRaises(ZeroDivisionError) as cm:
            div(10, 0)
            # 验证异常信息
            self.assertEqual(str(cm.exception), "除数不能为零")

    # 方式-2：装饰器
    @unittest.expectedFailure
    def test_divide_by_zero_decorator(self):
        div(10, 0)


if __name__ == "__main__":
    unittest.main()
