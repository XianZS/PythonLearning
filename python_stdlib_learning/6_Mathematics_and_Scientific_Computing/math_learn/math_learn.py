"""
math 标准库学习
"""

from enum import Flag
import math

# 基础-1：数学常量
# Π：3.14 math.pi
# e：2.7 无穷大 非数字
print(f"[Π]:{math.pi}")
print(f"[e]:{math.e}")
print(f"[2Π]:{math.tau}")
print(f"[无穷大]:{math.inf}")
print(f"[非数字]:{math.nan}")
# 基础-2：基础数值运算
number = 3.14
print(f"[向上取整]:{math.ceil(number)}")
print(f"[向下取整]:{math.floor(number)}")
print(f"[截断整数部分]:{math.trunc(number)}")
number1 = -43
print(f"[绝对值]:{math.fabs(number1)}")
a, b = 15, 4
# 15%4=3
print(f"[取模运算]:{math.fmod(a, b)}")
print(f"[x的y次方]:{math.pow(a, b)}")
print(f"[以10为底的对数]:{math.log10(a)}")
print(f"[以2为底的对数]:{math.log2(a)}")
# 基础-3：三角函数的使用，弧度制
angle_deg = 30
angle_rad = math.radians(angle_deg)
print(f"[弧度]:{angle_rad}")
print(f"[math.sin]:{math.sin(angle_rad)}")
print(f"[math.cos]:{math.cos(angle_rad)}")
print(f"[math.tan]:{math.tan(angle_rad)}")
# 基础-4：双曲函数
# 双曲正弦、双曲余弦、双曲正切、反双曲正弦、反双曲余弦、反双曲正切函数
x = 1
print(f"[双曲正弦]:{math.sinh(x)}")
print(f"[双曲余弦]:{math.cosh(x)}")
print(f"[双曲正切]:{math.tanh(x)}")
# 进阶-1：特殊函数的使用
print(f"[误差函数]:{math.erf(1 / math.sqrt(2))}")
# print(f"[补误差函数]:{math.erfc()}")
gamma_number = 100
print(f"[伽马函数]:{math.gamma(gamma_number)}")
print(f"[伽马函数的自然对数]:{math.lgamma(gamma_number)}")
fact_number = 5
print(f"[阶乘]:{math.factorial(fact_number)}")
a, b = 5, 2
print(f"[组合数]:{math.comb(a, b)}")
print(f"[排列数]:{math.perm(a, b)}")
c, d = 18, 24
print(f"[最大公约数]:{math.gcd(c, d)}")
print(f"[最小公倍数]:{math.lcm(c, d)}")
# 进阶-2：浮点数处理和工具函数
# 判断是否是无穷大
num1, num2, num3 = 10, math.inf, -math.inf


def judge(*cho) -> list:
    dnums = [False for _ in range(len(cho))]
    for index in range(len(cho)):
        if math.isinf(cho[index]):
            dnums[index] = True
        else:
            dnums[index] = False
    return dnums


res = judge(num1, num2, num3)
print(res)
# 判断数字是不是NAN
num4 = math.nan


def judge_nan(*nums) -> list:
    dnums = [False for _ in range(len(nums))]
    for index in range(len(nums)):
        if math.isnan(nums[index]):
            dnums[index] = True
        else:
            dnums[index] = False
    return dnums


res_nan = judge_nan(num1, num2, num3, num4)
print(res_nan)
# 是不是有限数字 （不包含无穷和非数字） math.isfinite(number)
# 两个浮点数是否接近 （避免精度误差的问题） math.isclose(number1,number2)


# === 实战案例：几何计算工具箱 ===
# - 计算两点之间的欧几里得距离
# - 计算⚪的面积和周长
# - 用海伦公式计算三角形的面积
# - 两点相对于原点的夹角
class Toolkit:
    @staticmethod
    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """计算两点之间的欧几里得距离"""
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def circle(radius: float) -> tuple[float, float]:
        """计算圆的面积和周长"""
        if radius < 0:
            raise ValueError("半径不可以为负数")
        else:
            area = math.pi * radius**2
            perimeter = 2 * math.pi * radius
            return area, perimeter

    @staticmethod
    def make_area(a: float, b: float, c: float) -> float:
        """用海伦公式计算三角形面积，a、b、c为三角形的三边"""
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("边长必须为正数")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("两边之和必须要大于第三边")
        else:
            s = (a + b + c) / 2
            return math.sqrt(s * (s - a) * (s - b) * (s - c))

    @staticmethod
    def angle_between(
        x1: float, y1: float, x2: float, y2: float
    ) -> tuple[float, float]:
        """计算两点之间的相对于原点夹角，返回（弧度，角度）"""
        a1 = math.atan2(y1, x1)
        a2 = math.atan2(y2, x2)
        a_rad = a2 - a1
        # 归一化到[-Π,Π]
        a_r = math.atan2(math.sin(a_rad), math.cos(a_rad))
        angle_deg = math.degrees(a_rad)
        return a_r, angle_deg


if __name__ == "__main__":
    toolkit = Toolkit()
    # 计算两点之间的距离
    print(toolkit.distance(0, 0, 3, 4))
    # 计算原的面积和周长
    radius = 5
    area, perimeter = toolkit.circle(radius)
    print(f"【面积】:{area},周长:{perimeter}")
