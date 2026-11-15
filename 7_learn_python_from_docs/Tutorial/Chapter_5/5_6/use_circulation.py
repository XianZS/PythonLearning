people={
    "name":"jom",
    "age":18,
    "address":"A城市",
}
for cho in people:
    print(cho)

print("-"*10)

for k,v in people.items():
    print(k,v)

print("-"*10)

names=["aom","som","dom","fom","gom","hom"]
# for index in range(len(names))
# for child in names
for index,child in enumerate(names):
    print(f"下标:[{index}];元素:[{child}]")

print("-"*10)

names1=["jom","aom","dom"]
ages1=[12,13,13,14]
address=["a","b","c"]
for x,y,z in zip(names1,ages1,address):
    print(x,y,z)

print("-"*10)
names2=["jom","aom","dom"]
name3=reversed(names2)
print(list(name3))

print("-"*10)

nums=[123,3,2,1,12,3,5,2,2,3,54,212,12,1,1,1,675]
nums.sort()
print(nums)
nums=[123,3,2,1,12,3,5,2,2,3,54,212,12,1,1,1,675]
new_nums=sorted(nums)
print(new_nums)
print(nums)

print("-"*10)

nums=[123,3,2,1,12,3,5,2,2,3,54,212,12,1,1,1,675]
print(set(nums))
new_nums=sorted(set(nums))
print(new_nums)

print("-"*10)
some=["dom","som","kom",None,"pom"]
for index,child in enumerate(some):
    if not child:
        some[index]="aom"
        break
print(some)