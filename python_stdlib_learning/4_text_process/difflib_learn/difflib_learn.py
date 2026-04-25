"""
difflib 标准库学习
"""

import difflib as dl
from os import lseek

# 基础-1：如何生成带着标记的逐行检查
# 使用Differ类
# 比较两个字符串对象，生成标准的可视化差异结果
text1 = """
    hello jom,
    how are you?
    Thanks.
""".splitlines()
text2 = """
    hello kom,
    I'm fine.
    Thanks.
""".splitlines()
# 初始化Differ对象
d = dl.Differ()
# 差异化比较两个对象
d_res = d.compare(text1, text2)
print("=== 文本差异化分析结果 ===")
print("\n".join(d_res))
# 基础-2：计算序列相似度和最长公共子串
# sequencematcher
# 初始化——》返回相似度计算结果——》输出结果
a = "Python is good"
b = "Java is good"
s = dl.SequenceMatcher(isjunk=None, a=a, b=b)
# 字符串相似度计算
number = s.ratio()
print(f"a和b字符串的相似度计算结果为:{float(number) * 100:.2f}%")
# 字符串最长公共子串计算
match = s.find_longest_match(0, len(a), 0, len(b))
print(f"最长公共子串信息:{match}")
print(f"最长公共子串内容:{a[match.a : match.a + match.size]}")
# 基础-3：如何生成统一格式的差异（GIT格式的差异化表示）
# dl.unified_diff(
#   a, b, fromfile="", tofile="", fromfiledate="", tofiledate="", n=3, lineterm=""
# )
old_lines = ["def add(a,b):", "    return a+b", ""]
new_lines = ["def add(a,b):", "    return a+b", "def multiply(a,b):", "  return a*b"]
# 生成统一格式化差异
diff = dl.unified_diff(
    old_lines, new_lines, fromfile="old.py", tofile="new.py", lineterm=""
)
print("统一格式差异报告：")
print("\n".join(diff))
# 基础-4：生成上下文格式差异
old_lines = ["hello world", "how are you?"]
new_lines = ["hello world", "how are you?", "and you?", ""]
diff = dl.context_diff(
    old_lines, new_lines, fromfile="old.txt", tofile="new.txt", lineterm=""
)
print("上下文格式差异报告")
print("\n".join(diff))

# 进阶-1：生成HTML格式差异报告
old_text = """
    Python is a great language.
    It's easy to learn.
""".splitlines()
new_text = """
    Python is a powerful language.
    It's easy to learn and use.
""".splitlines()
# 生成 HTML 差异化格式报告
html_diff = dl.HtmlDiff()
html_content = html_diff.make_file(
    old_text, new_text, fromdesc="旧版本", todesc="新版本"
)
with open("example_html_different.html", "w", encoding="utf-8") as f:
    f.write(html_content)
    print("生成结束")

# 进阶-2：查找近似匹配的字符串
# get_close_matches(word,候选字符串列表,n=可选-返回的最大匹配数量,cutoff=可选-匹配阈值，默认为0.6)
# 设置目标词
target_word = "appel"  # 故意写错了
# 设置候选词列表
lists = ["apple", "banana", "apply", "application"]
# 查找近似匹配
matches = dl.get_close_matches(target_word, lists, cutoff=0.7)
print(f"[近似匹配]：{target_word}的近似匹配结果为:{matches}")


# 实战部分：代码版本差异分析工具
# 读取两个python文件
# 生成统一的格式差异
# 生成html可视化差异报告
# 计算两个文件之中的代码相似度
# 查找旧文件每行在新文件中的近似匹配行
class CodeDifferAnalyzer:
    def __init__(self, old_file, new_file):
        self.old_file = old_file
        self.new_file = new_file
        self.old_lines = self._read_file(old_file)
        self.new_lines = self._read_file(new_file)

    def _read_file(self, file_path):
        """读取文件为行列表形式"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().splitlines()
        except FileNotFoundError:
            print(f"文件路径{file_path}不存在")
            return []

    def generate_unified_diff(self):
        """生成统一的格式差异"""
        if not self.old_lines or not self.new_lines:
            return "文件读取失败，无法生成差异"
        diff = dl.unified_diff(
            self.old_lines,
            self.new_lines,
            fromfile=self.old_file,
            tofile=self.new_file,
            lineterm="",
        )
        return "\n".join(diff) or "两个文件没有差异"

    def generate_html_report(self, output_path="code_diff.html"):
        if not self.old_lines or not self.new_lines:
            print("不存在")
            return
        html_diff = dl.HtmlDiff(wrapcolumn=80)
        html_content = html_diff.make_file(
            self.old_lines, self.new_lines, fromdesc=self.old_file, todesc=self.new_file
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("差异化结果分析完毕")


if __name__ == "__main__":
    analyzer = CodeDifferAnalyzer("v1.py", "v2.py")
    # 1、输出统一的格式化差异报告
    print("=" * 60)
    print("统一格式化差异报告")
    print("=" * 60)
    print(analyzer.generate_html_report())
    # 2、生成HTML差异报告
    print("=" * 60)
    print("生成HTML差异报告")
    print("=" * 60)
    analyzer.generate_html_report("v1_v2_diff.html")
