"""
textwrap 标准库学习
"""

import textwrap as tw

# 基础-1：文本自动填充换行
# textwrap.fill(
#   text,width,
#   initial_indent="",
#   subsequent_indent=""
# )
print("\t===tw.fill===")
long_text = "Python is a powerful programming language."
res1 = tw.fill(text=long_text, width=20, initial_indent="  ", subsequent_indent="    ")
print(res1, type(res1))
# 基础-2：将文本划分为行列表
# textwrap.wrap()
res2 = tw.wrap(text=long_text, width=20)
print(res2, type(res2))
print("-" * 10)
# 基础-3：文本截断和占位
res3 = tw.shorten(text=long_text, width=20, placeholder="[...]")
print(res3)
print("-" * 10)

# 进阶-1：给文本添加行前缀
# 语法规范：
# textwrap.indent(text,prefix,predicate=None)
original_text = """Python
Java
"""
print(f"[初始文本]:\n{original_text}")
res1 = tw.indent(original_text, ">>>")
print(f"[处理之后]:\n{res1}")


def judge(line):
    # print(f"[line]:{line},{type(line)}")
    if line == "Python\n":
        return True
    return False


res11 = tw.indent(original_text, ">>>", predicate=judge)
print(res11)
print("-" * 10)
# 进阶-2：实现自定义复杂排版规则
wrapper = tw.TextWrapper(
    width=45,
    initial_indent=">>>",
    subsequent_indent="   ",
    break_long_words=False,
    expand_tabs=True,
    tabsize=4,
    placeholder="[...]",
)
text_with_tabs = "Python的textwrap的的的模块\t提供了TextWrapper类，通过实现TextWrapper类，得到一个类对象，支持自定义复杂的排版规则，比如可以处理很长的字符串supermarket"
filled1 = wrapper.fill(text_with_tabs)
print(filled1)
print("-" * 10)
# 进阶-3：长单词与连字符
english_text = "This is a text with a some word word supercalifragilisticexpia word and a high-preformance component"
w1 = tw.TextWrapper(width=30)
print(w1.fill(english_text))
