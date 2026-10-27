# 进阶-3：参数化测试
import unittest


# 上下文管理器来进行参数化测试
# subtest 和 with 搭配使用
def is_even(n):
    # 判断数字n是不是偶数
    return n % 2 == 0


class TestEven(unittest.TestCase):
    def test_is_even(self):
        test_cases = [
            (2, True, "偶数"),
            (3, False, "奇数"),
            (0, True, "零"),
            (-4, True, "负偶数"),
            (-5, False, "负奇数"),
        ]
        for n, expected, des in test_cases:
            with self.subTest(n=n, description=des):
                self.assertEqual(is_even(n), expected)


# 第三方库
# parameterized 第三方库


if __name__ == "__main__":
    unittest.main()
