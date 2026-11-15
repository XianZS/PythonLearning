names=["aom","dom","gom"]

if "kom" not in names:
    print("True")
else:
    print("False")

res="kom" not in names
print(res)

print("-"*10)
names=["aom","dom","gom"]
new_names=names
new_names2=["aom","dom","gom"]
print(id(names))
print(id(new_names))
print(id(new_names2))

res2=names is new_names
res3=names is not new_names2
res4=new_names2 is new_names
print(res2,res3,res4)

print("-"*10)

a,b=0,1
if a and b:
    print("运行成功")
else:
    print("运行失败")


print("-"*10)

res5=a and b
print(res5)