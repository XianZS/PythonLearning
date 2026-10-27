"""
tempfile 标准库学习：临时文件和临时目录的创建和使用
1、临时文件创建（核心功能）
（1）临时文件
（2）文件
2、临时目录创建（批量临时文件）
"""

import tempfile as tf
import pathlib


# 1、临时文件的创建
# 自动删除的临时文件的创建
fname1 = ""
with tf.TemporaryFile(mode="w+", encoding="utf-8") as f1:
    f1.write("111\n")
    f1.write("222\n")
    f1.write("333\n")
    # 将f1的文件指针指向文件的头部
    f1.seek(0)
    content = f1.read()
    print(content)
    fname1 = f1.name

fname1 = pathlib.Path(fname1)
if fname1.exists():
    print("文件存在")
else:
    print("文件已经被自动删除")

print("-" * 10)
print("-" * 10)
# 非自动删除的临时文件的创建
fname2 = ""
with tf.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as f2:
    fname2 = f2.name
    f2.write("dasondo1")
    f2.seek(0)
    content = f2.read()
    print(content)

fname2 = pathlib.Path(fname2)
if fname2.exists():
    print("文件存在")
else:
    print("文件已经被自动删除")


print("-" * 10)
# 2、临时目录的创建
dirs = ""
with tf.TemporaryDirectory() as f:
    # dirs=f
    print(f)
    dir_obj = pathlib.Path(f)
    print(dir_obj)
    dir_obj = dir_obj / "some"
    dir_obj.mkdir()
    lists = dir_obj.iterdir()
    print(lists)
    dirs = f


dirs = pathlib.Path(dirs)
if dirs.exists():
    print("存在")
else:
    print("不存在")
