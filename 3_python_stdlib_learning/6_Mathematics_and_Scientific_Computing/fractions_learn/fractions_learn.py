"""
fractions 标准库学习
"""

import decimal
import fractions

# 基础-1：导入和基本构造
# 分子+分母
# fractions.Fraction(分子，分母)
f1 = fractions.Fraction(1, 3)
print(f"[f1]:{f1},[type]:{type(f1)}")
# 单个整数，分母默认为1
f2 = fractions.Fraction(5)
print(f"[f2]:{f2},[type]:{type(f2)}")
# 浮点数形式创建
f3 = fractions.Fraction(0.3)
print(f"[f3]:{f3},[type]:{type(f3)}")
# (推荐)字符串形式进行创建
f4 = fractions.Fraction("0.3")
print(f"[f4]:{f4},[type]:{type(f4)}")
# DECIMAL形式创建
f5 = fractions.Fraction(decimal.Decimal("0.3"))
print(f"[f5]:{f5}")
# 通过数字来构建
f6 = fractions.Fraction.from_number(0.3)
print(f"[f6]:{f6}")
# 基础-2：核心属性
# fractions对象的分子和分母
f_obj = fractions.Fraction("1/3")
print(f"[f_obj]:{f_obj},[分子]:{f_obj.numerator},[分母]:{f_obj.denominator}")
# 基础-3：简单数学运算
a = fractions.Fraction("1/4")
b = fractions.Fraction("1/12")
c = a + b
print(f"[a+b]:{c},[type]:{type(c)}")
judge = a > b
print(f"[a>b]:{judge}")
print("-" * 10)
# 进阶-1：限制分母
f = fractions.Fraction(0.3)
print(f"[f]:{f}")
# [f]:5404319552844595/18014398509481984
new_f = f.limit_denominator(10)
print(f"[new_f]:{new_f}")
# [new_f]:3/10
# 进阶-2：类型转换
frac = fractions.Fraction("3/2")
print(f"[frac]:{frac}")
print(f"[float-frac]:{float(frac)}")
print(f"[int-frac]:{int(frac)}")
# 进阶-3：格式化输出
# 假设现在存在一个物品的效率为0.3333333
f = fractions.Fraction("1/3")
print(f"[float]:{float(f)}")
print(f"[效率]:{f:.3%}")


# 实战案例
# === 食谱分量计算器 ===
def adjust_recipe(datas, original_servings, target_servings):
    """
    第一个参数：原食谱字典
    第二个参数：原食谱的份数
    第三个参数：目标食谱的份数
    return :调整之后的食谱字典
    """
    ratio = fractions.Fraction(target_servings, original_servings)
    adjusted = dict()
    for name, amount in datas.items():
        # key：食材名字 value：食材数量
        if isinstance(amount, str):
            frac_amount = fractions.Fraction(amount)
        else:
            frac_amount = fractions.Fraction.from_number(amount)
        adjusted[name] = (frac_amount * ratio).limit_denominator(8)
    return adjusted


# 假设原食谱是两人份，现在需要将原本两人份的食谱，调整为五人份
datas = {"面包": "1/2", "牛奶": "3/4", "糖": 2, "鸡蛋": 1}
adjusted = adjust_recipe(datas, original_servings=2, target_servings=5)
print(f"[adjusted]:{adjusted}")
