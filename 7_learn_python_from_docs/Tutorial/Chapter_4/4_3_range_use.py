# 等差数列
# a1=3
# d=4
nums = [x for x in range(3, 100, 4)]
print(nums)
print("---" * 10)
# range(start_index,end_index,step)
# start_index:可选参数，默认值为0
# end_index:必选参数
# step:可选参数，默认值为1
# 区间取值范围：左闭右开
# 包含start_index，而不包含end_index。
res = list(range(10))
print(res)
print("---" * 10)
# --- 负数步长
# 9开始，d=-3
some = [x for x in range(9, -100, -3)]
print(some)

print("---" * 10)
names = ["aom", "som", "dom", "fom", "gom", "hom"]
# 假设求一次长度消耗的时间为time
# 总时间为n*time
for index in range(len(names)):
    print(names[index])
# 总时间为time
L = len(names)
for index in range(L):
    print(names[index])
print("---" * 10)
print(sum(some))
