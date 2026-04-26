"""
datetime 标准库
"""

import datetime
from typing import dataclass_transform


# 基础-1：获取当前的时间和日期
# 获取本地日期
now_time = datetime.date.today()
print(f"[now_time]:{now_time}")
# 返回当前本地的日期时间
now_day_time = datetime.datetime.now()
print(f"[now_day_time]:{now_day_time}")
# 基础-2：创建指定的日期时间
# 创建日期对象
d = datetime.date(2026, 5, 1)
print(f"指定时间为:{d}")
# 创建指定日期时间
dt = datetime.datetime(2026, 5, 2, 12, 0, 0)
print(f"指定日期时间为:{dt}")
# 基础-3：提取具体属性
dt = datetime.datetime(2026, 5, 1, 1, 1, 1)
print(f"[年]:{dt.year}")
print(f"[月]:{dt.month}")
print(f"[日]:{dt.day}")
print(f"[时]:{dt.hour}")
print(f"[分]:{dt.minute}")
print(f"[秒]:{dt.second}")
# 基础-4：日期时间和字符串的转换
# datetime对象转为字符串：datetime.strftime()
now = datetime.datetime.now()
formatted1 = now.strftime("%Y-%m-%d %H:%M:%S")
formatted2 = now.strftime("%Y年%m月%d日 %H时%M分%S秒")
print(formatted1, type(formatted1))
print(formatted2, type(formatted2))
# 字符串转为datetime对象：datetime.strptime()
date_str = "2026-5-3 09:08:07"
dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print(dt)
print("-" * 10)
# 基础-5：时间间隔
# timedelta
# datetime.timedelta(days=0,seconds=0,hours=0,days=0)
now = datetime.datetime.now()
print(f"[当前时间]:{now}")
after_3 = now + datetime.timedelta(days=3)
print(f"[三天后时间]:{after_3}")


# 进阶-1：时区处理
class UTC8(datetime.tzinfo):
    def utcoffset(self, dt):
        # 设置时间偏移量为8小时
        return datetime.timedelta(hours=8)

    def tzname(self, dt):
        return "UTC+8"  # 时区名称设置

    def dst(self, dt):
        return datetime.timedelta(0)  # 无夏令时


# 创建带着时区的datetime对象
dt_utc8 = datetime.datetime(2026, 5, 5, 20, 14, 30, tzinfo=UTC8())
print(dt_utc8)

# 进阶-2：实现时间戳和datetime模块之间的转换
# 时间戳：时间戳指的是从1970年1月1日0点0分0秒到现在的秒数
now = datetime.datetime.now()
time_stamp = now.timestamp()
print(f"[时间戳]:{time_stamp}，时间戳类型:{type(time_stamp)}")
dt = datetime.datetime.fromtimestamp(489012849)
print(f"[时间戳转为datetime时间]:{dt}")
# 进阶-3：时间日期的比较
dt1 = datetime.datetime(2026, 5, 2)
dt2 = datetime.datetime(2026, 5, 3)
if dt1 > dt2:
    print(f"{dt1}时间大")
elif dt1 < dt2:
    print(f"{dt2}时间大")
else:
    print("两个时间一样大")
# 进阶-4：替换日期时间的属性
dt = datetime.datetime(2026, 5, 6)
print(f"[原时间]:{dt}")
new_dt = dt.replace(day=7)
print(f"[新时间]:{new_dt}")
# 进阶-5：如何进行星期数的判断
# 语法规范：
#   date_obj.weekday():返回0（周一）~6（周日）
#   date_obj.isoweekday():返回1（周一）~7（周日）
now_time = datetime.datetime.now()
print(f"当前是周几？weekday：{now_time.weekday()}")
print(f"当前是周几？isoweekday：{now_time.isoweekday()}")


# 实战案例
# 任务调度与时间追踪工具
# - 添加任务
# - 计算任务的剩余时间
# - 判断任务是否过期
# - 按照截至时间对任务进行排序
# - 统计本周内需要完成的任务
class Task:
    def __init__(self, name, deadline):
        self.name = name
        self.deadline = deadline

    def is_overdue(self):
        """判断任务是否过期"""
        return datetime.datetime.now() > self.deadline

    def get_remaining_time(self):
        """获取任务的剩余时间"""
        now_time = datetime.datetime.now()
        if self.is_overdue():
            # 过期，返回已经过期的时间
            return now_time - self.deadline
        else:
            # 没有过期，返回剩余的时间
            return self.deadline - now_time

    def __str__(self):
        status = "已过期" if self.is_overdue() else "进行中"
        remaining = self.get_remaining_time()
        if self.is_overdue():
            # 过期
            time_str = f"已经过期{remaining.days}天"
        else:
            time_str = f"剩余{remaining.days}天"
        return f"【{status}】{self.name}|截至时间:{self.deadline.strftime('%Y-%m-%d %H:%M')}|{time_str}"
