# 字符串处理 正则表达式 re
import re


test_txt = """
客户联系信息：
张三：13812345678，邮箱：zhangsan@example.com
李四：13998765432，邮箱：lisi_123@test.cn
王五：18876543210（备用：17788889999），邮箱：wangwu@company.com
无效号码：12345678901（位数不对）、138123456789（超11位）
无效邮箱：wangwu@、@test.com、lisi#test.cn
"""

# 编译一个正则表达式
# \d{number} 匹配number个数字
# [abcd] 随意匹配abcd四个对象之中的一个
# obj 只匹配obj这个对象
re_com = re.compile(r"1[345678]\d{9}")

# 如何得到所有的匹配结果
res = re_com.findall(test_txt)
print(res, type(res))

# 只得到第一个正则re匹配结果
res_first = re_com.search(test_txt)
print(res_first, type(res_first))

# 123******89
# <re.Match object; span=(12, 23), match='13812345678'> <class 're.Match'>
result = re_com.sub(lambda x: x.group()[:3] + "******" + x.group()[-2:], test_txt)
print(result)


# 日期的简单格式化 datetime
from datetime import datetime, timedelta, date

# 咱们需要格式化的数据
test_txt_1 = "2026年1月1日 3时15分28秒"
# 年    %Y
# 月    %m
# 日    %d
# 时    %H
# 分    %M
# 秒    %S
str_format_pattern = "%Y年%m月%d日 %H时%M分%S秒"
res = datetime.strptime(test_txt_1, str_format_pattern)
print(res, type(res))

now_time = date.today()
print(now_time)
time_bulle = timedelta(days=100)
next_time = now_time + time_bulle
print(next_time)


if __name__ == "__main__":
    pass

