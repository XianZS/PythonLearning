for x in range(1, 11):
    print(x)
else:
    print("遍历结束")

# for ... :
#   for code
# else:
#   else code
print("---" * 10)
# names = ["jom", "kom", "lom", None, "qom", "pom"]
names = ["jom", "kom", "lom", "qom", "pom"]

L = len(names)
for index in range(L):
    if names[index]:
        print(names[index])
    else:
        print("存在非法名称")
        break
else:
    print("无非法名称")
print("---" * 10)

index = -10
while index < 10:
    print(index)
    index += 1
else:
    print(f"[end number] >>> {index}")
