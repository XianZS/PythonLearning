# from b import function_b
# import b

# (1)import 整个包
#   （缺点）包中的函数过多时，会花费时间在导入之上
# (2)延迟导入
#   （缺点）不在文件开头导入，不利于管理
# (3)将引发循环导入的部分抽离出来，放到另外一个模块之中


def function_a():
    # （延迟导入）
    # 在使用时导入
    from b import function_b

    print("function_a")
