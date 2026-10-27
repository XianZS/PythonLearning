# --- if
# if 函数式
# 函数式的结果必须为布尔数值
# bool:(False/True)
# 1==1 >>> True
# -1==1 >>> False

number = int(input())

if number < 0:
    print("成立")

if number == 0:
    print(f"{number} == zero")
else:
    if number < 0:
        print(f"{number} < zero")
    else:
        print(f"{number} > zero")

if number == 0:
    print(f"{number} == zero")
elif number < 0:
    print(f"{number} < zero")
else:
    print(f"{number} > zero")
