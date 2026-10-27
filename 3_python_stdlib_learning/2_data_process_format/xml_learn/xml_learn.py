"""
XML标准库学习
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

# 1、核心概念和基础解析
# 标签、属性、文本和子元素
xml_example = """
<library>
<book id="1">
<title>Python入门1</title>
</book>

<book id="2">
<title>Python入门2</title>
</book>

<book id="3">
<title>Python入门3</title>
</book>
</library>
"""
print(xml_example, type(xml_example))
root = ET.fromstring(xml_example)
print(root, type(root))
print("-" * 10)
# 2、遍历和查找XML元素
# （不推荐使用）直接遍历，使用for循环
for book in root:
    print(book)
    print(f"{book.tag},{book.get('id')}")
# （比较推荐的遍历方式）find() findall() 方法
# find() 返回第一个匹配结果
first_book = root.find("book")
print(f"第一本书的标题:{first_book.find('title').text}")  # type:ignore
# findall() 返回所有的匹配结果
all_books = root.findall("book")
for book in all_books:
    title = book.find("title").text  # type:ignore
    print(f"当前书的title是:{title}")
# （深层标签查询）iter()
for title in root.iter("title"):
    print(f"标题:{title.text}")

print("-" * 10)
# 3、如何修改和保存XML文档
root = ET.fromstring(xml_example)
tree = ET.ElementTree(root)
print(tree)
# 修改文本和属性
book = root.find("book")
# 修改文本
book.find("title").text = "C语言学习"  # type:ignore
# 添加修改属性
book.set("price", "99")  # type:ignore


all_books = root.findall("book")
for book in all_books:
    title = book.find("title").text  # type:ignore
    print(f"当前书的title是:{title}")
# （深层标签查询）iter()
for title in root.iter("title"):
    print(f"标题:{title.text}")
print("-" * 10)
# 添加子元素
new_book = ET.Element("book", id="4")
ET.SubElement(new_book, "title").text = "XML学习进阶"
ET.SubElement(new_book, "author").text = "admin"
root.append(new_book)
print("[root]:")
print(list(root))

all_books = root.findall("book")
for book in all_books:
    title = book.find("title").text  # type:ignore
    print(f"当前书的title是:{title}")
# （深层标签查询）iter()
for title in root.iter("title"):
    print(f"标题:{title.text}")

print("-" * 10)
# 删除子元素
for book in root.findall("book"):
    # print(book.get("id"), type(book.get("id")))
    if book.get("id") == "3":
        root.remove(book)
        # print("删除")
        break

for book in root.findall("book"):
    print(book.get("id"))

# 如何保存XML到文件之中
tree.write("books.xml", encoding="utf-8", xml_declaration=True)
print("已保存成功")
print("-" * 10)
# 4、如何创建XML文档
# 第一步：从0创建一个空文档
root = ET.Element("students")
student1 = ET.SubElement(root, "student", id="101")
ET.SubElement(student1, "name").text = "jom"
ET.SubElement(student1, "age").text = "18"
ET.SubElement(student1, "address").text = "A城市"


student2 = ET.SubElement(root, "student", id="102")
ET.SubElement(student2, "name").text = "kom"
ET.SubElement(student2, "age").text = "18"
ET.SubElement(student2, "address").text = "A城市"


student3 = ET.SubElement(root, "student", id="103")
ET.SubElement(student3, "name").text = "lom"
ET.SubElement(student3, "age").text = "18"
ET.SubElement(student3, "address").text = "A城市"

# 第二步：简单保存（无美化处理的简单保存）
tree = ET.ElementTree(root)
tree.write("students.xml", encoding="utf-8", xml_declaration=True)
print("从0开始初始化XML文档成功")


# 第三步：美观输出
def prettify_xml(element):
    """
    将ELEMENT转化为美化后的XML字符串
    """
    format_string = ET.tostring(element, encoding="utf-8")
    res = minidom.parseString(format_string)
    return res.toprettyxml(indent="  ")


# 保存美化之后的XML文件
res_all = prettify_xml(root)
with open("student_format.xml", mode="w+", encoding="utf-8") as f:
    f.write(res_all)
print("已经保存美化之后的所有内容，保存到student_format.xml文件之中")
print("-" * 10)
# 5、常见的应用场景
# 模拟RSS订阅解析
rss_xml = """
<rss version="2.0">
    <channel>
        <title>技术博客</title>
        <link>https://example.com</link>
        <item>
            <title>Python XML 教程</title>
            <link>https://example.com/xml</link>
            <pubDate>2026-04-14</pubDate>
        </item>
        <item>
            <title>Python JSON 教程</title>
            <link>https://example.com/json</link>
            <pubDate>2026-04-13</pubDate>
        </item>
    </channel>
</rss>
"""
root = ET.fromstring(rss_xml)
channel = root.find("channel")
print(f"博客标题:{channel.find('title').text}")  # type:ignore
print("最新文章")
for item in channel.iter("item"):  # type:ignore
    print(f"文章标题:{item.find('title').text}")  # type:ignore
    print(f"文章链接:{item.find('link').text}")  # type:ignore
    print(f"文章日期:{item.find('pubDate').text}")  # type:ignore
