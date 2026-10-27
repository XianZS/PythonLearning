"""
unittest 标准库学习
"""

import unittest


def setUpModule():
    """unittest模型执行前调用一次"""
    print("模块执行前调用一次")
    global config
    config = {"debug": True}


def tearDownModule():
    print("模块执行后调用一次")
    global config
    del config


class TestConfig(unittest.TestCase):
    def test_debug_mode(self):
        self.assertTrue(config["debug"])


# 基础-1：基本使用
def add(a, b):
    """
    等待测试的加法函数
    """
    result = a + b
    return result


class TestAddFunction(unittest.TestCase):
    """
    测试add函数的测试类
    """

    def test_add_positive_numbers(self):
        """测试两个正数相加"""
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_add_zero(self):
        """测试与0相加"""
        result = add(0, 5)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        result = add(-2, -3)
        self.assertEqual(result, -5)


# 基础-2：基本断言方法
# assertEqual(a,b) 验证 a==b
# assertNotEqual(a,b) 验证 a!=b
# assertTrue(x) 验证 x==True
# assertFalse(x) 验证 x==False
# assertIs(a,b) 验证 a is b
# assertIsNone(x) 验证 x is None
# === python 3.14 最新特性 ===
# self.assertSequenceEqual(strict=True)
# 使用strict=True，同时比较内容和类型


# 基础-3：测试固件
# 测试执行前后的准备和清理工作，确保测试环境的独立性
# 语法规范：
# setUp() tearDown() setUpClass() tearDownClass() setUpModule() tearDownModule()
# 方法级固件：每个测试方法执行前后调用
# 类级固件：整个测试类执行前后调用
# 模块级固件：整个模块执行前后分别调用一次
class TestAddFunction_1(unittest.TestCase):
    """
    测试add函数的测试类
    """

    @classmethod
    def setUpClass(cls):
        """测试类执行前调用"""
        print("测试类执行前调用")

    @classmethod
    def tearDownClass(cls):
        print("测试类执行后调用")

    # def setUp(self):
    #     # 在每个测试方法执行前调用
    #     print("准备测试环境")
    #
    # def tearDown(self):
    #     print("清理测试环境")

    def test_add_positive_numbers(self):
        """测试两个正数相加"""
        print("=== 正在测试 ===")
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_add_zero(self):
        """测试与0相加"""
        print("=== 正在测试 ===")
        result = add(0, 5)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        print("=== 正在测试 ===")
        result = add(-2, -3)
        self.assertEqual(result, -5)


# 基础-4：运行测试
# 代码内测试：直接写就行
# 命令行测试：python -m unittest python_file.MyTestClass.function


if __name__ == "__main__":
    unittest.main()
