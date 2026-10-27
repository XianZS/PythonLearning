"""
pathlib标准库学习：
1、路径的获取
（1）获取当前用户路径
（2）获取当前工作目录
2、路径的操作
（1）路径拼接
（2）获取各个属性部分 文件名-含后缀-文件后缀-父目录
3、文件和路径的基础操作
（1）是否存在/是否是文件/路径
（2）创建目录
（3）创建文件
（4）重命名/移动文件
（5）删除文件/目录
4、目录遍历和文件查找
（1）遍历当前目录
（2）匹配当前目录文件
（3）递归匹配所有子目录
5、简化文件读写操作
（1）快速读文件
（2）快速写文件
"""

# import pathlib
from pathlib import Path

# 1、路径的获取
p1 = Path("./test.txt")
print(f"object:{p1},type:{type(p1)}")

# XianZS
p2 = Path.home()
print(f"home:{p2}")

# 获取当前工作路径 pwd
p3 = Path.cwd()
# os.getcwd()
print(f"当前的工作路径为:{p3}")

# 2、路径操作
# 路径拼接
p4 = Path("/user/admin")
print(f"p4:{p4}")

# /user/admin/download/xunlei
p5 = p4 / "download" / "xunlei"
print(f"拼接之后的路径为：{p5}")
p6 = p5 / "main.py"
print(p6)
# 得到拼接之后的各个属性部分
file_basename1 = p6.name
file_basename2 = p6.stem
file_houzhui = p6.suffix
file_father_dir = p6.parent
print(f"文件名:{file_basename1}；{file_basename2}")
print(f"文件类型:{file_houzhui}")
print(f"文件的父目录:{file_father_dir}")


# 3、路径判断和文件系统操作
# 路径和文件是否存在的判断
p7 = Path("./test.txt")  # p7对象真实存在
if p7.exists():
    print("p7对象存在")
else:
    print("p7不存在")

if p4.exists():
    print("p4对象存在")
else:
    print("p4不存在")


# 判断是文件还是路径
def judge(obj):
    if obj.is_file():
        print("它是文件")
    else:
        if obj.is_dir():
            print("它是目录")
        else:
            print("无法判断")


judge(p7)
judge(p4)
p8 = Path.cwd()
judge(p8)


print("-" * 10)
# 创建目录
create_dir_1 = Path("data")
create_dir_2 = create_dir_1 / "input"
create_dir_2.mkdir(parents=True, exist_ok=True)
# 创建文件
create_file_1 = create_dir_2 / "input.txt"
create_file_1.touch(exist_ok=True)
# 如何进行重命名文件
# file_1 = Path("./data/input/input.txt")
# print(file_1)
# file_1.rename("./data/input/new_input.txt")
# file_2 = Path("./data/input/new_input.txt")
# file_2.rename("./data/new_input.txt")
# 首先对文件进行复制，将复制样本放置到本地缓存之中
# 然后再确定复制样本的存储位置
# 判断复制样本的存储位置和源文件的存储位置是否相同
# 相同：覆盖源文件
# 不同：复制源文件
# 删除文件
# obj_new_input = Path("./data/new_input.txt")
# obj_new_input.unlink()
# 相当于os.remove()方法
# 目录删除
dir_obj = Path("./data/some/")
if dir_obj.exists():
    dir_obj.rmdir()
    # 更推荐使用 shutil.rmtree()
else:
    print("目录不存在")


# 4、目录遍历和文件查找
# 主要替代了 os.walk()
base_dir = Path("test_project")
(base_dir / "src").mkdir(parents=True, exist_ok=True)
(base_dir / "docs").mkdir(exist_ok=True)
(base_dir / "src" / "main.py").touch()
(base_dir / "src" / "utils.py").touch()
(base_dir / "docs" / "readme.md").touch()
(base_dir / "notes.txt").touch()

print("-" * 10)
# 循环遍历当前路径下的内容（非递归形式）
for item in base_dir.iterdir():
    print(item, type(item))

print("-" * 10)
# 在当前目录下找到所有的txt文件（非递归形式）
for txt_file in base_dir.glob("*.txt"):
    print(txt_file)

print("-" * 10)
# 在当前目录下找到所有的python文件（递归形式）
for py_file in base_dir.glob("*.py"):
    print(py_file)

# 5、简化文件的读写操作
file_path = Path("readme.txt")
# 文件的写入操作
file_path.write_text("hello world\nthis is two line")

# 文件的读操作
res = file_path.read_text(encoding="utf-8")
print(res)
