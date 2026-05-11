# 进阶-2：跳过测试与预期失败
# unittest 提供了装饰器来控制测试的执行
# @unittest.skip() 跳过
# @unittest.skipIf() 条件满足时跳过
# @unittest.skipUnless() 条件不满足时跳过
# @unittest.exceptedFailure() 预期测试失败
import unittest
import sys


class TestSkipExamples(unittest.TestCase):
    @unittest.skip("跳过这个测试")
    def test_skip(self):
        self.fail("这个测试不会被执行")

    @unittest.skipIf(sys.version_info < (3, 14), "需要python3.14及其以上版本")
    def test_skip_if(self):
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_expected_failure(self):
        self.assertEqual(-1, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
