# 进阶-1：测试套件和测试组织
# 逻辑组：测试用例的组合
import unittest


class TestMathOper(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 3, 5)

    def test_sub(self):
        self.assertEqual(2 - 3, -1)


class TestStringOper(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("hello".upper(), "HELLO")

    def test_isupper(self):
        self.assertTrue("HELLO".isupper())
        self.assertFalse("Hello".isupper())


def create_test_suite():
    """
    创建测试套件
    """
    suite = unittest.TestSuite()
    # 添加单个测试方法
    suite.addTest(TestMathOper("test_add"))
    # 添加单个测试类
    math_test = unittest.TestLoader().loadTestsFromTestCase(TestMathOper)
    string_test = unittest.TestLoader().loadTestsFromTestCase(TestStringOper)
    suite.addTests([math_test, string_test])
    return suite


if __name__ == "__main__":
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    # 语法规范：
    # runner.run(测试套件对象)
    runner.run(suite)
