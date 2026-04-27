"""
cmath标准库学习
"""

import cmath
import math

# 基础-1：复数的创建和基本属性
# a+bj
z1 = 2 + 4j
print(f"[z1]:{z1},[type]:{type(z1)}")
z2 = complex(3, 4)
print(f"[z2]:{z2}")
print(f"[z2实部]:{z2.real},[z2虚部]:{z2.imag}")
# 基础-2：数学常量
# 圆周率：pi
# 自然对数底数：e
# 正无穷虚数：cmath.infj
# 非数字虚数：cmath.nanj
print(cmath.infj)
print(cmath.nanj)
# 基础-3：极坐标和直角坐标系之间的转换
# 转换为极坐标系
r, phi = cmath.polar(z2)
print(f"[r]:{r},[phi]:{phi}")
# 转换为直角坐标系
z_rect = cmath.rect(r, phi)
print(f"[z_rect]:{z_rect}")
# 基础-4：模r和幅角phi
z = complex(3, 4)
print(f"[模]:{abs(z)}")
print(f"[模]:{cmath.polar(z)}")
print(f"[幅角-弧度]:{cmath.phase(z)}")
print(f"[幅角-角度]:{math.degrees(cmath.phase(z))}")
# 进阶-1：三角函数-复数版本
# cmath.sin cmath.cos cmath.atan
z = complex(0, 1)
sin_z = cmath.sin(z)
print(f"sin(1j)={sin_z}")
print(f"cos(1j)={cmath.cos(z)}")
# 进阶-2：双曲函数-复数版本
z = complex(1, 1)
sinh_z = cmath.sinh(z)
print(f"[sinh_z]:{sinh_z}")
# 进阶-3：指数和对数-复数版本
# [欧拉公式]：e^(1j*Π)+1=0
euler = cmath.exp(complex(0, 1) * cmath.pi) + 1
print(f"[e^(1j*Π)+1]={euler}")


# 实战案例：RLC串流交流电电路分析
# - 计算电路的复数阻抗
# - 计算阻抗的模 计算阻抗的幅角
# - 计算电路的谐振频率
class RLC:
    def __init__(self, R: float, L: float, C: float):
        """
        初始化电路参数：
        R：电阻
        L：电感
        C：电容
        """
        self.R = R
        self.L = L
        self.C = C

    def calculate_imp(self, omega: float) -> complex:
        """
        计算复数阻抗
        Z=R+j(a*L-1/(a*C))
        rad/s
        """
        XL = omega * self.L
        XC = 1 / (omega * self.C)
        Z = self.R + complex(0, 1) * (XL - XC)
        return Z

    def analyze_imp(self, omega: float) -> dict:
        Z = self.calculate_imp(omega)
        Z_mag = abs(Z)  # 对复数阻抗进行取模运算
        Z_rad = cmath.phase(Z)
        Z_deg = math.degrees(Z_rad)
        return {
            "复数阻抗": Z,
            "阻抗模(Ω)": Z_mag,
            "幅角（弧度）": Z_rad,
            "幅角（角度）": Z_deg,
        }

    def calculate_resonant_frequency(self) -> dict:
        """
        谐振频率：
        f0=a0*(2Π)
        """
        omega0 = 1 / cmath.sqrt(self.L * self.C).real
        f0 = omega0 / (2 * cmath.pi)
        return {"谐振角频率": omega0, "谐振频率": f0}


if __name__ == "__main__":
    R, L, C = 10.0, 0.1, 10e-6
    rlc = RLC(R, L, C)
    # 计算谐振频率
    info = rlc.calculate_resonant_frequency()
    print(f"[info]:{info}")
