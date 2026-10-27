for x in range(1, 11):
    if x == 6:
        print(x)
        break
    else:
        print(x)

print("---" * 10)
for x in range(1, 11):
    if x == 6:
        continue
    else:
        print(x)
