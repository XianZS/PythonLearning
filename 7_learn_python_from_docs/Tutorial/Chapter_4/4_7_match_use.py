# match var:
#   case 被匹配对象1:
#       case 1 code
#   case 被匹配对象2:
#       case 2 code


def http_status(status_code):
    match status_code:
        case 200:
            return "success"
        case 400 | 401 | 402 | 403:
            return "not found"
        case 500:
            return "client error"
        case _:
            return "default code"


res = http_status(403)
print(res)
res = http_status(402)
print(res)

# res = http_status(400)
# print(f"[res str] >>> {res}")
# res = http_status(300)
# print(f"[res str] >>> {res}")


def judge_point(point):
    match point:
        case (x, y) if x > 0 and y > 0:
            print("第一象限")
        case (x, y) if x < 0 and y > 0:
            print("第二象限")
        case (x, y) if x < 0 and y < 0:
            print("第三象限")
        case (x, y) if x > 0 and y < 0:
            print("第四象限")
        case (x, 0) if x > 0:
            print("x正半轴")
        case (x, 0) if x < 0:
            print("x负半轴")
        case (0, y) if y > 0:
            print("y正半轴")
        case (0, y) if y < 0:
            print("y负半轴")


judge_point((-1, 10))
judge_point((-1, 0))


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


def where(point):
    match point:
        case [Point(x=0, y=0)]:
            print("origin")
        case [Point(x=0, y=y)]:
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case _:
            print("default case code")


where([Point(0, 0)])
where([Point(0, 1)])


def func(stu: dict):
    # 额外的键会被忽略
    match stu:
        case {"name": "jom", "address": "shanghai"}:
            print("=== 1 ===")
            print(f"{stu}")
        case {"name": "jom", "number": "10000"}:
            print("=== 2 ===")
            print(f"{stu}")


stu = {
    "name": "jom",
    "address": "xian",
    "number": "10000",
    "other": "default",
}
func(stu)

# 具名常量
from enum import Enum


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


color = Color("red")
print(color, type(color))
match color:
    case Color.RED:
        print("红色")
    case Color.GREEN:
        print("绿色")
    case Color.BLUE:
        print("蓝色")
