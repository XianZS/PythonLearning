"""
re 标准库
"""

import re

# 1、从字符串开头进行匹配
# re.match(正则表达式模式字符串，待匹配的目标字符串，可选参数-匹配修饰符flags)
text1 = "Python is good"
text2 = "java is good"
res1 = re.match(r"Python", text1)
print(f"res1:{res1}")
res2 = re.match(r"Python", text2)
print(f"res2:{res2}")
# 2、搜索第一个匹配项
text = "联系方式为: 123@qq.com 或 456@qq.com"
pattern_match = r"\w+@\w+\.\w+"
email = re.search(pattern_match, text)
print(f"email:{email}，精准输出:{email.group()}")  # type:ignore
# 3、搜索所有的匹配项
emails = re.findall(pattern_match, text)
print(f"所有的邮箱为:{emails}")
# ['123@qq.com', '456@qq.com']
# 4、搜索所有的匹配项，迭代器方式
emails_match_obj = re.finditer(pattern_match, text)
print(f"emails_match_obj:\n{list(emails_match_obj)}")
for match in re.finditer(pattern_match, text):
    print(match)
    print(f"匹配内容:{match.group()}，匹配位置:{match.span()}")
# 5、re.sub()替换匹配项
# 替换所有选项，返回新的字符串
# re.sub(pattern,repl,string,count=0,flags=0/else)
text = "我的个人电话号为: 12345678900 , 我的身份证号为 12345678900"
res = re.sub(r"\d", "*", text)
print(f"[{text}]加密之后的结果为:{res}")


def repl_func(match):
    match_obj = str(match.group())
    res = match_obj[:3] + "*" * (len(match_obj) - 6) + match_obj[-3:]
    return res


res2 = re.sub(r"\d+", repl_func, text)
print(f"保留前3位和后3位的结果为:{res2}")

# 6、按照模式分割字符串
# re.split(pattern,string,maxsplit=0,flags=0)
text = "a,b:c d,e;;f"
res = re.split(r"[,;: ]+", text)
print(f"按照多种分隔符进行分割之后的结果为:{res}")

# 7、预编译正则表达式
# 语法规范：pattern_obj=re.compile(pattern,flags=0)
email_obj = re.compile(r"\w+@\w+\.\w+")
print(email_obj, type(email_obj))
# 多次使用该模式
text1 = "联系: support@emample.com"
text2 = "反馈: feedback@example.com"
print(email_obj.findall(text1))
print(email_obj.findall(text2))

# === 进阶部分 ===
# 进阶-1：分组
# 捕获组和非捕获组
# 捕获组:(pattern)，通过 match.group(n) 来提取
# 非捕获组:(?:pattern)，不占用分组索引
text = "手机号: 12345678900"
pattern = r"(\d{3})(\d{8})"
match = re.search(pattern, text)
print(match)
if match:
    print(f"[match.group]:{match.group()}")
    print(f"号段:{match.group(1)}")
    print(f"后8位:{match.group(2)}")
# 命名捕获组
email = "user@example.com"
pattern = r"(?P<username>\w+)@(?P<domain>\w+\.\w+)"
match = re.search(pattern, email)
if match:
    print(f"用户名:{match.group('username')}")
    print(f"邮件服务器:{match.group('domain')}")
else:
    print("未找到match")
print("-" * 10)
# 进阶-2：贪婪匹配和非贪婪匹配
text = "<div>内容1</div><div>内容2</div>"
# 贪婪匹配-默认，假设现在需要匹配最长的子串
pattern_greedy = r"<div>.*</div>"
res = re.findall(pattern_greedy, text)
print(f"贪婪匹配:{res}")
# 非贪婪匹配
pattern_lazy = r"<div>.*?</div>"
res = re.findall(pattern_lazy, text)
print(f"非贪婪匹配:{res}")
# 贪婪匹配:['<div>内容1</div><div>内容2</div>']
# 非贪婪匹配:['<div>内容1</div>', '<div>内容2</div>']
# 进阶-3：匹配修饰符号
# re.I:忽略大小写
# re.M:多行匹配
# re.S:让.匹配包括换行符在内的所有字符
# re.X:忽略模式之中的空白和注释
text1 = "Python python PYTHON"
res1 = re.findall("Python", text1)
print(f"未设置大小写忽略的匹配结果为:{res1}")
res2 = re.findall("Python", text1, flags=re.I)
print(f"设置大小写忽略的匹配结果为:{res2}")


# 实战案例
# 日志分析与信息提取工具
# 功能描述：
# 提取出每条日志的IP、时间、请求方式、URL、状态码、相应大小等一些信息。
class LogAnalyzer:
    def __init__(self, log_text):
        self.log_text = log_text
        self.log_pattern = re.compile(
            r"""
            (?P<ip>\d+\.\d+\.\d+\.\d+)    # IP地址
            \s-\s-\s                       # 固定分隔符
            \[(?P<time>[^\]]+)\]           # 时间（匹配到]为止）
            \s"                            # 空格+引号
            (?P<method>\w+)                # 请求方法（GET/POST等）
            \s(?P<url>[^\s]+)              # URL
            \sHTTP/[\d.]+                  # HTTP版本
            "\s                            # 引号+空格
            (?P<status>\d+)                # 状态码
            \s(?P<size>\d+|-)              # 响应大小（-表示无）
            \s"[^"]+"\s"                   # 忽略referer
            (?P<user_agent>[^"]+)          # User-Agent
            "\s(?P<response_time>[\d.]+)   # 响应时间（秒）
        """,
            re.X,
        )  # 用re.X忽略模式中的空白和注释

    def extract_all_logs(self):
        """提取出所有日志的结构化信息"""
        logs = []
        for math in self.log_pattern.finditer(self.log_text):
            logs.append(math.groupdict())
        return logs


if __name__ == "__main__":
    nginx_logs = """192.168.1.100 - - [20/May/2024:10:30:45 +0800] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 0.5
10.0.0.5 - - [20/May/2024:10:30:46 +0800] "POST /api/login HTTP/1.1" 200 567 "-" "PostmanRuntime/7.0" 1.2
192.168.1.101 - - [20/May/2024:10:30:47 +0800] "GET /not-found HTTP/1.1" 404 152 "-" "Chrome/125.0" 0.3
172.16.0.20 - - [20/May/2024:10:30:48 +0800] "GET /api/data HTTP/1.1" 500 89 "-" "Firefox/126.0" 2.1
192.168.1.100 - - [20/May/2024:10:30:49 +0800] "GET /static/logo.png HTTP/1.1" 200 4567 "-" "Safari/17.0" 0.8"""
    analyzer = LogAnalyzer(nginx_logs)
    for cho in analyzer.extract_all_logs():
        print(cho)
