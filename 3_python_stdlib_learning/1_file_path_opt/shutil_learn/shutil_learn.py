"""
shutil标准库：
1、文件和目录的复制
（1）文件的复制
（2）目录的复制
2、文件和目录的移动和重命名
（1）文件的移动和重命名
（2）目录的移动和重命名
3、目录的删除
以递归删除目录
4、压缩包操作
创建压缩包
解压压缩包
"""

import shutil

# 1、文件的复制
# 不复制元数据：仅仅对内容进行拷贝
shutil.copy("test.txt", "copy_test.txt")
# 复制元数据：对元数据（所属者，创建时间，权限），以及内容
shutil.copy2("test.txt", "copy_test_2.txt")
# 目录的复制：默认进行递归性的复制
# shutil.copytree("./test_dir", "./copt_test_dir")
# 2、文件和目录的移动和重命名工作
# 文件的移动和重命名
# shutil.move("./move_test.txt", "./copt_test_dir/")
# shutil.move("./copt_test_dir/move_test.txt", "./new_name.txt")
# 目录的移动和重命名
# shutil.move("./copt_test_dir/", "./copy_test_dir/")
# 3、目录的删除
# shutil.rmtree("./copy_test_dir")
# 4、压缩包处理
# 创建压缩包
# make_archive("压缩包名","压缩包格式","压缩对象")
shutil.make_archive("压缩包", "zip", "./test_dir/")
# shutil.unpack_archive("压缩包对象","解压路径")
shutil.unpack_archive("压缩包.zip", "./some")
#
#
#
#
#
#
#
