# PythonLearning

> Welcome！A comprehensive Python learning repository!

## 一、Python基础学习部分

| 模块顺序                           | 核心讲解内容                                                 |
| ---------------------------------- | ------------------------------------------------------------ |
| 1. 入门引导（破冰）                | ① Python是什么/能做什么（爬虫、数据分析、自动化等场景可视化展示）；<br />② 环境搭建（Windows/Mac/Linux三系统适配，Anaconda+PyCharm安装，解决“安装报错”痛点）；<br />③ 第一个程序（Hello World+个性化改造，比如输出自己的名字，增强代入感） |
| 2. 变量与数据类型                  | ① 变量定义（命名规则+禁忌，避坑：中文变量、关键字命名）；<br />② 基础数据类型（int/float/str/bool，每个类型配2个生活化案例：比如str处理姓名、int计算工资）；<br />③ 类型转换（强制转换+自动转换，易错点：str转int的格式问题）；<br />④ 实操练习：记录个人信息（姓名、年龄、薪资）并打印 |
| 3. 运算符与表达式                  | ① 算术运算符（+/-/*//%**，案例：计算购物折扣、工资个税（简化版））；<br />② 赋值运算符（=/:=等，避坑：连续赋值的优先级）；<br />③ 比较运算符（==/!=/>/<，案例：判断成绩是否及格）；<br />④ 逻辑运算符（and/or/not，案例：判断是否满足“成年且有收入”）；<br />⑤ 实操练习：简易计算器（实现加减乘除） |
| 4. 流程控制（核心基础）            | ① if-elif-else（案例：成绩分级、判断闰年）；<br />② for循环（遍历字符串/列表，案例：批量打印姓名）；<br />③ while循环（条件循环，案例：倒计时、猜数字游戏（1-100））；<br />④ 循环控制（break/continue，避坑：循环嵌套的缩进问题）；⑤ 实操练习：猜数字游戏（加入容错机制，输入非数字不崩溃） |
| 5. 函数基础                        | ① 函数定义与调用（def关键字、参数、返回值）；<br />② 参数类型（位置参数、关键字参数、默认参数，避坑：参数顺序）；<br />③ 函数嵌套（简单嵌套，案例：计算复杂公式）；<br />④ 匿名函数（lambda，案例：简单计算）；<br />⑤ 实操练习：封装“成绩判断函数”“计算面积函数” |
| 6. 数据结构（列表/元组/字典/集合） | ① 列表（创建/增删改查，案例：购物清单管理）；<br />② 元组（不可变特性，案例：记录身份证号/坐标）；<br />③ 字典（键值对，案例：学生信息管理（姓名-成绩））；<br />④ 集合（去重/交集并集，案例：筛选重复数据）；<br />⑤ 避坑：列表索引越界、字典键不可变；<br />⑥ 实操练习：学生成绩管理系统（增删改查） |
| 7. 文件操作                        | ① 打开/关闭文件（open函数、with语句，避坑：忘记关闭文件）；<br />② 文本文件读写（read/readline/write，案例：读取成绩文件、写入日志）；<br />③ CSV文件基础读写（案例：批量导入学生信息）；<br />④ 实操练习：将学生成绩写入CSV文件并读取 |
| 8. 异常处理                        | ① 异常概念（try-except-finally）；<br />② 常见异常（ValueError/TypeError/FileNotFoundError等）；<br />③ 自定义异常（简单案例）；<br />④ 实操练习：优化猜数字游戏/计算器（加入异常捕获，避免崩溃） |
| 9. 基础综合实战                    | ① 项目：简易通讯录（实现增删改查+文件保存）；<br />② 代码复盘：梳理核心知识点+常见错误；<br />③ 作业布置：优化通讯录（添加搜索功能） |

### 代码文件

- [1_Variables_and_Data_Types.py](python_basic_learning/1_Variables_and_Data_Types.py)：变量和数据类型
- [2_Operators_and_Expressions.py](python_basic_learning/2_Operators_and_Expressions.py)：运算符和表达式
- [3_process_control.py](python_basic_learning/3_process_control.py)：流程控制
- [4_Function_Basics.py](python_basic_learning/4_Function_Basics.py)：函数基础
- [5_container_structure.py](python_basic_learning/5_container_structure.py)：容器结构
- [6_file_operate.py](python_basic_learning/6_file_operate.py)：文件操作
- [7_try_except.py](python_basic_learning/7_try_except.py)：异常处理
- [8_module.py](python_basic_learning/8_module.py)：模块

### 学习文档

-  [1_Python_数据类型分类详解.md](python_basic_learning\word\1_Python 数据类型分类详解.md) 
-  [2_Python_运算符核心类型及使用规则详解.md](python_basic_learning\word\2_Python 运算符核心类型及使用规则详解.md) 
-  [3_Python_流程控制语句及其应用详解.md](python_basic_learning\word\3_Python 流程控制语句及其应用详解.md) 
-  [4_Python_函数基础：掌握代码复用的关键.md](python_basic_learning\word\4_Python 函数基础：掌握代码复用的关键.md) 
-  [5_Python_四大核心数据结构整合示例：从基础用法到综合应用.md](python_basic_learning\word\5_Python 四大核心数据结构整合示例：从基础用法到综合应用.md) 
-  [6_Python_文件操作：从基础到进阶的分步讲解.md](python_basic_learning\word\6_Python 文件操作：从基础到进阶的分步讲解.md) 
-  [7_Python_异常处理：从基础认知到最佳实践.md](python_basic_learning\word\7_Python 异常处理：从基础认知到最佳实践.md) 
-  [8_Python_模块与包：从浅入深的模块化讲解.md](python_basic_learning\word\8_Python 模块与包：从浅入深的模块化讲解.md) 

## 二、Python进阶学习部分

| 模块顺序                               | 核心讲解内容                                                 |
| -------------------------------------- | ------------------------------------------------------------ |
| 1. 函数进阶                            | ① 可变参数（*args/**kwargs，案例：批量处理不确定数量的参数）；<br />② 装饰器（基础原理+语法糖，案例：函数计时、日志记录）；<br />③ 生成器（yield关键字，案例：批量生成数据，解决内存占用问题）；<br />④ 迭代器（iter/next，对比生成器区别）；<br />⑤ 避坑：装饰器嵌套顺序、生成器惰性求值；<br />⑥ 实操练习：用装饰器优化之前的通讯录项目（添加日志） |
| 2. 面向对象编程（OOP）                 | ① 类与对象（定义/实例化，案例：创建“学生类”“教师类”）；<br />② 封装/继承/多态（核心特性，案例：学生类继承“人类”，重写方法）；<br />③ 类属性与实例属性（避坑：属性名冲突）；<br />④ 魔术方法（__init__/__str__/__repr__等，案例：优化类的打印输出）；<br />⑤ 实操练习：用OOP重构通讯录项目（创建Contact类，实现封装） |
| 3. 模块化与包管理                      | ① 模块导入（import/from...import，避坑：循环导入、模块路径问题）；<br />② 自定义模块（将通讯录项目拆分为多个模块：业务逻辑/文件操作/异常处理）；<br />③ 包的创建（__init__.py作用）；<br />④ 虚拟环境（venv创建，解决依赖冲突）；<br />⑤ PyPI发布（简单演示，可选）；<br />⑥ 实操练习：拆分通讯录为模块化项目，创建虚拟环境 |
| 4. 数据处理基础（衔接标准库/第三方库） | ① 字符串进阶处理（正则表达式基础，re模块，案例：提取文本中的手机号/邮箱）；<br />② 日期时间处理（datetime模块，案例：日志时间格式化、计算日期差）；<br />③ 数据序列化（json模块，案例：将通讯录数据转为JSON保存）；<br />④ 实操练习：批量提取文本中的联系方式并保存为JSON |
| 5. 网络编程基础                        | ① HTTP协议基础（请求/响应，GET/POST方法）；<br />② urllib库使用（案例：简单爬取网页文本）；<br />③ requests库（第三方，简化请求，案例：爬取天气数据）；<br />④ 避坑：反爬基础（User-Agent设置）；<br />⑤ 实操练习：爬取本地城市天气并保存为文本 |
| 6. 数据库编程                          | ① SQLite基础（内置数据库，无需安装，案例：创建学生成绩数据库）；<br />② SQL基础语句（增删改查，CRUD）；<br />③ Python操作SQLite（sqlite3模块，案例：将通讯录数据存入数据库）；<br />④ MySQL入门（可选，pymysql库，案例：批量插入数据）；<br />⑤ 避坑：SQL注入、数据库连接关闭；<br />⑥ 实操练习：用数据库替代文件，优化通讯录项目 |
| 7. 并发编程入门                        | ① 线程与进程（概念区别，GIL全局解释器锁）；<br />② threading模块（线程创建，案例：多线程下载图片）；<br />③ multiprocessing模块（进程创建，案例：多进程处理数据）；<br />④ 避坑：线程安全问题、GIL对CPU密集型任务的影响；<br />⑤ 实操练习：多线程爬取多个网页的天气数据 |
| 8. 进阶综合实战（2个项目，覆盖多模块） | ① 项目1：简易爬虫+数据可视化（爬取某平台商品价格，用matplotlib绘图，覆盖网络请求、数据处理、可视化）；<br />② 项目2：学生成绩管理系统（升级版，覆盖OOP、数据库、模块化、异常处理）；<br />③ 每个项目分“需求分析→代码实现→优化复盘”3个视频 |
| 9. 进阶阶段复盘与方向指引              | ① 核心知识点梳理（思维导图形式）；<br />② 常见错误汇总与解决方案；<br />③ 后续方向指引（数据分析/爬虫/自动化/后端开发） |

### 代码文件

- [1_super_struct.py](python_advance_learning/1_super_struct.py)：高级数据结构
- [2_advance_function.py](python_advance_learning/2_advance_function.py)：高级函数

### 学习文档

-  [1_Python_高级数据结构之 collections 模块详解.md](python_advance_learning\word\1_Python 高级数据结构之 collections 模块详解.md) 
-  [2_Python_函数进阶：深入剖析迭代器与生成器.md](python_advance_learning\word\2_Python 函数进阶：深入剖析迭代器与生成器.md) 

## 三、Python标准库学习部分（核心目标：熟练运用标准库解决实际问题，减少第三方库依赖）

| 模块顺序（按使用频率排序）                  | 核心讲解内容                                                 |
| ------------------------------------------- | ------------------------------------------------------------ |
| 1. sys/os模块（系统交互核心）               | ① sys：命令行参数（sys.argv）、退出程序（sys.exit）、获取系统信息（sys.platform）；<br />② os：路径处理（os.path/Pathlib，重点，避坑：跨平台路径问题）、文件夹操作（创建/删除/遍历）、系统命令调用（os.system）；<br />③ 实操练习：批量重命名文件、遍历指定文件夹下的所有CSV文件 |
| 2. datetime模块（时间处理唯一选择）         | ① 时间对象（datetime.datetime/datetime.date）；<br />② 时间格式化（strftime/strptime，重点，避坑：格式符错误）；<br />③ 时间计算（timedelta，案例：计算距离生日还有多少天）；<br />④ 时区处理（简单入门，pytz库辅助）；<br />⑤ 实操练习：生成每日日志文件名（包含日期）、计算项目耗时 |
| 3. json/csv模块（数据序列化高频）           | ① json：dump/dumps/load/loads（案例：保存配置文件、接口数据处理）；<br />② csv：reader/writer/DictReader（案例：批量导入/导出表格数据）；<br />③ 避坑：json中文编码问题、csv换行符问题；<br />④ 实操练习：将数据库中的学生成绩导出为CSV/JSON文件 |
| 4. re模块（正则表达式，文本处理必备）       | ① 正则基础语法（元字符、量词、分组）；<br />② 常用方法（match/search/findall/sub，案例：提取文本中的URL、替换敏感词）；<br />③ 避坑：贪婪匹配/非贪婪匹配、转义字符问题；<br />④ 实操练习：批量清洗文本数据（去除空格、提取关键信息） |
| 5. urllib模块（网络请求基础，无第三方依赖） | ① urlopen（简单GET请求）；<br />② Request对象（设置请求头、POST请求）；<br />③ 异常处理（HTTPError/URLError）；<br />④ 案例：爬取简单网页、获取接口数据；<br />⑤ 实操练习：爬取股票行情简单数据并保存为JSON |
| 6. logging模块（日志记录，项目必备）        | ① 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）；<br />② 日志配置（基本配置、输出到文件、格式化日志）；<br />③ 案例：为学生成绩管理系统添加日志（记录操作行为、错误信息）；<br />④ 避坑：日志重复输出、编码问题；<br />⑤ 实操练习：优化之前的项目，添加完整日志功能 |
| 7. collections模块（高级数据结构补充）      | ① 常用子类（defaultdict、OrderedDict、Counter、deque）；<br />② 案例：Counter统计词频、deque实现队列（高效）；<br />③ 对比普通数据结构（dict/list）的优势；<br />④ 实操练习：统计文本词频并排序 |
| 8. 其他高频辅助模块（按需选讲）             | ① random模块（随机数生成，案例：抽奖程序、随机密码生成）；<br />② math模块（数学计算，案例：几何计算、三角函数）；<br />③ hashlib模块（加密，案例：密码加密存储）；<br />④ 实操练习：生成随机密码并加密保存 |
| 9. 标准库综合实战                           | ① 项目：批量数据处理工具（覆盖os/sys/json/csv/re/logging模块，实现批量读取文件、清洗数据、保存结果、记录日志）；<br />② 代码复盘：梳理各模块协同逻辑；<br />③ 作业布置：优化工具，添加自定义配置功能 |
