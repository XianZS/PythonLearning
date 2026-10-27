# 进阶-3：与unittest框架的集成
import unittest
import doctest
import math_functions


def load_tests(loader, tests, ignore):
    """
    加载doctest测试用例，到unittest测试套件之中
    """
    # 添加函数级别的
    tests.addTests(doctest.DocTestSuite(math_functions))
    # 添加文件级别的
    tests.addTests(doctest.DocFileSuite("math_functions.txt"))
    return tests


# D:\code\py_item\PythonLearning\python_stdlib_learning\8_debug_test\doctest_learn\math_functions.txt
# Doctest: math_functions.txt ... ok
#
# ----------------------------------------------------------------------
# Ran 1 test in 0.001s
#
# OK

if __name__ == "__main__":
    unittest.main()
