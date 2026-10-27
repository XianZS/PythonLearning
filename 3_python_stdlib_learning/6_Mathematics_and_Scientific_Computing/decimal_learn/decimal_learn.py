"""
decimal 标准库学习
"""

import decimal

# 基础-1：导入和基本构造
# （推荐使用）第一种创建方式：字符串形式创建
a1 = decimal.Decimal("0.1")
a2 = decimal.Decimal("0.2")
print(a1 + a2, 0.1 + 0.2)
# 第二种创建方式：整数
a3 = decimal.Decimal(4)
print(f"[a3]:{a3}")
# 第三种创建方式：浮点数传入，会得到一个长小数
a4 = decimal.Decimal(0.1)
print(a4)
# 0.1000000000000000055511151231257827021181583404541015625
# 第四种创建方式：元组创建方式
# 1.23:(0,(1,2,3),-2)
# 0：表示符号 0正1负
# (1,2,3)：数字元组
# -2：指数
a5 = decimal.Decimal((0, (1, 2, 3), -2))
print(f"[a5]:{a5}")
# 基础-2：核心上下文控制
print(decimal.getcontext())
# Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[FloatOperation], traps=[InvalidOperation, DivisionByZero, Overflow])
# 设置有效数字
decimal.getcontext().prec = 9
# 设置decimal全局舍入模范
decimal.getcontext().rounding = decimal.ROUND_HALF_UP
print(decimal.getcontext())
# decimal.ROUND_HALF_UP:四舍五入
# decimal.ROUND_FLOOR:向下取整
# decimal.ROUND_CEILING:向上取整
# decimal.ROUND_HALF_EVEN:银行家舍入（四舍六入五成双）
# 基础-3：基础运算和比较
a = decimal.Decimal("1")
b = decimal.Decimal("3")
print(f"[a+b]:{a + b}")
print(f"[a/b]:{a / b}")
if 0.1 + 0.2 == 0.3:
    print("[常规运算]:0.1+0.2==0.3")
else:
    print("[常规运算]:0.1+0.2!=0.3")
c = decimal.Decimal("0.1")
d = decimal.Decimal("0.2")
if c + d == decimal.Decimal("0.3"):
    print("[Decimal]:0.1+0.2==0.3")
else:
    print("[Decimal]:0.1+0.2!=0.3")

# 进阶-1：临时上下文管理
print(f"全局精度下的计算:{decimal.Decimal('1') / decimal.Decimal('3')}")
with decimal.localcontext() as ctx:
    ctx.prec = 2  # 将decimal临时精度设置为两位有效数字
    print(f"临时精度下的计算:{decimal.Decimal('1') / decimal.Decimal('3')}")
print(f"恢复全局精度下的计算:{decimal.Decimal('1') / decimal.Decimal('3')}")
# 进阶-2：固定小数位
amount = decimal.Decimal("123.456")
res = amount.quantize(decimal.Decimal("0.00"), rounding=decimal.ROUND_HALF_UP)
res2 = amount.quantize(decimal.Decimal("0"), rounding=decimal.ROUND_HALF_UP)
print(res, res2)
# 进阶-3：信号和异常处理
try:
    a = 9
    b = 0
    print(a / b)
except Exception as e:
    print(f"[ERROR]:{e}")

try:
    a = decimal.Decimal("9")
    b = decimal.Decimal("0")
    print(a / b)
except Exception as e:
    print(f"[ERROR]:{e}")
# 关闭除零异常
# 非0数字/0 将分母的0作为一个趋近于0的无穷小来处理，所以它的返回结果就是一个无穷大
decimal.getcontext().traps[decimal.DivisionByZero] = False
print(decimal.Decimal("1") / decimal.Decimal("0"))
# 关闭无效操作
decimal.getcontext().traps[decimal.InvalidOperation] = False
print(decimal.Decimal("0") / decimal.Decimal("0"))
# 进阶-4：数学函数和特殊数值
number9 = decimal.Decimal("9")
print(number9.sqrt())
print(number9.exp())
inf_dec = decimal.Decimal("-Infinity")
print(inf_dec)
nan_dec = decimal.Decimal("NaN")
print(nan_dec)


# 实战案例
# === 实现电商购物车精准结账系统 ===
# - 精确计算总价、折扣、税
# - 将所有的金额保留两位小数，然后进行四舍五入
# - 支持满减折扣
decimal.getcontext().prec = 10
decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def precise_checkout(cart, number1, number2, tax_rate=decimal.Decimal("0.05")):
    """
    cart：是什么？单价？买了几个？
    number1：折扣门槛
    number2：折扣数目
    tax_rate：税率
    """
    # 计算每个商品的小计
    # cart==list list_child=(name,price,quantity)
    subtotals = []
    for name, price_str, quantity in cart:
        price = decimal.Decimal(price_str)
        subtotal = price * quantity
        subtotals.append(subtotal)
    # 计算总价
    total = sum(subtotals)
    # 应用折扣
    if total >= number1:
        print("满足折扣条件")
        total -= number2
    else:
        print("不满足折扣条件")
    # 计算税费
    tax = total * tax_rate
    print(f"[税费]:{tax}")
    # 计算最终价格=商品价格+税费
    res = total + tax
    return res


carts = [("无线鼠标", "99.99", 10), ("键盘", "500", 3), ("显示器", "600.54", 20)]
number = precise_checkout(carts, 100, 10)
print(number)
