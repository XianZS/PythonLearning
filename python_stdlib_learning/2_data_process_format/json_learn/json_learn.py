"""
JSON 标准库学习
1、数据类型的映射关系
2、序列化操作
3、反序列化操作
4、处理自定义对象
5、常见场景应用实战
"""

import json
from typing import dataclass_transform

# 1、json的核心概念和数据类型的映射
# object dict
# array list/tuple
# string str
# number int/float
# null None

# 2、序列化
# 主要是实现将python数据类型转换为json数据类型
# 实现dict-》object对象的转换：
data = {
    "name": "admin",
    "age": 25,
    "is_student": False,
    "address": {"city": "西安", "district": "临潼区"},
}
# print(data, type(data))
# json.dumps(python对象)：将python对象转换为json字符串
json_obj = json.dumps(data)
print(json_obj, "\n", type(json_obj))

json_obj_format = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)
print(json_obj_format)
# 将json数据直接写入文件之中
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
    print("\n已经写入到data.json文件之中")

# 3、如何进行反序列化
# JSON数据类型转换为Python数据类型
# json.loads(s)：将json字符串转换为python对象
json_str = """
    {"name":"北屿青禾","age":"22","is_student":true}
"""
# json_str：true/false
# python：True/False
# print(json_str, type(json_str))
res = json.loads(json_str)
print(res, type(res))

# json.load()
with open("data.json", "r", encoding="utf-8") as f:
    res = json.load(f)
    print(res)

print("-" * 10)


# 4、处理自定义对象
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name},age={self.age})"


class PersonEncoder(json.JSONEncoder):
    def default(self, obj):  # type:ignore
        if isinstance(obj, Person):
            return {"__type__": "Person", "name": obj.name, "age": obj.age}
        return super().default(obj)


def person_to_dict(obj):
    if isinstance(obj, Person):
        return {"__type__": "Person", "name": obj.name, "age": obj.age}
    raise TypeError(f"Object of type {type(obj)} is not json")


person = Person("admin", 22)
# 》》》 序列化过程 《《《
# 使用自定义的PersonEncoder
json_str1 = json.dumps(person, cls=PersonEncoder, ensure_ascii=False)
# 使用default自定义默认参数
json_str2 = json.dumps(person, default=person_to_dict, ensure_ascii=False)
print(json_str1)


# 》》》 反序列化过程 《《《
def dict_to_person(d):
    if d.get("__type__") == "Person":
        return Person(d["name"], d["age"])
    return d


person_from_json = json.loads(json_str1, object_hook=dict_to_person)
print("反序列化之后的对象为:")
print(person_from_json)
print(type(person_from_json))

print("-" * 10)
# 5、常见的应用场景实战
# API 数据解析
api_response = """
{
    "code":200,
    "message":"success",
    "data":{
        "total":2,
        "items":[
            {"id":1,"title":"测试数据1","price":99},
            {"id":2,"title":"测试数据2","price":88},
            {"id":3,"title":"测试数据3","price":77}
        ]
    }
}
"""
print(api_response)
res = json.loads(api_response)
if res["code"] == 200:
    print("API请求成功")
    items = res["data"]["items"]
    for item in items:
        print(item)
else:
    print("API请求失败")


if __name__ == "__main__":
    pass
