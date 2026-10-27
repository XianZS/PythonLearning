"""
1 2 3
2 4 6
3 6 9
"""

# nums = []
# for x in range(1, 4):
#     child = []
#     for y in range(1, 4):
#         child.append(x * y)
#     nums.append(child)
#
# print(nums)

nums = [[x * y for y in range(1, 4)] for x in range(1, 4)]
print(nums)
print("---" * 10)
result_zip = zip(*nums)
print(list(result_zip))
