"""
calendar_learn 学习
"""

import calendar as cr
import locale
from typing import List, Tuple, Optional

# 基础-1：设置/获取一周的第一天
first_day = cr.firstweekday()
print(f"[first_day]:{first_day}")
cr.setfirstweekday(6)
first_day = cr.firstweekday()
print(f"[first_day]:{first_day}")
# 基础-2：如何判断闰年
# 闰年的规则：能被4整除但不能被100整除，或者可以被400整除。
print(cr.isleap(2024))
print(cr.isleap(2025))
print(cr.isleap(2026))
# 基础-3：如何计算两个年份之间的闰年数
# cr.leapdays(y1,y2)
print(f"[2000~2026]:{cr.leapdays(2000, 2024)}")
# 基础-4：获取当前时间是一周之中的星期几
print(f"[weekday]:{cr.weekday(2026, 4, 26)}")
# 基础-5：获取某一个月的日历信息
# cr.monthrange(year,month)
first_weekday, num_days = cr.monthrange(2026, 4)
print(f"[first_weekday]:{first_weekday},[num_days]:{num_days}")
# 基础-6：生成文本格式的月历
# cr.month()
print(f"[2026.4]:\n{cr.month(2026, 4)}")
# 基础-7：生成文本格式的年历
print(f"[2026]:\n{cr.calendar(2026)}")
# 进阶-1：生成列表格式的月历/年历
print(f"[list-2026.4]:\n{cr.monthcalendar(2026, 4)}")
print(f"[list-2026]:\n{cr.Calendar().yeardays2calendar(2026)}")
# 进阶-2：生成HTML格式的月历或者年历
# 生成2026-4的HTML月历
html_cal = cr.HTMLCalendar(cr.MONDAY)
html_content = html_cal.formatmonth(2026, 4)
with open("2026_4.html", "w", encoding="utf-8") as f:
    f.write(
        """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>2026年4月日历</title>
        <style>
            table { border-collapse: collapse; margin: 20px auto; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
            th { background-color: #f2f2f2; }
            .sun { color: red; }
            .sat { color: blue; }
        </style>
    </head>
    <body>
    """
        + html_content
        + """
    </body>
    </html>
    """
    )
    print("写入成功")

# 进阶-3：多语言适配
# 配合local模块
locale.setlocale(locale.LC_ALL, "Chinese (Simplified)_China.936")
print(cr.month(2026, 4))


# 实战案例：工作日统计和日程提醒辅助工具
# - 统计工作日
# - 支持自定义非工作日
# - 生成某一个月的工作日列表或者非工作日列表
# - 判断某一天是否为工作日
# - 快速定位第一个工作日和最后一个工作日
class WorkDay:
    def __init__(
        self,
        firstweekday: int = cr.MONDAY,
        non_workdays: Optional[List[Tuple[int, int, int]]] = None,
    ):
        """
        firstweekday:一周第一天的索引
        non_workdays:自定义非工作日列表
        """
        self.firstweekday = firstweekday
        cr.setfirstweekday(self.firstweekday)
        self.non_workdays = non_workdays

    def is_workday(self, year: int, month: int, day: int) -> bool:
        """
        判断某一天是不是工作日
        是工作日：True
        不是工作日：False
        """
        if (year, month, day) in self.non_workdays:  # type:ignore
            return False
        weekday = cr.weekday(year, month, day)
        return 0 <= weekday <= 4

    def count_month_day(self, year: int, month: int) -> Tuple[int, int, int]:
        """
        统计某一个月的总天数、工作日数、非工作日数
        """
        total_days = cr.monthrange(year, month)[1]
        workdays = 0
        non_workdays = 0
        for day in range(1, total_days + 1):
            if self.is_workday(year, month, day):
                workdays += 1
            else:
                non_workdays += 1
        return (total_days, workdays, non_workdays)

    def get_month_day_list(self, year: int, month: int):
        """得到工作日列表 & 得到非工作日列表"""
        total_days = cr.monthrange(year, month)[1]
        workday_list, non_workdays = [], []
        for day in range(1, total_days + 1):
            date_tuple = (year, month, day)
            if self.is_workday(*date_tuple):
                workday_list.append(date_tuple)
            else:
                non_workdays.append(date_tuple)
        return (workday_list, non_workdays)


if __name__ == "__main__":
    custom_days = [(2026, 4, 1), (2026, 4, 2), (2026, 4, 3), (2026, 4, 8)]
    c = WorkDay(non_workdays=custom_days)
    # 统计2026年4月天数
    print(f"[2026.4]:{c.count_month_day(2026, 4)}")
    # 判断某一天是不是工作日
    print(c.is_workday(2026, 4, 8))
    # 获取工作日列表和非工作日列表
    print(f"[2026.4]:{c.get_month_day_list(2026, 4)[0]}")
    print(f"[2026.4]:{c.get_month_day_list(2026, 4)[1]}")
