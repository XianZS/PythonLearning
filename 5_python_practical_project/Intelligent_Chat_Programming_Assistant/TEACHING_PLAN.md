# 🤖 DeepSeek AI 聊天助手 — 30 天教学大纲

> **适用人群**：有 Python 基础的初学者（了解函数、`pip install`、类的基本概念即可）
> **每集时长**：20-35 分钟
> **最终产出**：一个完整的 Streamlit + DeepSeek API AI 聊天应用，支持流式对话与思维链推理
> **项目总行数**：约 850 行 Python 代码，分布在 9 个源文件中

---

## 九阶段总览

| 阶段 | 天数 | 核心主题 | 产出文件 |
|---|---|---|---|
| ① 环境与项目搭建 | Day 1-4 | Python 环境、Git、项目骨架 | 项目目录、requirements.txt、.gitignore |
| ② 配置与安全 | Day 5-7 | API 密钥、环境变量、配置模块 | `.env.example`、`src/config.py` |
| ③ API 客户端开发 | Day 8-12 | OpenAI SDK、流式生成器、异常处理 | `src/deepseek_client.py` |
| ④ Streamlit 入门 | Day 13-16 | 执行模型、Markdown、CSS、chat_input | `app.py`（骨架）、`src/ui/utils.py` |
| ⑤ 聊天 UI 渲染 | Day 17-20 | 消息气泡、折叠面板、欢迎页 | `src/ui/chat_area.py` |
| ⑥ 会话状态管理 | Day 21-24 | Session State、消息 CRUD、Token 估算 | `src/chat_manager.py` |
| ⑦ 侧边栏控件 | Day 25-27 | 参数调节、模型选择、会话管理 | `src/ui/sidebar.py` |
| ⑧ 流式处理与整合 | Day 28-29 | 占位符更新、模块编排 | `src/stream_handler.py`、`app.py`（完整） |
| ⑨ 项目发布 | Day 30 | README、GitHub、课程回顾 | `README.md` |

---

## 第一阶段：环境与项目搭建

### Day 1：课程概述 + Python 环境检测

#### 🎯 教学目标
- 观看最终成品演示，建立整体认知
- 确认本地 Python 版本 ≥ 3.8
- 理解 Python 版本号的含义（3.8 vs 3.11 vs 3.12）

#### 📝 知识点
- **Python 版本选择**：3.11 是目前平衡稳定性和性能的最佳选择
- **为什么不用最新版**：部分第三方库可能尚未适配
- **`python --version`**：终端中查看当前 Python 版本

#### 🛠️ 实操步骤

```bash
# 确认 Python 已安装且版本 ≥ 3.8（本课程推荐 3.11）
# --version 参数让 python 打印当前安装的版本号
python --version
# 预期输出：Python 3.11.x 或 Python 3.12.x

# 确认 pip（Python 包管理器）可用
# pip 是 Python 的标准包安装工具，用于从 PyPI 下载和安装第三方库
pip --version
```

#### 🎬 视频要点（~25min）
1. **开场（3min）**：直接运行最终成品，演示流式对话 + 思维链推理，给观众一个"学完能做出什么"的直观感受
2. **架构预告（5min）**：用一张图提前展示整个项目的模块结构（9 个文件），让观众有全局视野——但强调"每天只攻一个模块，30 天后全部拿下"
3. **环境检测（10min）**：带观众一起执行 `python --version`，解释如何判断版本是否满足要求
4. **常见问题（5min）**：Python 未安装怎么办？装了多个版本怎么办？

#### 📌 课后作业
- 确认 `python --version` 输出 ≥ 3.8
- 如果版本不对，去 [python.org](https://python.org) 下载 3.11 版本

---

### Day 2：虚拟环境 — conda 创建与激活

#### 🎯 教学目标
- 理解虚拟环境的概念和必要性
- 使用 conda 创建项目专属虚拟环境
- 掌握 `conda create`、`conda activate`、`conda deactivate`

#### 📝 知识点
- **虚拟环境是什么**：一个隔离的 Python 运行环境，各项目的依赖互不干扰
- **为什么需要它**：项目 A 需要 streamlit==1.28，项目 B 需要 streamlit==1.35，全局安装会冲突
- **conda vs venv**：conda 管理 Python 版本 + 包；venv 只管理包（本项目用 conda）
- **环境名 `PythonLearning`**：你可以自定义，但整个教程统一用这个名字

#### 🛠️ 实操步骤

```bash
# 1. 创建虚拟环境（指定 Python 3.11 版本）
# -n PythonLearning: 将环境命名为 PythonLearning（可自定义）
# python=3.11: 指定在此环境中使用的 Python 版本
# -y: 自动确认所有提示，无需手动输入 yes
conda create -n PythonLearning python=3.11 -y

# 2. 激活虚拟环境
# 激活后，命令行前缀会出现 (PythonLearning) 标识
# 激活后所有 python/pip 命令都指向该虚拟环境内的版本
conda activate PythonLearning

# 3. 验证——注意命令行前面出现 (PythonLearning) 前缀
python --version    # 应显示 Python 3.11.x
# pip 的路径应位于虚拟环境目录下（如 .../envs/PythonLearning/...）
pip --version

# 4. 退出虚拟环境（学完后才知道怎么退出）
conda deactivate
```

#### 🎬 视频要点（~20min）
1. **比喻引入（3min）**：虚拟环境 = 给每个项目一间独立的厨房，锅碗瓢盆互不串味
2. **实操（12min）**：从创建到激活到验证，每一步展示终端输出
3. **常见坑（3min）**：PowerShell 中 conda 命令找不到？需要先运行 `conda init powershell`

#### 📌 课后作业
- 成功创建 `PythonLearning` 环境并激活
- 尝试 `conda env list` 查看所有环境

---

### Day 3：项目目录 + 依赖安装

#### 🎯 教学目标
- 建立标准项目目录结构
- 理解 `requirements.txt` 的作用和写法
- 用 pip 安装项目依赖
- 理解每个依赖的用途

#### 📝 知识点
- **项目结构约定**：`src/` 放源代码，`app.py` 是入口，`requirements.txt` 声明依赖
- **`requirements.txt` 格式**：`包名>=最低版本`
- **`pip install -r requirements.txt`**：一键安装所有依赖
- **三个核心依赖**（本项目只用了 3 个）：
  - `openai>=1.0.0` — 调用 DeepSeek API（DeepSeek 兼容 OpenAI 接口格式）
  - `streamlit>=1.28.0` — Web UI 框架，把 Python 代码变成网页
  - `python-dotenv>=1.0.0` — 读取 `.env` 文件中的密钥配置

#### 🛠️ 实操步骤

```bash
# 确保虚拟环境已激活
conda activate PythonLearning

# 创建项目目录结构
# 创建项目根目录
mkdir Intelligent_Chat_Programming_Assistant
# 进入项目目录
cd Intelligent_Chat_Programming_Assistant
# -p 参数：递归创建多级目录，如果父目录不存在则自动创建
# 这里创建 src/ui/ 两层目录
mkdir -p src/ui

# 创建 requirements.txt 文件（依赖声明文件）
# > 重定向输出：创建新文件（覆盖已有内容）
echo "openai>=1.0.0" > requirements.txt
# >> 追加重定向：在文件末尾追加内容
echo "streamlit>=1.28.0" >> requirements.txt
echo "python-dotenv>=1.0.0" >> requirements.txt

# 一键安装 requirements.txt 中声明的所有依赖
# -r requirements.txt: 从文件中读取包列表
pip install -r requirements.txt

# 验证安装：列出已安装的包并筛选出 3 个直接依赖
# | 管道符：将左边命令的输出传递给右边命令
# grep -E: 使用扩展正则表达式匹配包含 openai 或 streamlit 或 dotenv 的行
pip list | grep -E "openai|streamlit|dotenv"
```

#### 🎬 视频要点（~22min）
1. **目录结构讲解（5min）**：在白板上画出 `app.py` → `src/` → `src/ui/` 的层次关系
2. **依赖讲解（7min）**：三个包各自做什么——openai 发请求、streamlit 画界面、dotenv 读密钥
3. **安装演示（8min）**：展示 `pip install` 过程，解释"间接依赖"——安装了 3 个包，实际下载了十几个

#### 📌 课后作业
- 确认 `pip list` 能显示 3 个直接依赖
- 运行 `streamlit hello` 验证 Streamlit 安装成功（会打开一个演示页面）

---

### Day 4：Git 初始化 + .gitignore

#### 🎯 教学目标
- 初始化 Git 仓库
- 编写 `.gitignore` 排除不该提交的文件
- 完成第一次 commit

#### 📝 知识点
- **版本控制**：Git 记录每次修改，方便回溯和协作
- **`.gitignore`**：告诉 Git 哪些文件/目录不要跟踪
- **必须忽略的文件**：
  - `__pycache__/` — Python 自动生成的字节码缓存
  - `.env` — 包含真实 API 密钥，绝对不能泄露
  - `venv/`、`.conda/` — 虚拟环境文件夹（太大，且其他人应自己创建）
  - `*.pyc` — 编译后的 Python 字节码

#### 📄 创建文件

**.gitignore**：
```
# ===== Python 编译缓存 =====
# Python 导入模块时自动生成的字节码缓存目录，每个 .py 文件对应一个 .pyc
__pycache__/
# 编译后的 Python 字节码文件，运行时由解释器自动生成，不应纳入版本控制
*.pyc

# ===== 环境变量（包含真实 API 密钥） =====
# .env 文件存放真实的 API 密钥等敏感信息，绝对不能提交到 Git 仓库
# 一旦泄露，任何人都可以用你的密钥调用 DeepSeek API，产生费用
.env

# ===== 虚拟环境 =====
# Python 虚拟环境目录，体积大且包含平台相关的二进制文件
# 其他开发者应该通过 requirements.txt 自行创建环境
venv/
# conda 虚拟环境缓存目录
.conda/

# ===== IDE 配置 =====
# VS Code 的工作区配置（settings.json、launch.json 等），属于个人偏好
.vscode/
# JetBrains IDE（PyCharm 等）的项目配置目录
.idea/
```

#### 🛠️ 实操步骤

```bash
# 进入项目目录
cd Intelligent_Chat_Programming_Assistant
# 初始化 Git 仓库：在当前目录创建 .git 隐藏文件夹，开始版本控制跟踪
git init
# 将当前目录下的所有文件添加到暂存区（staging area）
# . 表示当前目录，Git 会自动根据 .gitignore 规则排除不应跟踪的文件
git add .
# 将暂存区的内容提交为一个快照，附带提交说明
# -m 后面是本次提交的描述信息
# "init:" 前缀是常见的 commit message 规范，表示初始化相关的提交
git commit -m "init: 项目初始化"
```

#### 🎬 视频要点（~18min）
1. **安全警告（5min）**：强调 `.env` 绝对不能提交——GitHub 上每小时都有爬虫在扫描泄露的 API 密钥
2. **实操（10min）**：创建 `.gitignore` → `git init` → `git add` → `git commit`

#### 📌 课后作业
- 确认 `git log` 能看到第一次 commit
- 确认 `.env` 在 `.gitignore` 中（即使还没有创建 `.env` 文件）

---

## 第二阶段：配置与安全

### Day 5：API 密钥 — 概念与获取

#### 🎯 教学目标
- 理解 API 密钥的本质（身份凭证）
- 注册 DeepSeek 开放平台并获取密钥
- 了解 DeepSeek 的计费模式

#### 📝 知识点
- **API（Application Programming Interface）**：程序与程序之间的交互接口。在这里，你的 Python 代码通过 API 调用 DeepSeek 的大模型
- **API 密钥**：一串以 `sk-` 开头的字符，用于验证"你是谁"。类似于银行卡号 + 密码
- **DeepSeek 开放平台**：https://platform.deepseek.com/api_keys
- **计费模式**：按 token 计费，注册赠送免费额度（足够学完整个课程）

#### 🛠️ 实操步骤

1. 浏览器打开 https://platform.deepseek.com
2. 注册账号（手机号即可）
3. 进入「API Keys」页面，点击「创建 API Key」
4. 复制密钥（以 `sk-` 开头，只显示一次！）

#### 🎬 视频要点（~22min）
1. **API 概念讲解（8min）**：用"餐厅点餐"比喻——你（客户端）→ 菜单（API 文档）→ 服务员（API）→ 厨房（DeepSeek 模型）
2. **注册演示（5min）**：屏幕录像展示注册和获取密钥的全流程
3. **安全提醒（5min）**：密钥只显示一次，必须马上保存；不要截图发朋友圈

#### 📌 课后作业
- 注册 DeepSeek 账号并获取 API Key
- 将密钥暂时保存在记事本中（明天会用到）

---

### Day 6：`.env` 文件 — 安全存储密钥

#### 🎯 教学目标
- 理解环境变量的概念
- 创建 `.env` 文件存储 API 密钥
- 使用 `python-dotenv` 加载环境变量
- 区分 `.env`（机密）和 `.env.example`（模板）

#### 📝 知识点
- **环境变量**：操作系统级别的键值对配置，程序运行时可以读取
- **`.env` 文件**：项目级别的环境变量文件，用 `KEY=VALUE` 格式存储
- **`python-dotenv` 的 `load_dotenv()`**：自动查找并加载 `.env` 文件，将其中的键值对注入 `os.environ`
- **双文件策略**：
  - `.env` — 存真实密钥，已在 `.gitignore` 中排除，不会提交到 GitHub
  - `.env.example` — 存示例占位符，提交到 GitHub，告诉别人需要哪些变量

#### 📄 创建文件

**.env.example**（提交到 Git）：
```bash
# ===== DeepSeek API 密钥配置模板 =====
# 这是一个示例文件，提交到 Git 仓库供其他开发者参考
# 获取方式：访问 https://platform.deepseek.com/api_keys 注册并创建 Key
# 注意：这里的值只是占位符，真实密钥请写入 .env 文件（已在 .gitignore 中排除）
DEEPSEEK_API_KEY=example-key
```

**.env**（本地文件，不提交）：
```bash
# ===== DeepSeek API 密钥（真实值） =====
# 此文件仅存在于本地，不会被 Git 跟踪（已在 .gitignore 中排除）
# 将下面等号右边的值替换为你在 DeepSeek 开放平台获取的真实密钥（以 sk- 开头）
DEEPSEEK_API_KEY=sk-你的真实密钥
```

#### 🐍 临时测试脚本（`test_env.py`，演示后删除）

```python
# 导入操作系统接口模块，用于读取环境变量
import os
# 从 python-dotenv 库导入 load_dotenv 函数
from dotenv import load_dotenv

# 自动查找当前工作目录下的 .env 文件，将其中的键值对加载到 os.environ 中
# 这样后续代码就能通过 os.environ 访问 .env 中定义的变量
load_dotenv()

# 从环境变量中读取 DEEPSEEK_API_KEY 的值
# 使用 .get() 方法而非 os.environ["DEEPSEEK_API_KEY"] 下标访问的好处是：
# 如果环境变量不存在，.get() 返回 None，而下标访问会抛出 KeyError 异常导致程序崩溃
api_key = os.environ.get("DEEPSEEK_API_KEY")
# 打印密钥的前5个字符 + *** 进行脱敏处理，防止在终端中完全暴露密钥
# api_key[:5] 取字符串前5个字符（如 "sk-31"）
print(f"读取到的密钥：{api_key[:5]}***（已脱敏）")
```

运行：
```bash
# 运行测试脚本，验证能正确从 .env 文件读取密钥
python test_env.py
# 预期输出：读取到的密钥：sk-31***（已脱敏）
# 如果输出 None 或空白，说明 .env 文件路径不对或格式有问题
```

#### 🎬 视频要点（~25min）
1. **`os.environ` 讲解（5min）**：`os.environ` 就是一个字典，`load_dotenv()` 把 `.env` 文件的内容"注入"进去
2. **双文件策略（5min）**：`.env.example` = 说明书（告诉别人需要什么），`.env` = 保险箱（存真密钥）
3. **实操（10min）**：创建两个文件 → 运行测试脚本 → 确认读取成功
4. **安全检查（3min）**：确认 `.env` 在 `.gitignore` 中，`git status` 不显示它

#### 📌 课后作业
- 创建 `.env` 和 `.env.example`
- 用 `python test_env.py` 验证能正确读取
- `git status` 确认 `.env` 未被 Git 跟踪

---

### Day 7：`config.py` — 配置管理模块

#### 🎯 教学目标
- 创建 `src/__init__.py` 和 `src/config.py`
- 集中管理所有配置常量（API 地址、模型 ID、默认参数）
- 实现密钥读写函数（`get_api_key`、`set_api_key`）
- 实现配置校验函数（`validate_config`）
- 理解 Python 模块和包的概念

#### 📝 知识点
- **`__init__.py`**：标记一个目录为 Python 包（package），可以为空文件
- **常量命名规范**：大写 + 下划线（`DEFAULT_MODEL`、`MAX_MAX_TOKENS`）
- **`load_dotenv()` 的调用时机**：在模块顶层调用一次即可
- **`os.environ.get(key)` vs `os.environ[key]`**：前者返回 `None`（键不存在），后者抛出 `KeyError`
- **元组返回模式**：`return (True, "成功")` 或 `return (False, "失败原因")`

#### 📄 创建文件（完整代码，一次性写完）

**src/__init__.py**（标记 src 为 Python 包，暂时为空，Day 29 将填充公共 API 导出）：
```python
```

**src/config.py**：
```python
"""配置管理：从环境变量读取 API 密钥和默认设置

本模块在导入时自动加载 .env 文件，并提供：
1. API 配置常量（Base URL、模型标识）
2. 模型元数据字典（名称、描述、是否支持思维链）
3. 默认参数常量（Temperature、Max Tokens 等）
4. 密钥管理函数（读取、运行时设置）
5. 配置校验函数（多层防御性校验）
6. 模型查询工具函数
"""
import os
from typing import Optional
from dotenv import load_dotenv

# 模块导入时自动执行一次：查找并加载 .env 文件到 os.environ
# 这样后续代码就可以直接通过 os.environ 读取环境变量
load_dotenv()

# ==================== API 配置 ====================

# DeepSeek API 的基础地址
# 虽然使用 OpenAI SDK，但将 base_url 指向 DeepSeek 的服务器
# 这是 DeepSeek 兼容 OpenAI 接口格式的关键——换一个 URL 就能切换服务商
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ==================== 模型标识 ====================

# deepseek-v4-flash：快速、经济的轻量模型，适合日常对话
MODEL_FLASH = "deepseek-v4-flash"
# deepseek-v4-pro：高性能模型，支持思维链推理，适合编程、数学等复杂任务
MODEL_PRO = "deepseek-v4-pro"

# ==================== 模型元数据 ====================

# 模型字典：键是模型标识（发给 API 用的机器名），值是该模型的元信息（给人看的）
# 这种设计将"机器可读"和"人类可读"分离，方便 UI 展示和逻辑判断
MODELS: dict[str, dict] = {
    MODEL_FLASH: {
        "name": "DeepSeek V4 Flash",              # 显示在下拉框中的中文名称
        "description": "快速、经济实惠的通用模型，适合日常对话",  # 鼠标悬停时的描述
        "supports_thinking": False,                # 不支持思维链推理
    },
    MODEL_PRO: {
        "name": "DeepSeek V4 Pro",
        "description": "高性能模型，支持思维链推理，适合复杂任务",
        "supports_thinking": True,                 # 支持思维链推理
    },
}

# ==================== 默认参数 ====================

# 默认使用的模型——选择 Flash 因为更快更便宜，适合大多数日常场景
DEFAULT_MODEL = MODEL_FLASH
# Temperature 默认值 0.7：在创造性和确定性之间的平衡点
# 0.0 = 完全确定（适合代码生成），2.0 = 最大随机性（适合创意写作）
DEFAULT_TEMPERATURE = 0.7
# 单次回复的最大 Token 数，4096 已足够大多数对话场景
DEFAULT_MAX_TOKENS = 4096
# 滑块最小值：至少 256 Token，避免回复过短不完整
MIN_MAX_TOKENS = 256
# 滑块最大值：8192 Token，DeepSeek 单次输出的上限
MAX_MAX_TOKENS = 8192
# 滑块的步长：每次拖动增加/减少 256 Token
TOKEN_STEP = 256

# ==================== Token 估算常量 ====================

# 当估算的 Token 数超过 50000 时，在侧边栏显示警告
# DeepSeek V4 支持 128K 上下文，50000 是一个保守的提醒阈值
TOKEN_WARNING_THRESHOLD = 50000
# 保守估算：中文约 1.5-2 字符/Token，英文约 4 字符/Token
# 取 2 字符/Token 是"宁可多估、不可少估"的策略
CHARS_PER_TOKEN = 2


# ==================== 密钥管理 ====================

def get_api_key() -> Optional[str]:
    """获取 API 密钥（优先读取环境变量）
    
    返回值可能为 None（用户既没有设置 .env 文件，
    也没有在侧边栏输入密钥），调用方需要判空。
    """
    return os.environ.get("DEEPSEEK_API_KEY")


def set_api_key(api_key: str) -> None:
    """运行时设置 API 密钥（用户从侧边栏输入时调用）
    
    将用户输入的密钥写入 os.environ，覆盖 .env 中的值。
    这样即使 .env 中没有配置密钥，用户也可以从 UI 输入。
    注意：这个修改只在当前进程有效，不会写回 .env 文件。
    """
    os.environ["DEEPSEEK_API_KEY"] = api_key


# ==================== 配置校验 ====================

def validate_config() -> tuple[bool, str]:
    """校验配置是否就绪，返回 (是否有效, 说明信息)
    
    三层防御性校验，从外到内逐层过滤常见错误：
    1. 密钥是否为空（用户忘记配置）
    2. 是否使用了示例值 your_api_key_here（复制了模板但没改值）
    3. 密钥格式是否正确（DeepSeek 密钥统一以 'sk-' 开头）
    
    Returns:
        tuple[bool, str]: (是否有效, 说明信息)
            - (True, "✅ 配置就绪") —— 一切正常
            - (False, "⚠️ ...") —— 有问题，第二个元素描述原因
    """
    api_key = get_api_key()
    # 第一层：密钥不存在
    if not api_key:
        return False, "⚠️ 请设置 DEEPSEEK_API_KEY（通过 .env 文件或侧边栏输入）"
    # 第二层：使用了模板中的示例值而非真实密钥
    if api_key == "your_api_key_here":
        return False, "⚠️ 请将 .env 中的 DEEPSEEK_API_KEY 替换为你的真实密钥"
    # 第三层：密钥格式校验——DeepSeek 的密钥统一以 sk- 开头
    if not api_key.startswith("sk-"):
        return False, "⚠️ API 密钥格式不正确，DeepSeek 密钥应以 'sk-' 开头"
    return True, "✅ 配置就绪"


# ==================== 模型查询 ====================

def get_model_label(model_id: str) -> str:
    """获取模型的显示名称（中文）
    
    用于 st.selectbox 的 format_func 参数：
    把机器标识 "deepseek-v4-flash" 转换为人类可读的 "DeepSeek V4 Flash"
    
    MODELS.get(model_id, {}) 的两层兜底：
    - 第一层：model_id 不存在于 MODELS 字典 → 返回空字典 {}
    - 第二层：空字典没有 "name" 键 → 返回原始的 model_id 字符串
    这样即使传入了未知的模型 ID，也不会崩溃，而是直接显示原始标识
    """
    return MODELS.get(model_id, {}).get("name", model_id)


def supports_thinking(model_id: str) -> bool:
    """判断模型是否支持思维链模式
    
    目前仅 deepseek-v4-pro 支持思维链推理，
    deepseek-v4-flash 不支持。
    此函数用于控制侧边栏"思维链推理"开关的 disabled 状态。
    """
    return MODELS.get(model_id, {}).get("supports_thinking", False)
```

#### 🐍 验证

```bash
# 测试 config 模块是否能正常导入
# -c 参数：告诉 Python 执行后面引号中的代码（而非运行一个 .py 文件）
# 先导入 get_api_key 和 validate_config 函数，然后调用 validate_config() 打印结果
python -c "from src.config import get_api_key, validate_config; print(validate_config())"
```

#### 🎬 视频要点（~30min）
1. **包的概念（5min）**：`src/` 目录 + `__init__.py` = 一个 Python 包，可以被 `from src.xxx import yyy` 导入
2. **常量讲解（8min）**：逐行解释 `MODELS` 字典的设计——键是机器标识，值是给人看的元数据
3. **`validate_config` 的三层校验（8min）**：密钥为空 → 用了示例值 → 格式不对，逐层防御
4. **`MODELS.get(model_id, {}).get("name", model_id)` 的两层兜底（5min）**：模型不存在时返回原始 ID 而非崩溃

#### 📌 课后作业
- 在 `validate_config()` 中添加第四层校验：密钥长度至少 32 个字符
- 用三种不同的 `.env` 配置（空、假密钥、真密钥）分别运行验证脚本

---

## 第三阶段：API 客户端开发

### Day 8：OpenAI SDK 初探 — 第一次 API 调用

#### 🎯 教学目标
- 理解 OpenAI SDK 的兼容性设计
- 创建 DeepSeek API 客户端
- 发起第一次对话请求（非流式）

#### 📝 知识点
- **SDK（Software Development Kit）**：封装了 HTTP 请求细节的工具包，让你用 Python 函数调用 API
- **`OpenAI(api_key=..., base_url=...)`**：创建客户端实例。默认 `base_url` 指向 OpenAI，改为 `https://api.deepseek.com` 即可调用 DeepSeek
- **`chat.completions.create()`**：对话补全 API，传入消息列表，返回模型回复
- **消息格式**：`[{"role": "user", "content": "你好"}]`

#### 📄 创建文件（临时版，后续升级）

**src/deepseek_client.py**：
```python
"""DeepSeek API 客户端封装

本模块封装了对 DeepSeek API 的调用逻辑，对外暴露简洁的函数接口。
调用方不需要知道底层用的是 OpenAI SDK，也不需要处理 HTTP 细节。
"""
from openai import OpenAI
from .config import DEEPSEEK_BASE_URL


def _create_client(api_key: str) -> OpenAI:
    """创建 DeepSeek API 客户端

    以下划线 _ 开头表示这是模块内部使用的"私有函数"，
    外部使用者不应直接调用它——这是 Python 社区的约定。
    
    通过 OpenAI 类创建客户端，但将 base_url 指向 DeepSeek 服务器，
    这是 DeepSeek 兼容 OpenAI 接口格式的核心技巧：
    同一个 SDK，改一个 URL，就能调用不同的模型服务商。
    """
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def chat_once(api_key: str, prompt: str) -> str:
    """发送一次对话，返回回复文本（非流式，仅用于学习）

    这是最简单的 API 调用方式：发送一个用户消息，等待完整回复。
    缺点：用户需要等待整个回复生成完毕才能看到内容，体验不好。
    后续课程会升级为流式版本 chat_stream()。

    Args:
        api_key: DeepSeek API 密钥（以 sk- 开头）
        prompt: 用户输入的问题文本

    Returns:
        模型回复的完整文本（Markdown 格式）
    """
    client = _create_client(api_key)

    # 调用对话补全 API
    response = client.chat.completions.create(
        model="deepseek-v4-flash",  # 使用 Flash 模型（快速、经济）
        messages=[{"role": "user", "content": prompt}],  # 消息列表，这里只有一条用户消息
        temperature=0.7,  # 创造性参数：0.7 是较为平衡的默认值
        max_tokens=4096,  # 限制回复最大长度，防止单次回复消耗过多 Token
    )

    # response 是 ChatCompletion 对象，结构为：
    # response.choices[0].message.content
    # - choices: 模型生成的候选回复列表（通常只有 1 个）
    # - message: 消息对象，包含 role 和 content
    # - content: 实际的回复文本
    return response.choices[0].message.content
```

#### 🐍 临时测试

```bash
# 第一次真正调用 DeepSeek API，验证整个链路是否通畅
# -c 执行多行 Python 代码（用双引号包裹，内部支持换行）
python -c "
# 手动加载 .env 文件中的环境变量
from dotenv import load_dotenv
load_dotenv()
import os
# 导入我们刚写的 chat_once 函数
from src.deepseek_client import chat_once
# 用环境变量中的密钥发起一次真实的 API 调用
# os.environ['DEEPSEEK_API_KEY'] 获取密钥（注意：这里用下标访问，确定密钥存在）
reply = chat_once(os.environ['DEEPSEEK_API_KEY'], '用一句话介绍Python')
# 打印 AI 的回复
print(reply)
"
```

#### 🎬 视频要点（~28min）
1. **为什么用 OpenAI SDK 调 DeepSeek（5min）**：OpenAI 定义了 API 格式的"行业标准"，DeepSeek 兼容它——换 `base_url` 即可，代码不用改
2. **逐行讲解（12min）**：`_create_client` 返回的是什么？`response.choices[0].message.content` 这个路径为什么这么长？
3. **首次调用（8min）**：运行测试，看到 AI 回复的那一刻——这是整个课程的里程碑时刻

#### 📌 课后作业
- 用 `chat_once()` 发送 5 个不同的问题
- 尝试修改 `temperature` 为 0.0 和 1.5，感受回复差异

---

### Day 9：配置校验函数补完

#### 🎯 教学目标
- 回顾 Day 7 的 `config.py`，确保理解每个函数
- 补充：`validate_config` 为什么需要三层校验
- 练习：给 `config.py` 添加单元测试风格的验证代码

#### 📝 知识点
- **防御性编程**：不信任任何外部输入（包括 `.env` 文件和用户输入）
- **校验的层次**：存在性 → 内容合法性 → 格式正确性
- **`os.environ.get()` 的安全用法**：永远用 `get()` 而非 `[]`，避免 KeyError

#### 🛠️ 实操步骤

在 `config.py` 所在目录创建 `test_config.py`（演示后删除）：

```python
"""config 模块的简单验证

这个脚本手动测试 validate_config() 的四种典型场景，
确保每种情况下的返回值都符合预期。
这不是正式的单元测试，而是教学用的验证脚本。
"""
import os
from src.config import validate_config, set_api_key

# ==== 测试 1：环境变量中没有 DEEPSEEK_API_KEY ====
# 先用 .pop() 移除可能存在的环境变量（第二个参数 None 表示键不存在也不报错）
os.environ.pop("DEEPSEEK_API_KEY", None)
valid, msg = validate_config()
print(f"测试1（无密钥）: {valid=}, {msg=}")
# 预期：valid=False，因为密钥为空
assert not valid

# ==== 测试 2：密钥是示例占位符 "your_api_key_here" ====
# 模拟初学者常见错误——复制了 .env.example 但忘了修改值
set_api_key("your_api_key_here")
valid, msg = validate_config()
print(f"测试2（示例值）: {valid=}, {msg=}")
# 预期：valid=False，因为使用了模板占位符
assert not valid

# ==== 测试 3：密钥格式错误（不以 sk- 开头） ====
# 模拟用户输入了错误格式的密钥
set_api_key("invalid-key-format")
valid, msg = validate_config()
print(f"测试3（格式错）: {valid=}, {msg=}")
# 预期：valid=False，因为不以 'sk-' 开头
assert not valid

# ==== 测试 4：正确的密钥格式 ====
# 模拟一切正常的情况
set_api_key("sk-correct-key-format-12345")
valid, msg = validate_config()
print(f"测试4（正确）: {valid=}, {msg=}")
# 预期：valid=True，密钥格式正确
assert valid

print("\n全部测试通过！")
```

#### 🎬 视频要点（~22min）
1. **回顾 Day 7（5min）**：快速过一遍 `config.py` 的所有常量和函数
2. **测试驱动讲解（12min）**：跑 4 个测试用例，观察每种情况下的返回值——"让代码自己证明自己正确"
3. **补充 `your_api_key_here` 检测（3min）**：这是一个常见的初学者陷阱——复制了 `.env.example` 但忘了改值

#### 📌 课后作业
- 独立写出 4 个测试用例，不需要看教程代码
- 思考：还需要增加哪些校验？（提示：密钥长度、特殊字符）

---

### Day 10：Generator 生成器 — Python 进阶特性

#### 🎯 教学目标
- 理解 Generator（生成器）与普通函数的区别
- 掌握 `yield` 关键字的使用
- 理解 Generator 的惰性求值特性

#### 📝 知识点
- **普通函数 vs Generator**：普通函数 `return` 一次性返回，Generator `yield` 逐步产出
- **`yield` 的执行模型**：函数执行到 `yield` 时暂停，下次迭代从暂停处继续
- **`for ... in generator`**：自动调用 `next()`，直到 `StopIteration`
- **为什么流式 API 需要 Generator**：服务端逐 token 推送，客户端逐 token 消费

#### 🐍 演示代码（理解 Generator）

```python
# ===== 示例 1：普通函数 =====
# 使用 return 一次性返回整个列表
def get_numbers():
    # 整个列表在内存中一次性创建并返回
    return [1, 2, 3, 4, 5]

# ===== 示例 2：Generator（等价但惰性求值） =====
# 使用 yield 逐个产出值，不一次性占用全部内存
def generate_numbers():
    for i in range(1, 6):
        # 每次 yield 时打印，方便观察执行时机
        print(f"产出: {i}")
        # yield 暂停函数执行，将值返回给调用方
        # 下次调用 next() 时，从 yield 的下一行继续执行
        yield i

# ===== 对比两种调用方式 =====
print("普通函数：")
# get_numbers() 被调用时立即执行整个函数体
# 返回完整的列表 [1, 2, 3, 4, 5]
nums = get_numbers()
print(nums)  # 输出：[1, 2, 3, 4, 5]

print("\nGenerator：")
# generate_numbers() 被调用时不会执行函数体中的任何代码
# 它只是返回一个生成器对象，等待被迭代
gen = generate_numbers()
# next() 驱动生成器执行到第一个 yield，返回 1
print(next(gen))          # 输出：产出: 1 \n 1
# 再次 next() 从上次暂停处继续，执行到下一个 yield
print(next(gen))          # 输出：产出: 2 \n 2
# 可以用 next() 逐个取值，直到生成器耗尽（抛出 StopIteration 异常）
# 更常见的是用 for 循环自动处理 next() 和 StopIteration
# for num in generate_numbers():
#     print(num)
```

#### 🎬 视频要点（~25min）
1. **用生活类比（5min）**：普通函数 = 厨师一次性上齐所有菜；Generator = 旋转寿司，来一个吃一个
2. **代码演示（15min）**：逐步执行 `next(gen)`，展示每次 `yield` 时的"暂停-恢复"
3. **内存优势（3min）**：Generator 不需要一次把所有数据加载到内存

#### 📌 课后作业
- 用 Generator 实现一个 `fibonacci(n)` 函数，每次 `yield` 一个斐波那契数
- 思考：流式聊天为什么需要 Generator？

---

### Day 11：`chat_stream()` — 流式对话生成器

#### 🎯 教学目标
- 将非流式 `chat_once()` 升级为流式 `chat_stream()`
- 解析流式响应的 chunk 结构
- 理解 `delta.content` 和 `delta.reasoning_content`

#### 📝 知识点
- **`stream=True`**：让 API 以 SSE（Server-Sent Events）方式逐步推送
- **chunk（数据块）**：流式响应的最小单位，每个 chunk 包含一小段文本
- **`delta.content`**：本 chunk 中的新文本（普通回复）
- **`delta.reasoning_content`**：本 chunk 中的推理文本（思维链，仅 V4 Pro）
- **`getattr(delta, "reasoning_content", None)`**：安全获取可能不存在的属性

#### 📄 重写 `deepseek_client.py`

```python
"""DeepSeek API 客户端封装：流式对话与异常处理

本模块是 API 通信层，负责：
1. 创建并配置 DeepSeek API 客户端
2. 以流式（stream）方式发送对话请求
3. 将 API 返回的原始 chunk 转换为统一的字典格式
4. 对所有已知异常类型进行友好处理

设计原则：
- 调用方不需要知道底层 SDK 是什么（封装变化）
- 错误在模块内部处理，不会向上传播导致 UI 崩溃
- Generator 模式让调用方可以逐 chunk 消费，实现打字机效果
"""
from collections.abc import Generator
# 从 OpenAI SDK 导入所有需要捕获的异常类型
from openai import OpenAI, AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError
from .config import DEEPSEEK_BASE_URL, MODEL_FLASH, MODEL_PRO


def _create_client(api_key: str) -> OpenAI:
    """创建 DeepSeek API 客户端
    
    私有函数，仅模块内部使用。
    将 OpenAI SDK 的客户端指向 DeepSeek 的服务器地址，
    这是 DeepSeek 兼容 OpenAI 接口格式的关键。
    """
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def chat_stream(
    api_key: str,
    message: list[dict[str, str]],
    model: str = MODEL_FLASH,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    enable_thinking: bool = False,
) -> Generator[dict, None, None]:
    """流式对话生成器

    使用 yield 逐步产出 API 响应的每个 chunk，让调用方可以实时更新 UI。
    每个 chunk 是一个统一格式的字典，包含 type 字段标识类型。

    Yields:
        字典，type 字段可能为：
        {"type": "reasoning", "text": "..."}   — 思维链推理片段（仅 V4 Pro）
        {"type": "content",   "text": "..."}   — 回复内容片段（逐 Token）
        {"type": "done",      "usage": {...}}  — 流结束信号
        {"type": "error",     "message": "..."} — 错误信息（中文友好提示）
    """
    try:
        client = _create_client(api_key)

        # 构建 API 调用的参数
        kwargs: dict = {
            "model": model,
            "messages": message,
            "stream": True,        # 关键参数：开启流式响应模式
            "max_tokens": max_tokens,
        }

        # 思维链模式处理：仅 deepseek-v4-pro 支持
        # 思维链参数需要通过 extra_body 传递（这不是 OpenAI 标准参数，而是 DeepSeek 扩展的）
        if enable_thinking and model == MODEL_PRO:
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
            # 注意：思维链模式下 API 不接受 temperature 参数
            # 因为推理过程需要确定性，不需要随机性
        else:
            kwargs["temperature"] = temperature

        # 发起流式 API 请求
        # response 是一个可迭代对象，每个元素是响应流中的一个 chunk
        response = client.chat.completions.create(**kwargs)

        for chunk in response:
            # 安全获取 delta 对象：先检查 choices 列表是否非空
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta is None:
                continue  # 空 chunk，跳过

            # 获取思维链内容（reasoning_content 是 DeepSeek 扩展字段）
            # 使用 getattr 安全获取：如果 delta 对象没有 reasoning_content 属性，返回 ""
            # 这比直接访问 delta.reasoning_content 更安全，后者的属性不存在时会抛出 AttributeError
            reasoning = getattr(delta, "reasoning_content", None) or ""
            if reasoning:
                yield {"type": "reasoning", "text": reasoning}

            # 获取普通回复内容（标准 OpenAI 字段）
            if delta.content:
                yield {"type": "content", "text": delta.content}

        # 所有 chunk 处理完毕，发送完成信号
        yield {"type": "done", "usage": None}

    # ===== 异常分类处理 =====
    # 注意：这里不 raise 异常，而是 yield 一个 error 类型的字典
    # 因为 Generator 中 raise 会导致调用方的 for 循环崩溃
    # yield 错误让调用方可以优雅地展示错误信息后继续运行

    except AuthenticationError:
        # HTTP 401: API 密钥无效或过期
        yield {"type": "error", "message": "🔑 API 密钥无效，请检查后重试。可以前往 platform.deepseek.com/api_keys 获取密钥。"}
    except RateLimitError:
        # HTTP 429: 请求频率超限（免费用户每分钟 50 次）
        yield {"type": "error", "message": "⏳ API 请求频率超限，请稍等片刻后重试。"}
    except APITimeoutError:
        # 请求超时（默认 60 秒无响应）
        yield {"type": "error", "message": "⏰ 请求超时，请检查网络连接后重试。"}
    except APIConnectionError:
        # 网络连接失败（DNS 解析失败、网络不通等）
        yield {"type": "error", "message": "🌐 无法连接到 DeepSeek 服务器，请检查网络连接。"}
    except Exception as e:
        # 兜底异常处理：捕获所有未被上述具体异常捕获的情况
        # 注意捕获顺序：必须从具体到宽泛，如果把 except Exception 放最前面，
        # 后面的具体异常捕获永远无法执行
        error_msg = str(e)
        if "status_code" in error_msg and "400" in error_msg:
            # HTTP 400: 请求参数错误（如历史消息中包含了 reasoning_content 字段）
            yield {"type": "error", "message": "⚠️ 请求参数错误，请尝试清除对话历史后重试。"}
        elif "status_code" in error_msg and "500" in error_msg:
            # HTTP 500: 服务器内部错误（通常是临时问题，等一会重试）
            yield {"type": "error", "message": "⚠️ DeepSeek 服务器内部错误，请稍后重试。"}
        else:
            # 未知错误：返回原始错误信息，方便排查
            yield {"type": "error", "message": f"❌ 发生未知错误：{error_msg}"}
```

删除之前的 `chat_once()` 函数。

#### 🎬 视频要点（~30min）
1. **`stream=True` 的效果（5min）**：对比 Day 8 的非流式（等 3 秒一口气返回）vs 流式（逐字蹦出）
2. **chunk 结构解析（8min）**：拿一个真实响应，拆解每个 chunk 的内部结构
3. **`extra_body` 参数（5min）**：为什么思维链模式用 `extra_body` 传参？（因为这不是 OpenAI 原生参数）
4. **`getattr` 安全访问（3min）**：`reasoning_content` 不是标准字段，用 `getattr` 防止 AttributeError
5. **Generator 类型注解（3min）**：`Generator[dict, None, None]` 三个参数的含义

#### 📌 课后作业
- 写一个循环 `for chunk in chat_stream(...)` 打印所有 chunk，观察输出格式
- 分别用 V4 Flash 和 V4 Pro（开 thinking）测试，对比响应差异

#### 🧪 测试验证

```bash
python tests/test_day11_deepseek_client.py
```

测试覆盖：chat_stream 正常流式输出、思维链 reasoning chunk、思维链 extra_body 传参、
AuthenticationError / RateLimitError / HTTP 400 / HTTP 500 异常处理、默认模型常量。

---

### Day 12：异常处理 — 让错误信息友好

#### 🎯 教学目标
- 识别 5 种 OpenAI SDK 异常类型
- 理解 `try/except` 的捕获顺序（具体 → 宽泛）
- 理解在 Generator 中用 `yield` 错误而不是 `raise` 的原因
- 处理 HTTP 状态码错误（400、500）

#### 📝 知识点
- **异常类型与含义**：

| 异常类型 | HTTP 状态码 | 触发场景 |
|---|---|---|
| `AuthenticationError` | 401 | API 密钥无效 |
| `RateLimitError` | 429 | 请求频率超限（免费用户 50次/分钟） |
| `APITimeoutError` | — | 服务器响应超时（默认 60s） |
| `APIConnectionError` | — | 网络不通或 DNS 解析失败 |
| 通用 `Exception` | 400 | 请求参数错误（如 history 太长） |
| 通用 `Exception` | 500 | 服务器内部错误 |

- **为什么 Generator 中不 `raise`**：调用方在 `for` 循环中消费 Generator，如果 `raise`，整个循环崩溃。`yield error` 让调用方优雅处理
- **异常捕获顺序**：先捕获具体异常（`AuthenticationError`），最后捕获 `Exception`（兜底）

> 📝 代码已在 Day 11 的 `chat_stream()` 中写好了 try/except 块，本节课专门讲解异常处理的原理。

#### 🎬 视频要点（~25min）
1. **故意触发错误（12min）**：
   - 用假密钥 → `AuthenticationError`
   - 改 `base_url` 为一个不通的地址 → `APIConnectionError`
   - 每种错误展示对应的中文提示
2. **异常捕获顺序（5min）**：如果把 `except Exception` 放在最前面会怎样？（后面的捕获永远不会执行）
3. **错误信息设计原则（5min）**：每条错误信息包含三要素——emoji 图标、中文说明、解决建议

#### 📌 课后作业
- 故意用错误的 `base_url` 触发 `APIConnectionError`
- 思考：还有什么异常场景没有被覆盖？

#### 🧪 测试验证

Day 12 无新增代码——本节讲解 Day 11 中已写好的异常处理逻辑。
运行 Day 11 测试确认异常处理正确：

```bash
python tests/test_day11_deepseek_client.py
```

其中 4 个异常测试覆盖全部 6 种异常类型。详见 `tests/test_day12_exceptions.py`。

---

## 第四阶段：Streamlit 入门

### Day 13：Streamlit 执行模型 — Rerun 循环

#### 🎯 教学目标
- 理解 Streamlit 的核心执行模型（rerun 循环）
- 创建第一个 `app.py`
- 使用 `st.set_page_config()` 配置页面

#### 📝 知识点
- **Streamlit 的执行模型**：每次用户交互（点击按钮、输入文字），整个 Python 脚本从头到尾重新执行一遍
- **这与传统 Web 框架完全不同**：Django/Flask 是请求-响应模式；Streamlit 是脚本重跑模式
- **`st.set_page_config()` 必须是第一个 Streamlit 调用**：否则报错
- **参数说明**：
  - `page_title`：浏览器标签页标题
  - `page_icon`：标签页图标（emoji）
  - `layout`：`"wide"` 宽屏 / `"centered"` 居中
  - `initial_sidebar_state`：`"expanded"` 默认展开 / `"collapsed"` 折叠

#### 📄 创建文件

**app.py**（Day 13 版本，最简骨架）：
```python
"""DeepSeek AI 聊天助手 — 主程序入口

这是整个应用的最简骨架版本，仅包含：
1. Streamlit 页面基础配置
2. 标题和描述
3. 聊天输入框
后续课程会逐步添加侧边栏、聊天历史、流式响应等功能。
"""
import streamlit as st

# ⚠️ set_page_config 必须是第一个 Streamlit 调用
# 必须放在任何其他 st.xxx() 调用之前，否则 Streamlit 会抛出异常
st.set_page_config(
    page_title="DeepSeek AI 助手",  # 浏览器标签页显示的标题
    page_icon="🤖",                  # 标签页图标（可以用 emoji 或图片 URL）
    layout="wide",                   # 宽屏布局，填满整个浏览器宽度
    initial_sidebar_state="expanded",  # 侧边栏默认展开
)

# 页面大标题
st.title("🤖 DeepSeek AI 聊天助手")
# 标题下方的副标题描述
st.markdown("基于 DeepSeek V4 大模型，支持流式对话与思维链推理")

# 聊天输入框：出现在页面底部
# st.chat_input() 返回用户输入的文本，如果还没输入则返回 None
# := 是"海象运算符"：同时完成赋值和判断，等价于：
#   prompt = st.chat_input("输入你的问题...")
#   if prompt:
#       ...
if prompt := st.chat_input("输入你的问题..."):
    # 将用户输入显示为粗体文本
    st.markdown(f"你说：**{prompt}**")
```

#### 🛠️ 运行

```bash
# 启动 Streamlit 开发服务器，运行 app.py
# streamlit run 会启动一个本地 Web 服务器，默认监听 http://localhost:8501
# 浏览器会自动打开该地址，展示应用界面
# 按 Ctrl+C 可以停止服务器
streamlit run app.py
```

#### 🎬 视频要点（~22min）
1. **Rerun 演示（10min）**：输入文字 → 按 Enter → 脚本重跑 → 新内容出现。用 `st.write("rerun!")` 证明每次都在重跑
2. **`:=` 海象运算符（5min）**：`if prompt := st.chat_input(...)` 等价于 `prompt = st.chat_input(...)` + `if prompt:`，但更简洁
3. **页面配置（5min）**：逐一修改 `page_title`、`layout` 等参数，展示效果变化

#### 📌 课后作业
- 修改 `page_icon` 为 🚀，修改 `layout` 为 `"centered"`，感受差异
- 在 `app.py` 中添加 `st.write(f"页面加载次数：{st.session_state.get('count', 0)}")` 观察 rerun 次数

#### 测试验证

Day 13 创建 app.py 骨架，验证方式是启动 Streamlit 开发服务器：

```bash
streamlit run app.py
```

详见 `tests/test_day13_streamlit_skeleton.py` 中的完整验证清单。

---

### Day 14：`st.markdown()` — Markdown 与 HTML 渲染

#### 🎯 教学目标
- 掌握 `st.markdown()` 的各种用法
- 理解 `unsafe_allow_html=True` 的作用和安全含义

#### 📝 知识点
- **`st.markdown()` 三种用法**：
  1. Markdown 文本：`st.markdown("**粗体** *斜体*")`
  2. HTML 标签：`st.markdown("<div style='color:red'>红色文字</div>", unsafe_allow_html=True)`
  3. 多行文本：`st.markdown("""第一行\n第二行""")`
- **`unsafe_allow_html`**：默认为 `False`（安全考虑），设为 `True` 后才渲染 HTML。Streamlit 团队认为 HTML 注入有 XSS 风险

#### 🐍 演示代码（不写进最终项目，仅用于理解）

```python
# ===== 1. 纯 Markdown 用法 =====
# Streamlit 内置的 Markdown 渲染引擎，无需 unsafe_allow_html
st.markdown("## 二级标题")        # Markdown 标题语法
st.markdown("**粗体** 和 *斜体*")  # 加粗和斜体

# ===== 2. HTML 用法（需要允许不安全 HTML） =====
# 默认 unsafe_allow_html=False，出于安全考虑不渲染 HTML 标签
# 只有当你信任内容来源时才设为 True
st.markdown(
    '<div style="color: #ff6b6b; font-size: 1.5em;">红色大字</div>',
    unsafe_allow_html=True,  # 必须显式启用，否则 HTML 标签会被当作纯文本显示
)

# ===== 3. Markdown + HTML 混合使用 =====
# 在同一个 st.markdown() 中混合使用 Markdown 语法和 HTML 标签
# 利用三引号字符串（"""）编写多行内容
st.markdown("""
    ## 标题
    这是**Markdown**内容
    <div style="background: #333; padding: 10px;">
        这是 HTML 内容
    </div>
""", unsafe_allow_html=True)  # 启用后 HTML 标签才会被渲染
```

#### 🎬 视频要点（~20min）
1. **三种模式展示（10min）**：纯 Markdown、纯 HTML、混合，逐一演示效果
2. **安全机制解释（5min）**：为什么不默认允许 HTML？——防止恶意用户注入 `<script>` 标签
3. **什么时候需要 HTML（3min）**：Streamlit 原生组件不支持的样式（如颜色、边框、hover 效果）

#### 📌 课后作业
- 用 `st.markdown` 在 `app.py` 中添加一段带背景色和边框的提示文字
- 尝试不用 `unsafe_allow_html=True` 渲染 HTML，观察结果

#### 测试验证

Day 14 无新增项目代码——本节是 `st.markdown()` 的练习讲解。
参见 `tests/test_day14_markdown.py` 了解 Markdown/HTML 渲染验证方式。

---

### Day 15：`utils.py` — 自定义 CSS 注入

#### 🎯 教学目标
- 将 CSS 样式封装为独立模块
- 理解 CSS 选择器在 Streamlit 中的使用
- 使用 Chrome DevTools 定位 Streamlit 组件的 HTML 元素

#### 📝 知识点
- **注入方式**：通过 `st.markdown("<style>...</style>", unsafe_allow_html=True)` 注入 CSS
- **Streamlit 组件定位**：每个组件渲染后带有 `data-testid` 属性，可被 CSS 选择器选中
- **常见选择器**：
  - `footer` — 页脚（"Made with Streamlit"）
  - `[data-testid="stSidebar"]` — 侧边栏容器
  - `.stChatMessage` — 聊天消息气泡
  - `.block-container` — 主内容区域

#### 📄 创建文件

**src/ui/__init__.py**：
```python
"""DeepSeek AI 聊天助手 UI 模块

提供 Streamlit UI 组件：侧边栏控件、聊天区域渲染和自定义样式。

模块结构（对应教学单元）：
- utils:     自定义 CSS 样式注入
- sidebar:   侧边栏设置面板（模型选择、参数调节、会话管理）
- chat_area: 聊天区域消息渲染（Markdown、思维链折叠面板）
"""

from .utils import inject_custom_css
from .sidebar import render as render_sidebar
from .chat_area import render_all_message, render_welcome

__all__ = [
    "inject_custom_css",
    "render_sidebar",
    "render_all_message",
    "render_welcome",
]
```

**src/ui/utils.py**：
```python
"""UI 工具函数：CSS 样式注入

本模块通过 st.markdown(..., unsafe_allow_html=True) 注入自定义 CSS，
用于微调 Streamlit 默认样式或隐藏不需要的元素。
所有和样式相关的代码集中在这里，方便维护和修改。
"""
import streamlit as st


def inject_custom_css() -> None:
    """注入自定义 CSS 样式

    通过 <style> 标签向 Streamlit 页面注入 CSS 规则。
    使用 CSS 选择器精确定位 Streamlit 渲染的 HTML 元素，
    选择器通过 Chrome DevTools（F12）查看元素属性获得。

    常用选择器参考：
    - footer: Streamlit 页面底部的 "Made with Streamlit" 文字
    - [data-testid="xxx"]: Streamlit 为组件添加的数据测试属性
    - .block-container: 主内容区域的容器
    - .stChatMessage: 聊天消息气泡容器
    """
    st.markdown(
        """
        <style>
            /* 隐藏 Streamlit 默认的 "Made with Streamlit" 页脚 */
            footer { display: none; }

            /* 主内容区域顶部留出一点间距，让布局更舒适 */
            .block-container {
                padding-top: 2rem;
            }

            /* 思维链展开面板的文字样式：略小、灰色，不抢主回复的视觉焦点 */
            .streamlit-expanderHeader {
                font-size: 0.9em;
                color: #888;
            }

            /* 侧边栏 API Key 输入框使用等宽字体 */
            /* 因为密钥包含大小写字母和数字，等宽字体更容易核对 */
            [data-testid="stSidebar"] [data-testid="stTextInput"] input {
                font-family: monospace;
            }

            /* 聊天消息的上下内边距，让气泡之间不至于太拥挤 */
            .stChatMessage {
                padding: 0.5rem 1rem;
            }

            /* 建议卡片的鼠标悬停效果 */
            /* 选择所有带有 style="cursor: pointer" 的 div（即欢迎页的建议卡片） */
            /* 鼠标悬停时边框从默认色变为蓝色，配合 0.3s 过渡动画 */
            [data-testid="stMarkdownContainer"]
            div[style*="cursor: pointer"]:hover {
                border-color: #4a9eff !important;
                transition: border-color 0.3s;
            }
        </style>
        """,
        unsafe_allow_html=True,  # 必须启用，否则 <style> 标签会被当作纯文本显示
    )
```

#### 🎬 视频要点（~25min）
1. **Chrome DevTools 教学（10min）**：打开 F12 → 找到 Streamlit 渲染的 HTML → 找到 `data-testid` 属性 → 写 CSS 选择器
2. **逐条 CSS 解释（10min）**：每条规则为什么需要，注释说明
3. **模块化思想（3min）**：为什么把 CSS 放在 `utils.py` 而不是直接写在 `app.py` 里？

#### 📌 课后作业
- 用 Chrome DevTools 找到 Streamlit 聊天消息的 `data-testid`
- 添加一条 CSS 规则：修改侧边栏背景色为深灰色

#### 测试验证

```bash
python tests/test_day15_ui_utils.py
```

测试覆盖：CSS 关键规则完整性、CSS 语法正确性、`ui/__init__.py` 公共 API 导出。

---

### Day 16：`st.chat_input()` — 聊天输入框

#### 🎯 教学目标
- 理解 `st.chat_input()` 的返回值和工作原理
- 掌握 `disabled` 参数控制输入框状态
- 理解占位符文字的变化逻辑

#### 📝 知识点
- **`st.chat_input(placeholder)`**：在页面底部显示一个聊天输入框
  - 返回 `None`：用户还没有输入
  - 返回 `str`：用户按了 Enter，返回值是输入的文字
- **`disabled` 参数**：当 API 密钥未配置时，禁用输入框，防止无效请求
- **`:=` 海象运算符**：`if prompt := st.chat_input(...)` 是 Streamlit 中的标准写法

#### 📄 更新 `app.py`

```python
import streamlit as st

# ⚠️ set_page_config 必须是第一个 Streamlit 调用，放在所有导入之前
st.set_page_config(
    page_title="DeepSeek AI 助手", page_icon="🤖",
    layout="wide", initial_sidebar_state="expanded",
)

# 导入自定义模块（注意：在 set_page_config 之后导入，因为模块内部可能使用 st.xxx）
from src.ui.utils import inject_custom_css
from src.config import get_api_key, validate_config

# 注入自定义 CSS 样式（隐藏页脚、调整间距等）
inject_custom_css()

# 校验 API 密钥配置是否就绪
# valid: 布尔值，表示是否可以正常调用 API
# status_msg: 对应的提示信息（✅ 或 ⚠️）
valid, status_msg = validate_config()

# 根据配置状态决定是否禁用聊天输入框
# 密钥无效时禁用输入，防止用户发送注定失败的请求
chat_disabled = not valid

# 聊天输入框：占位符文字根据配置状态动态变化
if prompt := st.chat_input(
    # 密钥 OK → "输入你的问题..."；密钥缺失 → 提示用户去配置
    "输入你的问题..." if not chat_disabled else "请先在侧边栏配置 API 密钥",
    disabled=chat_disabled,  # 禁用状态下输入框变灰，不可交互
):
    # 用户发送消息后，在聊天气泡中显示
    # with st.chat_message(...): 创建一个聊天气泡上下文
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)  # 在气泡中使用 Markdown 渲染用户输入

# 在侧边栏顶部显示配置状态
if valid:
    st.sidebar.success(status_msg)   # 绿色 ✅ 提示
else:
    st.sidebar.warning(status_msg)   # 黄色 ⚠️ 提示
```

#### 🎬 视频要点（~20min）
1. **输入框的三种状态（8min）**：
   - API 密钥 OK → 输入框正常，"输入你的问题..."
   - API 密钥缺失 → 输入框灰色禁用，"请先在侧边栏配置 API 密钥"
   - 输入后 → 显示在用户气泡中
2. **`disabled` 参数（5min）**：为什么要在密钥缺失时禁用输入？——避免用户发送请求后看到错误
3. **状态反馈（5min）**：侧边栏的 ✅ / ⚠️ 提示

#### 📌 课后作业
- 修改代码，让禁用状态下输入框显示不同的 emoji
- 在 `.env` 中删除密钥 → 刷新页面 → 观察输入框变化 → 恢复密钥 → 再刷新

#### 测试验证

```bash
python tests/test_day16_chat_input.py
```

验证 app.py 中 chat_input 的 disabled 逻辑、动态占位符文字、密钥状态指示。
完整交互验证需启动 Streamlit（见测试文件中的手动验证步骤）。

---

## 第五阶段：聊天 UI 渲染

### Day 17：`st.chat_message()` — 消息气泡

#### 🎯 教学目标
- 使用 `st.chat_message()` 创建聊天气泡
- 区分 user 和 assistant 两种角色
- 实现 `render_message()` 函数

#### 📝 知识点
- **`st.chat_message(role, avatar)`**：Streamlit 内置的聊天消息组件
  - `role="user"`：用户消息样式（右对齐或不同背景色）
  - `role="assistant"`：助手消息样式
  - `avatar`：头像，可以是 emoji 或图片 URL
- **`with st.chat_message(...):`**：上下文管理器，`with` 块内的内容渲染在该气泡中

#### 📄 创建文件

**src/ui/chat_area.py**（上半部分）：
```python
"""聊天区域渲染：消息展示、思维链折叠、欢迎页面

本模块负责所有 UI 渲染逻辑，包括：
- render_message(): 渲染单条聊天消息气泡
- render_welcome(): 渲染无对话时的欢迎引导页
- render_all_message(): 渲染全部历史消息

渲染逻辑与数据管理分离：本模块只负责"怎么画"，不负责"数据在哪"。
数据管理由 chat_manager.py 负责。
"""
import streamlit as st
from typing import Optional


def render_message(
    role: str,
    content: str,
    reasoning_content: Optional[str] = None,
) -> None:
    """渲染单条消息气泡

    在聊天区域创建一个聊天气泡，显示消息内容和可选的思维链推理过程。

    Args:
        role: "user"（用户消息）或 "assistant"（AI 回复）
        content: 消息正文，支持 Markdown 格式渲染
        reasoning_content: 思维链推理内容（仅 assistant 角色可能有）
                           为 None 时不显示思维链面板
    """
    # 根据角色选择头像：用户用 🧑‍💻，助手用 🤖
    avatar = "🧑‍💻" if role == "user" else "🤖"

    # st.chat_message() 创建聊天气泡上下文管理器
    # with 块内的 st.xxx() 调用都会渲染在这个气泡内部
    with st.chat_message(role, avatar=avatar):
        # st.markdown 默认渲染 Markdown 内容，支持代码块、列表、加粗等
        st.markdown(content)
```

#### 🎬 视频要点（~20min）
1. **气泡对比（5min）**：分别展示 user 和 assistant 的气泡样式
2. **上下文管理器（5min）**：`with` 的用法——进入时创建气泡，退出时关闭
3. **Markdown 支持（5min）**：在消息中写 `**粗体**`、代码块等

#### 📌 课后作业
- 在 `app.py` 中手动调用 `render_message("user", "你好")` 和 `render_message("assistant", "你好，有什么可以帮你的？")` 观察效果
- 尝试用图片 URL 替代 emoji 作为 avatar

#### 测试验证

```bash
python tests/test_day17_20_chat_area.py
```

测试覆盖 Day 17-20 全部渲染函数（参见 Day 18-20 的测试验证说明）。

---

### Day 18：`st.expander()` — 思维链折叠面板

#### 🎯 教学目标
- 使用 `st.expander()` 创建可折叠内容
- 在消息气泡中嵌套折叠面板
- 用 HTML + 内联样式控制折叠面板的外观

#### 📝 知识点
- **`st.expander(label, expanded)`**：可折叠/展开的区域
  - `label`：折叠状态的标题文字
  - `expanded=False`：默认折叠；`expanded=True`：默认展开
- **嵌套组件**：`with st.chat_message(...):` 内可以放 `with st.expander(...):`
- **HTML 内联样式**：当 Streamlit 原生组件样式不够用时，用 `st.markdown(..., unsafe_allow_html=True)` 精细控制

#### 📄 更新 `render_message()`

```python
def render_message(
    role: str,
    content: str,
    reasoning_content: Optional[str] = None,
) -> None:
    # 根据角色选择头像
    avatar = "🧑‍💻" if role == "user" else "🤖"

    # 创建聊天气泡
    with st.chat_message(role, avatar=avatar):
        # ==== 思维链内容：在折叠面板中展示 ====
        # 仅当角色是 assistant 且确实有推理内容时才显示
        if reasoning_content and role == "assistant":
            # st.expander 创建一个可折叠/展开的区域
            # expanded=False: 默认折叠，用户点击标题才展开
            # 折叠时只显示 "🧠 查看思考过程"，不占用太多空间
            with st.expander("🧠 查看思考过程", expanded=False):
                # 使用 HTML + 内联样式精细控制外观
                # color: #888 — 灰色文字，与主回复区分
                # font-size: 0.9em — 比正文略小，暗示这是"辅助信息"
                # line-height: 1.6 — 增加行间距，长段落阅读更舒适
                st.markdown(
                    f'<div style="color: #888; font-size: 0.9em; '
                    f'line-height: 1.6;">{reasoning_content}</div>',
                    unsafe_allow_html=True,
                )

        # 消息正文：始终显示，支持 Markdown 格式
        st.markdown(content)
```

#### 🎬 视频要点（~18min）
1. **Expander 交互演示（5min）**：点击展开/折叠，展示两种状态
2. **HTML 样式解释（5min）**：`color: #888`（灰色文字）、`font-size: 0.9em`（略小）、`line-height: 1.6`（增加行间距）
3. **条件渲染（5min）**：只有 assistant 且有 reasoning_content 时才显示折叠面板

#### 📌 课后作业
- 尝试将 `expanded` 改为 `True`，观察默认展开效果
- 添加一个按钮，点击后将所有折叠面板同时展开

#### 测试验证

```bash
python tests/test_day17_20_chat_area.py
```

测试中 `test_render_message_has_expander` 验证思维链折叠面板的存在和条件渲染。

---

### Day 19：欢迎页面 — 引导与建议卡片

#### 🎯 教学目标
- 实现 `render_welcome()` — 无对话历史时的引导页
- 使用 `st.columns()` 创建多列布局
- 用 HTML + CSS 实现建议卡片

#### 📝 知识点
- **条件渲染策略**：有消息 → 聊天历史；无消息 → 欢迎页
- **`st.columns(n)`**：将页面分为 n 列等宽区域
- **`with cols[i]:`**：在第 i 列中渲染内容
- **建议卡片设计**：emoji + 标题 + 描述文字，hover 时边框变蓝

#### 📄 补充代码

```python
def render_welcome() -> None:
    """渲染欢迎屏幕（无对话历史时显示）

    当用户还没有发送任何消息时，显示引导页面，
    避免空白页给用户"应用坏了"的错觉。
    页面包含：标题、描述、三个建议问题卡片。
    """
    # ===== 标题区域 =====
    # 使用 HTML 实现居中和自定义字号（Streamlit 原生组件不支持）
    st.markdown(
        """
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="font-size: 2.5em; margin-bottom: 10px;">
                🤖 DeepSeek AI 聊天助手
            </h1>
            <p style="color: #888; font-size: 1.1em; margin-bottom: 30px;">
                基于 DeepSeek V4 大模型，支持流式对话与思维链推理
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ===== 示例提示词卡片区域 =====
    st.markdown("#### 💡 试试这些：")
    # 将页面分为 3 列等宽区域
    cols = st.columns(3)
    # 建议问题列表：每个元素为 (图标, 标题, 描述)
    suggestions = [
        ("📝", "帮我写一段Python代码", "用 Python 实现一个简单的 HTTP 服务器"),
        ("🔍", "解释概念", "请通俗易懂地解释什么是机器学习"),
        ("💡", "头脑风暴", "我想做一个个人博客网站，给我一些技术选型建议"),
    ]
    # 遍历建议列表，在每列中渲染一张卡片
    for i, (icon, title, desc) in enumerate(suggestions):
        # with cols[i]: 在第 i 列的上下文中渲染内容
        with cols[i]:
            # 用 HTML + 内联 CSS 创建卡片样式
            # cursor: pointer 让鼠标变为手型，暗示"可点击"
            # 鼠标悬停时的蓝色边框效果由 utils.py 中注入的 CSS 实现
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #333;       /* 深灰边框 */
                    border-radius: 10px;           /* 圆角 */
                    padding: 15px;                 /* 内边距 */
                    height: 100%;                  /* 与其他卡片等高 */
                    cursor: pointer;               /* 鼠标变为手型 */
                ">
                    <div style="font-size: 1.5em;">{icon}</div>      <!-- 图标（大号 emoji） -->
                    <div style="font-weight: bold; margin: 8px 0;">{title}</div>  <!-- 卡片标题 -->
                    <div style="color: #888; font-size: 0.85em;">{desc}</div>     <!-- 灰色描述 -->
                </div>
                """,
                unsafe_allow_html=True,
            )
```

#### 🎬 视频要点（~22min）
1. **欢迎页设计思路（5min）**：为什么需要欢迎页？——空白页会给用户"坏掉了"的错觉
2. **`st.columns` 布局（8min）**：3 列布局，每列一张卡片。对比使用 `st.columns` 和不使用（纵向堆叠）的效果
3. **CSS hover 效果（5min）**：边框从 `#333` 变为 `#4a9eff`，`transition: 0.3s` 平滑过渡
4. **观众互动（2min）**：建议观众自己设计欢迎页的样式——这没有标准答案

#### 📌 课后作业
- 修改 `suggestions` 列表，添加 3 个自己的建议问题
- 尝试用 4 列布局（`st.columns(4)`），观察卡片宽度变化

#### 测试验证

```bash
python tests/test_day17_20_chat_area.py
```

测试中 `test_render_welcome_structure` 验证欢迎页标题、3 列布局、建议卡片内容。

---

### Day 20：`render_all_message()` — 历史消息渲染

#### 🎯 教学目标
- 实现 `render_all_message()` 遍历历史消息
- 集成 `get_all_message()` 模块导入
- 理解条件渲染：欢迎页 vs 聊天历史

#### 📝 知识点
- **数据来源**：消息数据存储在 `st.session_state.message` 中（Day 21 会深入讲解）
- **`get_all_message()`**：返回消息列表（从 `chat_manager` 模块导入）
- **业务逻辑分离**：`chat_area.py` 只负责"渲染"，不负责"数据管理"

#### 📄 补充代码（`chat_area.py` 顶部添加导入）

```python
# 从父包导入 get_all_message 函数
# .. 表示上一级目录，即从 src.ui 回到 src
from ..chat_manager import get_all_message


def render_all_message() -> None:
    """渲染全部历史消息"""
    message = get_all_message()
    for msg in message:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        reasoning = msg.get("reasoning_content")
        render_message(role, content, reasoning)
```

#### 📄 更新 `app.py`

```python
from src.ui.chat_area import render_all_message, render_welcome
from src.chat_manager import init_message, get_message_count

# 在 main() 中：

# 确保消息列表已初始化（首次运行时创建空列表）
init_message()

# 根据消息数量决定显示什么：
# - 无消息 → 显示欢迎引导页（标题 + 建议卡片）
# - 有消息 → 显示完整的聊天历史
if get_message_count() == 0:
    render_welcome()
else:
    render_all_message()
```

#### 🎬 视频要点（~18min）
1. **两种页面状态切换（5min）**：无消息 → 欢迎页；有消息 → 聊天历史
2. **`get_all_message()` 导入链（5min）**：`chat_area.py` → `chat_manager.py` → `st.session_state`
3. **容错处理（5min）**：`msg.get("role", "user")` — 万一数据不完整，用默认值兜底

#### 📌 课后作业
- 手动在 `st.session_state.message` 中添加几条假消息，观察渲染效果
- 实现：当鼠标悬停在消息上时，显示删除按钮

#### 测试验证

```bash
python tests/test_day17_20_chat_area.py
```

测试中 `test_render_all_message_import` 验证 get_all_message 导入和消息遍历逻辑。

---

## 第六阶段：会话状态管理

### Day 21：`st.session_state` — Streamlit 的"记忆"

#### 🎯 教学目标
- 深入理解 `st.session_state` 的原理
- 理解为什么 Streamlit 需要 session_state
- 区分"变量"（每次 rerun 重置）和"session_state"（跨 rerun 持久）

#### 📝 知识点
- **问题根源**：Streamlit 的 rerun 模型导致所有普通 Python 变量在每次交互后重置
- **解决方案**：`st.session_state` 是一个特殊的字典，内容在多次 rerun 中保持
- **访问方式**：
  - `st.session_state.key`（属性访问）— 推荐
  - `st.session_state["key"]`（下标访问）— 也可
- **懒初始化模式**：
  ```python
  if "key" not in st.session_state:
      st.session_state.key = initial_value
  ```

#### 🐍 演示（临时代码，帮助理解）

```python
import streamlit as st

# ===== 普通 Python 变量 =====
# 每次 Streamlit rerun 时，整个脚本从头执行
# 这意味着 count_normal 每次都会被重新赋值为 0
count_normal = 0

# ===== session_state 持久变量 =====
# st.session_state 是一个特殊的字典，内容在多次 rerun 之间保持
# "懒初始化"模式：只在首次运行时创建，后续 rerun 时复用已有值
if "count_persistent" not in st.session_state:
    st.session_state.count_persistent = 0

# 点击按钮时，两个变量都 +1
if st.button("+1"):
    count_normal += 1                           # 普通变量 +1
    st.session_state.count_persistent += 1       # 持久变量 +1

# 显示两个变量的值，观察它们的差异
# 普通变量：每次 rerun 都重置为 0，所以点击后显示 1，下次又回到 0
st.write(f"普通变量: {count_normal}")
# 持久变量：值保留在 session_state 中，每次 +1 是真正累加的
st.write(f"持久变量: {st.session_state.count_persistent}")
# 结论：点击 10 次按钮后，普通变量始终显示 1，持久变量显示 10
```

#### 🎬 视频要点（~22min）
1. **对比实验（10min）**：上面这段代码，反复点击按钮，一个数永远是 1，另一个持续增长——直观展示区别
2. **原理图解（8min）**：画图解释 "rerun 时脚本从头执行，但 `session_state` 是保存在内存中的独立空间"
3. **字典 vs 属性访问（2min）**：两种写法等价，属性访问更简洁

#### 📌 课后作业
- 写一个简单的计数器应用：两个按钮分别 +1 和 -1，数值保持在 session_state 中
- 思考：如果没有 session_state，Streamlit 还能用来做什么？

#### 测试验证

Day 21 无新增项目代码——本节是 `st.session_state` 原理讲解。
参见 `tests/test_day21_session_state.py` 中的完整演示脚本，
可保存为独立 .py 文件并用 `streamlit run` 运行，直观对比普通变量与 session_state 的差异。

---

### Day 22：`chat_manager.py` — 消息存储与读写

#### 🎯 教学目标
- 创建 `chat_manager.py` 封装所有 session_state 操作
- 实现消息初始化、添加用户消息、添加助手消息
- 理解封装的价值：调用方不需要知道底层是 session_state

#### 📝 知识点
- **封装原则**：`app.py` 不应该直接操作 `st.session_state.message`，应该通过 `chat_manager` 的函数
- **消息数据结构**：
  ```python
  # 用户消息
  {"role": "user", "content": "你好"}

  # 助手消息
  {"role": "assistant", "content": "你好！", "reasoning_content": "让我想想..."}
  ```
- **`init_message()` 的懒初始化**：只在第一次调用时创建空列表

#### 📄 创建文件

**src/chat_manager.py**（上半部分）：
```python
"""会话管理：多轮对话历史、思维链裁剪、上下文限制

本模块封装了对 st.session_state.message 的全部读写操作，
是数据管理层，与 UI 渲染层（chat_area.py）完全分离。

调用方不需要知道底层是 session_state——如果以后想换成数据库存储，
只需要修改本模块，调用方的代码完全不变。
"""
from typing import Optional
import streamlit as st


# ==================== 消息初始化 ====================

def init_message() -> None:
    """初始化消息列表（如果不存在）

    使用"懒初始化"模式：只在首次调用时创建空列表。
    后续调用检测到列表已存在，不做任何操作。
    这个函数是幂等的——多次调用效果相同。
    """
    if "message" not in st.session_state:
        st.session_state.message = []


# ==================== 消息操作 ====================

def add_user_message(text: str) -> None:
    """添加用户消息到对话历史

    每次用户发送消息时调用，将用户输入追加到消息列表末尾。
    用户消息结构简单：只有 role 和 content，没有 reasoning_content。

    Args:
        text: 用户在聊天输入框中输入的文本
    """
    init_message()  # 确保消息列表已初始化（防御性编程）
    st.session_state.message.append({
        "role": "user",
        "content": text,
    })


def add_assistant_message(
    content: str,
    reasoning_content: Optional[str] = None,
) -> None:
    """添加助手回复（含可选的思维链推理内容）

    在流式响应结束后调用，将完整的助手回复持久化到消息列表。
    注意：reasoning_content 仅保存在本地 session_state 中用于展示，
    不会被发送给 API——build_api_message() 会自动裁剪掉它。

    Args:
        content: 助手回复正文（Markdown 格式，支持代码块等）
        reasoning_content: 思维链内容，仅用于本地展示，不会发给 API
                           为 None 表示该回复没有思维链推理过程
    """
    init_message()
    st.session_state.message.append({
        "role": "assistant",
        "content": content,
        "reasoning_content": reasoning_content,
    })
```

#### 🎬 视频要点（~22min）
1. **封装演示（8min）**：对比直接操作 `st.session_state.message.append(...)` vs 调用 `add_user_message(...)`——后者更清晰、更不容易出错
2. **数据结构设计（5min）**：为什么每条消息是 dict？为什么有 `reasoning_content` 字段？
3. **`Optional[str]` 类型注解（3min）**：Python 3.10+ 的 `Optional[X]` = `X | None`
4. **`init_message()` 防御性编程（3min）**：每个函数调用前都先 `init_message()`，保证不会 KeyError

#### 📌 课后作业
- 写一个辅助函数 `get_last_user_message()` 返回最近一条用户消息
- 思考：如果消息量很大（1000+ 条），当前的数据结构会有什么问题？

#### 测试验证

```bash
python tests/test_day22_24_chat_manager.py
```

测试覆盖 Day 22-24 全部函数（参见 Day 23-24 的测试验证说明）。

---

### Day 23：`chat_manager.py` — 查询、清空与 API 消息构建

#### 🎯 教学目标
- 实现消息查询函数（计数、获取全部）
- 实现 `clear_history()` 清空功能
- 实现 `build_api_message()` — 最关键的 API 消息转换

#### 📝 知识点
- **本地消息 vs API 消息**：本地消息包含 `reasoning_content`（给用户看），API 消息不能包含（协议要求）
- **DeepSeek API 的关键约束**：多轮对话时，历史 assistant 消息中的 `reasoning_content` 字段会导致 400 错误
- **消息裁剪策略**：`build_api_message()` 遍历所有消息，只保留 `role` 和 `content`

#### 📄 补充代码（`chat_manager.py` 下半部分）

```python
# ==================== 消息查询 ====================

def get_message_count() -> int:
    """当前消息总数

    用于判断是否显示欢迎页（count == 0 → 欢迎页）
    以及侧边栏的消息计数展示。
    """
    init_message()
    return len(st.session_state.message)


def get_all_message() -> list[dict]:
    """获取所有消息（含 reasoning_content，用于本地展示）

    返回完整的消息列表，包含 reasoning_content 字段。
    这个函数供 UI 渲染层（chat_area.py）使用，
    用于将对话历史渲染到页面上。

    注意：这个列表不应该直接发送给 API——
    应该使用 build_api_message() 构建 API 版本的消息列表。
    """
    init_message()
    return st.session_state.message


def clear_history() -> None:
    """清空所有对话历史

    将消息列表重置为空列表。
    调用后需要执行 st.rerun() 让页面刷新，
    否则用户看到的是旧消息（session_state 已清空但 UI 未更新）。
    """
    init_message()
    st.session_state.message = []


# ==================== API 消息构建 ====================

def build_api_message() -> list[dict[str, str]]:
    """构建发送给 DeepSeek API 的消息列表

    【关键规则 —— 踩坑总结】
    多轮对话中，如果在历史 assistant 消息中包含了 reasoning_content 字段，
    DeepSeek API 会返回 400 错误（请求参数错误）。
    原因是 reasoning_content 不是标准 OpenAI 消息格式的字段，
    DeepSeek 服务端不接受它在请求中出现。

    因此本函数遍历所有历史消息，对每条消息只保留 role 和 content，
    主动去掉 reasoning_content 字段。

    注意：由于消息是在流式结束后才持久化到 session_state 的，
    当前这条回复还未写入，所以只需要处理历史消息。
    """
    init_message()

    api_message = []
    for message in st.session_state.message:
        clean_message = {
            "role": message["role"],
            "content": message["content"],
        }
        api_message.append(clean_message)

    return api_message
```

#### 🎬 视频要点（~25min）
1. **对比实验（8min）**：`print(get_all_message())` vs `print(build_api_message())`，直观看到 `reasoning_content` 被移除
2. **为什么必须裁剪（8min）**：用 DeepSeek 官方文档截图证明——如果发送 `reasoning_content`，API 直接返回 400
3. **`clear_history()` 的 rerun（5min）**：清空后必须 `st.rerun()` 才能看到欢迎页——因为 Streamlit 不自动刷新

#### 📌 课后作业
- 构造一条含 `reasoning_content` 的假消息，验证 `build_api_message()` 是否正确裁剪
- 思考：如果 API 协议改变了，允许 reasoning_content，需要修改哪些代码？

#### 测试验证

```bash
python tests/test_day22_24_chat_manager.py
```

测试中 `test_build_api_message_strips_reasoning` 验证 API 消息裁剪逻辑——
这是整个项目最关键的规则之一：历史消息含 reasoning_content 会导致 400 错误。

---

### Day 24：Token 估算与上下文警告

#### 🎯 教学目标
- 理解 Token 的概念和估算方法
- 实现字符 → Token 的粗略转换
- 实现上下文长度警告机制

#### 📝 知识点
- **Token**：LLM 处理文本的最小单位，不是字符、不是单词。中文约 1.5-2 字符/token，英文约 4 字符/token
- **为什么估算而不是精确计算**：精确计算需要 tiktoken 等分词器，增加依赖。粗略估算对警告功能足够
- **保守策略**：取 2 字符/token（宁可多估，不可少估）
- **警告阈值**：50000 token（低于模型上限，提前提醒用户）

#### 📄 在 `src/config.py` 中已有：
```python
TOKEN_WARNING_THRESHOLD = 50000  # Token 警告阈值
CHARS_PER_TOKEN = 2              # 保守估算：2 字符 ≈ 1 token
```

#### 📄 在 `chat_manager.py` 顶部补充导入：
```python
# 将以下导入添加到 chat_manager.py 顶部（与已有的 import streamlit as st 放在一起）
from .config import CHARS_PER_TOKEN, TOKEN_WARNING_THRESHOLD


def estimate_token_count() -> int:
    """估算当前对话的总 token 数

    使用粗略的字符数 / Token 比例来估算，而不是精确计算。
    原因：精确计算需要 tiktoken 等分词库，增加依赖且对警告功能来说是过度工程。

    估算策略：
    - 中文 ~1.5-2 字符/token（中文字符信息密度高）
    - 英文 ~4 字符/token（英文单词由多个字母组成）
    - 取保守值 2 字符/token（宁可多估，不可少估）

    统计范围：
    - 所有消息的 content 字段
    - assistant 消息的 reasoning_content 字段（思维链也占用上下文窗口）

    Returns:
        估算的 Token 数量（整数）
    """
    init_message()

    total_chars = 0
    for message in st.session_state.message:
        total_chars += len(message.get("content", ""))
        if message.get("reasoning_content"):
            total_chars += len(message["reasoning_content"])

    # 整除得出粗略 Token 数（用 // 确保返回整数而不是浮点数）
    return total_chars // CHARS_PER_TOKEN


def should_warn_token_limit() -> bool:
    """是否应发出 token 限制警告

    当估算的 Token 数超过配置的阈值（默认 50000）时返回 True。
    调用方应在 UI 中展示警告，提醒用户对话已较长，
    建议清除历史或开始新对话。

    DeepSeek V4 支持 128K 上下文，50000 是一个保守的提醒阈值，
    给用户足够的缓冲空间。
    """
    return estimate_token_count() >= TOKEN_WARNING_THRESHOLD
```

#### 🎬 视频要点（~22min）
1. **Token 可视化（8min）**：用 OpenAI 的 [Tokenizer 工具](https://platform.openai.com/tokenizer) 展示一段文本被切成多少个 token——中文和英文的差异一目了然
2. **估算 vs 精确（5min）**：为什么不用 tiktoken 精确计算？——少一个依赖，够用就好
3. **警告展示（5min）**：发很多条长消息，观察 `should_warn_token_limit()` 何时变为 True
4. **上下文窗口概念（2min）**：DeepSeek V4 支持 128K 上下文，但太长的对话会变慢、变贵

#### 📌 课后作业
- 发送 3 段 1000 字的中文 + 3 段 1000 词的英文，对比估算 token 数和实际的字符数差异
- 研究 DeepSeek V4 Flash 和 V4 Pro 各自的上下文窗口大小

#### 测试验证

```bash
python tests/test_day22_24_chat_manager.py
```

测试中 `test_estimate_token_count` 和 `test_should_warn_*` 验证 Token 估算和阈值警告。

---

## 第七阶段：侧边栏控件

### Day 25：侧边栏基础 — API 密钥输入与状态

#### 🎯 教学目标
- 使用 `st.sidebar` 创建侧边栏布局
- 实现 API 密钥的密码输入框
- 实现状态指示器（✅ 配置就绪 / ⚠️ 需要配置）
- 实现运行时动态设置密钥

#### 📝 知识点
- **`st.sidebar.xxx()`**：所有 Streamlit 组件都有对应的侧边栏版本
- **`st.text_input(type="password")`**：掩码输入，不显示明文
- **`st.success()` / `st.warning()`**：状态消息组件
- **双重密钥来源**：`.env` 文件（环境变量）+ 侧边栏手动输入，侧边栏输入优先级更高

#### 📄 创建文件

**src/ui/sidebar.py**（上半部分）：
```python
"""Streamlit 侧边栏：模型选择、参数调节、会话管理

本模块负责渲染整个侧边栏 UI，包括：
1. API 密钥配置区（密码输入框 + 状态指示）
2. 模型选择区（下拉框 + 描述）
3. 对话参数区（Temperature、Max Tokens 滑块）
4. 思维链开关（条件禁用逻辑）
5. 会话管理区（消息计数、Token 估算、清空按钮）
6. 关于信息区

render() 函数返回一个包含所有用户设置值的字典，
供 app.py 中的主逻辑使用。
"""
import streamlit as st
from ..config import (
    MODELS, DEFAULT_MODEL,
    get_api_key, set_api_key, validate_config,
)


def render() -> dict:
    """渲染侧边栏，返回当前用户设置字典

    这是侧边栏的唯一公开接口。
    在 app.py 中调用一次，获取所有用户配置参数。

    Returns:
        dict: 包含 api_key, model, temperature, max_tokens, enable_thinking
    """
    st.sidebar.markdown("## ⚙️ 设置")

    # ==================== API Key 配置区 ====================
    st.sidebar.markdown("### 🔑 API 密钥")

    # 获取 .env 文件中的密钥（可能为 None）
    env_key = get_api_key()
    # 校验配置状态
    valid, status_msg = validate_config()

    # 根据校验结果显示不同的状态指示器
    if valid:
        st.sidebar.success(status_msg)       # 绿色 ✅ 提示——一切正常
    else:
        st.sidebar.warning(status_msg)       # 黄色 ⚠️ 提示——需要配置

    # 密码输入框：type="password" 将输入内容掩码显示（显示为 ***）
    # value 默认为 .env 中的值（如果有的话），方便用户看到已有配置
    api_key_input = st.sidebar.text_input(
        "DeepSeek API Key",
        type="password",                    # 密码模式，隐藏明文
        value=env_key or "",                # 如果 env_key 为 None，用空字符串
        placeholder="sk-...",              # 输入框为空时显示的灰色提示文字
        help="输入你的 DeepSeek API 密钥。可在 platform.deepseek.com/api_keys 获取。",
    )

    # 运行时更新密钥：如果用户在侧边栏输入了新的密钥
    # 且与 .env 中的不同，则覆盖环境变量中的值
    # 这样即使用户没有配置 .env，也可以从 UI 输入密钥
    if api_key_input and api_key_input != env_key:
        set_api_key(api_key_input)

    # 分割线
    st.sidebar.markdown("---")

    return {
        "api_key": api_key_input,
        # Day 26-27 继续补充其他字段
    }
```

#### 🐍 在 `app.py` 中调用：
```python
# 导入侧边栏渲染函数，使用 as 重命名为更明确的名字
from src.ui.sidebar import render as render_sidebar

# 渲染侧边栏并获取所有用户设置
settings = render_sidebar()
# 密钥优先级：侧边栏输入 > .env 环境变量
# 如果用户在侧边栏输入了密钥，使用侧边栏的；否则从环境变量读取
api_key = settings["api_key"] or get_api_key()
```

#### 🎬 视频要点（~22min）
1. **侧边栏演示（5min）**：打开/折叠侧边栏，展示组件排列
2. **密钥输入（8min）**：`type="password"` 掩码效果 → 输入密钥 → 状态变为 ✅
3. **双重密钥逻辑（5min）**：`settings["api_key"] or get_api_key()` — 侧边栏优先，环境变量兜底
4. **`help` 参数（2min）**：鼠标悬停在 ❓ 上显示帮助文字

#### 📌 课后作业
- 在侧边栏添加一个"显示/隐藏密钥"的切换按钮
- 尝试用 `st.sidebar.text_area` 替代 `text_input`

#### 测试验证

```bash
python tests/test_day25_27_sidebar.py
```

测试覆盖 Day 25-27 全部侧边栏功能（参见 Day 26-27 的测试验证说明）。

---

### Day 26：侧边栏 — 模型选择与参数滑块

#### 🎯 教学目标
- 实现模型选择下拉框
- 实现 Temperature 滑块（含条件禁用）
- 实现 Max Tokens 滑块
- 理解 `format_func` 参数格式化显示

#### 📝 知识点
- **`st.selectbox(label, options, format_func, index)`**：
  - `options`：选项值列表（机器标识）
  - `format_func`：显示给用户看的格式化函数（中文名）
  - `index`：默认选中项的索引
- **`st.slider(label, min, max, value, step, disabled)`**：数值滑块
- **`st.session_state` 存选中模型**：防止 rerun 时回到默认值

#### 📄 补充代码（`sidebar.py` 中段）

```python
# ⚠️ 将 Day 25 中原有的 from ..config import (...) 更新为如下完整版：
# （MODELS 和 DEFAULT_MODEL 已在 Day 25 导入，此处合并新增的 DEFAULT_TEMPERATURE 等）
from ..config import (
    MODELS, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS,
    MIN_MAX_TOKENS, MAX_MAX_TOKENS, TOKEN_STEP,
    get_model_label,    # 将 "deepseek-v4-flash" 转为 "DeepSeek V4 Flash" 显示
)

# ==================== 模型选择 ====================
st.sidebar.markdown("### 🤖 模型选择")

# 获取所有可用模型的标识列表
model_options = list(MODELS.keys())
# 找到默认模型在列表中的位置，用于设置下拉框的默认选中项
# if ... else 0 是防御性编程：万一 DEFAULT_MODEL 不在 options 中则回退到第 0 项
default_index = model_options.index(DEFAULT_MODEL) if DEFAULT_MODEL in model_options else 0

# 初始化或恢复选中的模型（存到 session_state 防止 rerun 时重置）
if "selected_model" not in st.session_state:
    st.session_state.selected_model = model_options[default_index]

# 模型选择下拉框
selected_model = st.sidebar.selectbox(
    "选择模型",
    options=model_options,                       # 选项列表（机器标识）
    format_func=get_model_label,                 # 显示格式化函数——把机器标识转为中文名称
    index=model_options.index(st.session_state.selected_model),  # 默认选中项
    key="model_selector",                        # 用于 Streamlit 内部追踪组件状态
)
# 更新 session_state 中的模型选择，下次 rerun 时不会丢失
st.session_state.selected_model = selected_model

# 显示当前选中模型的描述文字（灰色小字，位于下拉框下方）
model_info = MODELS.get(selected_model, {})
st.sidebar.caption(model_info.get("description", ""))

st.sidebar.markdown("---")

# ==================== 对话参数 ====================
st.sidebar.markdown("### 🎛️ 对话参数")

# Temperature 滑块：控制回复的随机性/创造性
# 注意：disabled 和 help 中用到的 thinking_mode 变量将在 Day 27 中定义
# 此处先按最终版本写出，后续 Day 27 补充 thinking_mode 后即可正常运行
temperature = st.sidebar.slider(
    "🌡️ Temperature",
    min_value=0.0,         # 最小值 0.0：完全确定，适合代码生成
    max_value=2.0,         # 最大值 2.0：最大随机性，适合创意写作
    value=DEFAULT_TEMPERATURE,  # 默认值 0.7：平衡点
    step=0.1,              # 步长 0.1，共 21 个档位
    disabled=thinking_mode,  # 思维链模式下禁用此滑块（thinking_mode 在 Day 27 定义）
    help="控制回复的随机性。越高越有创意。思维链模式下此参数无效。" if thinking_mode
         else "控制回复的随机性。越高越有创意，越低越确定。",
)

# Max Tokens 滑块：控制单次回复的最大长度
max_tokens = st.sidebar.slider(
    "📏 最大输出长度",
    min_value=MIN_MAX_TOKENS,   # 最小值 256：保证回复至少有基本长度
    max_value=MAX_MAX_TOKENS,   # 最大值 8192：DeepSeek 单次输出上限
    value=DEFAULT_MAX_TOKENS,   # 默认值 4096：适中的长度
    step=TOKEN_STEP,            # 步长 256，共 32 个档位
    help="单次回复的最大 token 数量。越大回复越长。",
)

st.sidebar.markdown("---")
```

#### 🎬 视频要点（~25min）
1. **`format_func` 的作用（5min）**：不传 → 下拉框显示 `"deepseek-v4-flash"`；传了 → 显示 `"DeepSeek V4 Flash"`
2. **滑块交互（8min）**：拖动滑块 → 观察值的实时变化
3. **`session_state` 记录模型选择（5min）**：为什么需要？——否则每次 rerun 都会回到默认值
4. **`st.caption` 灰色说明（3min）**：在模型选择后展示该模型的描述

#### 📌 课后作业
- 在 Temperature 滑块下方添加一个"重置默认值"按钮
- 尝试用 `st.slider` 的 `label_visibility` 参数隐藏标签

#### 测试验证

```bash
python tests/test_day25_27_sidebar.py
```

测试中验证：模型选择导入、Temperature 滑块 disabled=thinking_mode、返回字典字段。

---

### Day 27：侧边栏 — 思维链开关与会话管理

#### 🎯 教学目标
- 实现思维链开关（含条件禁用逻辑）
- 理解组件联动：切换模型 → 思维链禁用；开启思维链 → Temperature 禁用
- 实现会话管理区（消息数、Token 估算、清除按钮）
- 添加关于板块

#### 📝 知识点
- **`st.checkbox(label, value, disabled)`**：复选框开关
- **组件联动逻辑**：
  - V4 Flash 不支持 thinking → 开关禁用
  - Thinking 开启时 → Temperature 禁用（API 要求）
- **`st.metric(label, value)`**：KPI 数字卡片
- **`st.button(label, use_container_width)`**：触发一次性操作

#### 📄 补充代码（`sidebar.py` 下半部分）

⚠️ **注意代码插入位置！** 以下思维链开关代码需要插入在 Day 26 的 `### 🎛️ 对话参数` 标题之后、Temperature 滑块之前——因为 `thinking_mode` 变量必须在 Temperature 的 `disabled=thinking_mode` 之前定义。

```python
# ⚠️ 将以下导入合并到 sidebar.py 顶部已有的 import 区域：
# supports_thinking 合并到 from ..config import (...) 中
from ..config import supports_thinking
# 以下是新增的导入（来自 chat_manager 模块）
from ..chat_manager import (
    get_message_count, clear_history,
    should_warn_token_limit, estimate_token_count,
)

# ==================== 思维链开关 ====================
# 检查当前选中的模型是否支持思维链推理
model_supports_thinking = supports_thinking(selected_model)

# 初始化思维链开关状态（默认关闭）
if "enable_thinking" not in st.session_state:
    st.session_state.enable_thinking = False

# 组件联动逻辑：如果当前模型不支持思维链，自动关闭开关
# 例如：用户先在 V4 Pro 下开启了思维链，然后切换到 V4 Flash
# 此时 V4 Flash 不支持思维链，需要自动关闭并提示用户
if not model_supports_thinking and st.session_state.enable_thinking:
    st.session_state.enable_thinking = False
    st.sidebar.info("💡 思维链模式仅在 deepseek-v4-pro 模型中可用")

# 思维链复选框
enable_thinking = st.sidebar.checkbox(
    "🧠 思维链推理",
    value=st.session_state.enable_thinking,
    disabled=not model_supports_thinking,  # 模型不支持时变灰不可点击
    help="启用后展示推理过程。仅 V4 Pro 支持。",
)
st.session_state.enable_thinking = enable_thinking

# thinking_mode 为 True 表示开关开启 AND 模型真的支持
# 两个条件缺一不可
thinking_mode = enable_thinking and model_supports_thinking

# 思维链模式下 Temperature 参数无效
# 因为推理过程需要确定性，不能有随机扰动
if thinking_mode:
    st.sidebar.caption("💡 思维链模式下 Temperature 参数无效")

# ✅ 此时回顾 Day 26 的 Temperature 滑块：其中的 disabled=thinking_mode 和
# 条件化 help 文字现在可以正常工作了——因为 thinking_mode 已在本节定义。

st.sidebar.markdown("---")

# ==================== 会话管理 ====================
st.sidebar.markdown("### 💬 会话管理")

# 用两列并排展示消息数和 Token 估算值
col1, col2 = st.sidebar.columns(2)
with col1:
    # st.metric 渲染一个 KPI 数字卡片
    st.metric("消息数", get_message_count())
with col2:
    # Token 估算值（前面加 ~ 表示是约数）
    st.metric("估 Token", f"{estimate_token_count()}")

# 当 Token 数超过阈值时显示警告
if should_warn_token_limit():
    st.sidebar.warning("⚠️ 对话已较长，建议清除历史避免上下文溢出")

# 清除对话历史按钮
# use_container_width=True 让按钮占满侧边栏宽度
if st.sidebar.button("🗑️ 清除对话历史", use_container_width=True):
    # 清空 session_state 中的消息列表
    clear_history()
    # 触发 Streamlit rerun，刷新 UI 回到欢迎页
    # 如果不调用 rerun()，消息列表虽然已清空，但 UI 上还是旧的聊天记录
    st.rerun()

st.sidebar.markdown("---")

# ==================== 关于信息 ====================
st.sidebar.markdown("### 📖 关于")
st.sidebar.markdown("""
    **DeepSeek AI 聊天助手**
    基于 Streamlit + DeepSeek API 构建

    🎬 Bilibili 教程：[XianZS](https://space.bilibili.com/3690991649294439)
""")

# ==================== 返回完整设置字典 ====================
# 将所有的用户配置项打包返回，供 app.py 使用
return {
    "api_key": api_key_input,      # 用户在侧边栏输入的 API 密钥
    "model": selected_model,       # 选中的模型标识
    "temperature": temperature,    # Temperature 参数值
    "max_tokens": max_tokens,      # Max Tokens 参数值
    "enable_thinking": enable_thinking,  # 是否开启思维链推理
}
```

#### 🎬 视频要点（~28min）
1. **组件联动演示（8min）**：切换 V4 Flash → 思维链开关变灰 → 切换回 V4 Pro → 开关恢复
2. **`st.metric` 展示（5min）**：消息数和 Token 估算两个数字并排
3. **清除按钮（5min）**：点击 → `clear_history()` → `st.rerun()` → 回到欢迎页
4. **警告触发（5min）**：发很多条长消息，直到触发 ⚠️ 警告
5. **关于板块（2min）**：推广你的 Bilibili 频道

#### 📌 课后作业
- 实现"导出对话为 JSON"按钮（`st.download_button`）
- 在清除按钮前添加一个确认弹窗（`st.warning` + 二次确认按钮）

#### 测试验证

```bash
python tests/test_day25_27_sidebar.py
```

测试中验证：思维链复选框条件禁用、info 提示消息、Token 警告消息完整性、清除按钮逻辑。
完整交互验证需启动 Streamlit（见测试文件中的手动验证步骤）。

---

## 第八阶段：流式处理与整合

### Day 28：`stream_handler.py` — 流式响应处理

#### 🎯 教学目标
- 理解 `st.empty()` 占位符模式
- 实现 `process_stream()` 函数
- 处理 4 种 chunk 类型的 UI 更新
- 抽象重复的 HTML 模板

#### 📝 知识点
- **`st.empty()`**：创建一个空白占位符，返回的对象的 `.markdown()` / `.error()` 等方法可以替换内容
- **占位符更新模式**：每次调用 `.markdown(text)`，旧内容被新内容替换——实现"就地更新"效果
- **光标动画**：`content + "▌"` 模拟打字光标
- **HTML 模板函数**：`_render_reasoning_html(text, streaming)` 根据是否在推理中，生成不同的 HTML

#### 📄 创建文件

**src/stream_handler.py**：
```python
"""流式响应处理器：处理 LLM 流式输出并更新 Streamlit UI

本模块是教学重点之一——它展示了：
- 如何使用 st.empty() 占位符实现渐进式 UI 更新（打字机效果）
- 如何将 UI 渲染逻辑从业务编排中分离
- 如何抽象重复的 HTML 模板为可复用函数
- 如何处理流式响应的 4 种 chunk 类型

核心设计：
- 调用方创建两个 st.empty() 占位符（reasoning + content）
- process_stream() 在流式消费过程中不断更新这两个占位符
- 流式结束后，调用方用返回的完整文本持久化到 session_state
"""
import streamlit as st
from .deepseek_client import chat_stream


def _render_reasoning_html(text: str, *, streaming: bool) -> str:
    """生成思维链折叠面板 HTML

    使用原生 HTML <details> 标签实现折叠面板，
    比 Streamlit 的 st.expander() 更轻量，避免嵌套组件冲突。

    Args:
        text: 推理文本（已累积的全部内容，渐进增长中）
        streaming: True  → 面板展开状态，标题显示 "🧠 思考中..."
                   False → 面板折叠状态，标题显示 "🧠 查看思考过程"

    注意：* 后面的 streaming 是关键字参数（keyword-only argument），
    调用时必须写 streaming=True 或 streaming=False，不能传位置参数。
    """
    return (
        # <details open> 中的 open 属性让面板默认展开
        # 流式进行中时需要展开面板，让用户实时看到思考过程逐渐生成
        f'<details{" open" if streaming else ""}>'
        # summary 标签定义折叠面板的标题（点击标题切换展开/折叠）
        f'<summary style="color: #888; cursor: pointer; font-size: 0.9em;">'
        f'{"🧠 思考中..." if streaming else "🧠 查看思考过程"}</summary>'
        # 面板内容区：灰色文字 + 左边框 + 内边距
        f'<div style="color: #aaa; font-size: 0.85em; line-height: 1.6; '
        f'padding: 8px; border-left: 3px solid #555; margin-top: 4px;">'
        f'{text}</div></details>'
    )


def process_stream(
    api_key: str,
    api_message: list[dict[str, str]],
    settings: dict,
    reasoning_placeholder,   # st.empty() 占位符，用于显示/更新思维链内容
    content_placeholder,     # st.empty() 占位符，用于显示/更新回复内容
) -> tuple[str, str, bool]:
    """处理流式 LLM 响应并更新 UI 占位符

    这是连接 API 层（deepseek_client.py）和 UI 层（app.py）的中间层。
    它消费 chat_stream() 产出的 chunk 流，根据 chunk 类型执行不同的 UI 更新策略。

    调用方应在 with st.chat_message("assistant"): 内调用，
    调用前创建两个 st.empty() 占位符。

    占位符更新原理：
    - st.empty() 创建一个"空槽位"
    - 每次调用 placeholder.markdown(text) 都会替换槽位中的旧内容
    - 这就实现了"就地更新"效果，看起来像打字机逐字输出

    Returns:
        tuple[str, str, bool]: (reasoning_text, content_text, has_error)
        - reasoning_text: 完整的思维链文本（用于持久化到 session_state）
        - content_text: 完整的回复文本（用于持久化到 session_state）
        - has_error: 是否发生了错误（True 时不持久化消息）
    """
    reasoning_text = ""   # 累积的思维链推理文本
    content_text = ""      # 累积的回复正文
    has_error = False      # 错误标记

    # 消费来自 chat_stream 的流式 chunk
    for chunk in chat_stream(
        api_key=api_key,
        message=api_message,
        model=settings["model"],
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        enable_thinking=settings["enable_thinking"],
    ):
        chunk_type = chunk["type"]

        # ==== reasoning chunk：思维链推理片段 ====
        if chunk_type == "reasoning":
            # 累积推理文字
            reasoning_text += chunk["text"]
            # 实时更新占位符：展开面板 + 累积文字 + 流式标题
            reasoning_placeholder.markdown(
                _render_reasoning_html(reasoning_text, streaming=True),
                unsafe_allow_html=True,
            )

        # ==== content chunk：普通回复文本片段 ====
        elif chunk_type == "content":
            # 累积回复文字
            content_text += chunk["text"]
            # 实时更新占位符：累积文字 + 光标动画 "▌"
            # 光标 "▌" 模拟打字光标，让用户感觉到正在生成
            content_placeholder.markdown(content_text + "▌")

        # ==== done chunk：流结束信号 ====
        elif chunk_type == "done":
            # 最终状态：思维链面板切换为折叠状态
            if reasoning_text:
                reasoning_placeholder.markdown(
                    _render_reasoning_html(reasoning_text, streaming=False),
                    unsafe_allow_html=True,
                )
            else:
                # 如果没有思维链内容，清空占位符（不显示任何东西）
                reasoning_placeholder.empty()
            # 最终状态：移除光标动画，显示完整文本
            content_placeholder.markdown(content_text)

        # ==== error chunk：错误信息 ====
        elif chunk_type == "error":
            # 出错时清除思维链占位符
            if reasoning_text:
                reasoning_placeholder.empty()
            # 在 content 占位符中显示红色错误信息
            content_placeholder.error(chunk["message"])
            has_error = True
            break  # 错误发生后不再处理后续 chunk

    # 边界情况：模型正常完成但未返回任何内容
    # 例如：模型只推理不输出（全 reasoning 无 content）
    if not content_text and not has_error and not reasoning_text:
        content_placeholder.info("模型未返回任何内容，请重试。")

    return reasoning_text, content_text, has_error
```

#### 🎬 视频要点（~30min）
1. **占位符演示（8min）**：创建 2 个 `st.empty()` → 依次更新 → 展示"替换"而非"追加"的效果
2. **4 种 chunk 处理（10min）**：
   - reasoning：展开面板 + 累积文字
   - content：文字 + 光标动画
   - done：折叠面板 + 去除光标
   - error：清除面板 + 显示红色错误
3. **HTML 模板的抽象（5min）**：对比原始的 2 段重复 HTML → `_render_reasoning_html()` 的 `streaming` 参数
4. **边界情况（5min）**：模型返回空 → `content_placeholder.info(...)` 提示用户

#### 📌 课后作业
- 在光标处尝试不同的动画：`|` → `_` → 循环
- 画一张状态图描述 4 种 chunk 类型的转换关系

#### 测试验证

```bash
python tests/test_day28_stream_handler.py
```

测试覆盖：_render_reasoning_html 的展开/折叠状态、HTML CSS 样式完整性、
process_stream 对 reasoning/content/done/error 四种 chunk 的处理、空响应边界情况。

---

### Day 29：`app.py` — 完整编排

#### 🎯 教学目标
- 将所有模块组装为完整 `app.py`
- 理解 5 步数据流
- 理解 `st.rerun()` 的必要性

#### 📝 知识点
- **编排层的职责**：调用各模块，不包含业务细节
- **5 步数据流**：
  1. 用户输入 → `add_user_message()` 存到 session
  2. `build_api_message()` → 裁剪后的消息列表
  3. `process_stream()` → 流式 UI 更新
  4. `add_assistant_message()` → 持久化回复
  5. `st.rerun()` → 刷新页面

#### 📄 更新 `src/__init__.py` — 模块公共 API 导出

Day 7 创建的 `src/__init__.py` 当时为空文件。现在所有子模块都已完成，
是时候将其填充为模块的公共 API 导出文件——让外部调用方可以
从 `src` 包直接导入所有公开函数。

```python
"""DeepSeek AI 聊天助手核心模块

提供配置管理、API 客户端、会话管理和流式响应处理功能。

模块结构（对应教学单元）：
- config:          环境变量与 API 配置管理
- deepseek_client: DeepSeek API 客户端封装（流式调用）
- chat_manager:    多轮对话会话管理（上下文裁剪、Token 估算）
- stream_handler:  流式响应处理（UI 渐进更新）
"""

from .config import (
    get_api_key,
    set_api_key,
    validate_config,
    get_model_label,
    supports_thinking,
)
from .deepseek_client import chat_stream
from .chat_manager import (
    init_message,
    add_user_message,
    add_assistant_message,
    clear_history,
    get_message_count,
    get_all_message,
    build_api_message,
    estimate_token_count,
    should_warn_token_limit,
)
from .stream_handler import process_stream

__all__ = [
    # config
    "get_api_key",
    "set_api_key",
    "validate_config",
    "get_model_label",
    "supports_thinking",
    # deepseek_client
    "chat_stream",
    # chat_manager
    "init_message",
    "add_user_message",
    "add_assistant_message",
    "clear_history",
    "get_message_count",
    "get_all_message",
    "build_api_message",
    "estimate_token_count",
    "should_warn_token_limit",
    # stream_handler
    "process_stream",
]
```

> 💡 **为什么需要 `__init__.py` 的公共 API 导出？**
>
> `__all__` 列表声明了本模块的"公开接口"——哪些函数是给外部使用的。
> 当其他代码执行 `from src import get_api_key` 或 `from src import *` 时，
> 只有 `__all__` 中列出的名字会被导出。这是一种"白名单"设计，
> 防止内部实现细节泄露到模块外部。

#### 📄 最终版 `app.py`

```python
"""Streamlit 主程序入口：编排 UI 和业务逻辑

本文件是应用的"大脑"——它不包含具体的业务逻辑，
而是将 config、chat_manager、stream_handler、UI 模块
按照正确的顺序编排起来。

5 步数据流：
1. 用户输入 → add_user_message() 存入 session_state
2. build_api_message() → 裁剪后的消息列表（不含 reasoning_content）
3. process_stream() → 流式 UI 更新（打字机效果）
4. add_assistant_message() → 持久化回复到 session_state
5. st.rerun() → 触发页面刷新，展示完整历史消息
"""
import streamlit as st

# ⚠️ set_page_config 必须是第一个 Streamlit 调用
# 如果放在其他 st.xxx() 之后，Streamlit 会抛出异常
st.set_page_config(
    page_title="DeepSeek AI 助手",     # 浏览器标签页标题
    page_icon="🤖",                     # 标签页图标
    layout="wide",                      # 宽屏布局
    initial_sidebar_state="expanded",   # 侧边栏默认打开
)

# 导入各模块（必须在 set_page_config 之后，因为模块内部可能使用 st.xxx）
from src.ui.utils import inject_custom_css
from src.ui.sidebar import render as render_sidebar   # 重命名使语义更明确
from src.ui.chat_area import render_all_message, render_welcome, render_message
from src.config import get_api_key, validate_config
from src.chat_manager import (
    init_message,           # 初始化消息列表
    add_user_message,        # 添加用户消息
    add_assistant_message,   # 添加 AI 回复
    get_message_count,       # 获取消息总数
    build_api_message,      # 构建 API 格式的消息列表
)
from src.stream_handler import process_stream


def main() -> None:
    """主程序入口：编排应用生命周期

    这个函数在每次 Streamlit rerun 时都会完整执行一次。
    执行顺序：
    1. 注入样式 → 2. 初始化数据 → 3. 渲染侧边栏
    → 4. 渲染聊天区 → 5. 处理用户输入 → 6. 流式响应
    → 7. 持久化 → 8. Rerun
    """

    # ===== 初始化 =====
    # 注入自定义 CSS（隐藏页脚、调整间距等）
    inject_custom_css()
    # 确保消息列表存在（首次运行时创建空列表）
    init_message()

    # ===== 侧边栏 =====
    # 渲染整个侧边栏并获取所有用户设置
    settings = render_sidebar()
    # 密钥优先级：侧边栏输入 > .env 环境变量
    api_key = settings["api_key"] or get_api_key()
    # 校验配置状态（只取 valid 值，忽略描述信息）
    valid, _ = validate_config()

    # ===== 主聊天区域 =====
    # 根据是否有对话历史决定显示内容
    if get_message_count() == 0:
        # 无消息 → 显示欢迎引导页（标题 + 建议卡片）
        render_welcome()
    else:
        # 有消息 → 渲染完整的聊天历史
        render_all_message()

    # ===== 聊天输入框 =====
    # 配置无效时禁用输入框，防止用户发送注定失败的请求
    chat_disabled = not valid

    if prompt := st.chat_input(
        # 占位符文字根据配置状态动态变化
        "输入你的问题..." if not chat_disabled else "请先在侧边栏配置 API 密钥",
        disabled=chat_disabled,
    ):
        # 1. 记录 + 渲染用户消息
        add_user_message(prompt)
        render_message("user", prompt)

        # ==== 步骤 2：构建 API 消息列表 ====
        # 关键：必须去除 reasoning_content 字段，否则 API 返回 400 错误
        api_message = build_api_message()

        # ==== 步骤 3：流式处理 LLM 响应 ====
        # 在助手气泡中创建两个 st.empty() 占位符
        with st.chat_message("assistant", avatar="🤖"):
            # 占位符 A：用于显示思维链推理过程
            reasoning_placeholder = st.empty()
            # 占位符 B：用于显示回复正文 + 光标动画
            content_placeholder = st.empty()

            # process_stream 消费 API 流，实时更新两个占位符
            reasoning_text, content_text, _ = process_stream(
                api_key=api_key,
                api_message=api_message,
                settings=settings,
                reasoning_placeholder=reasoning_placeholder,
                content_placeholder=content_placeholder,
            )

        # ==== 步骤 4：持久化助手消息 ====
        # 只有在有内容返回（或至少有思维链文本）时才保存
        if content_text or reasoning_text:
            add_assistant_message(
                # 如果没有正文但有思维链内容，用占位文字替代
                content=content_text if content_text else "（模型未返回文本内容）",
                # 只有有思维链文本时才保存，否则存 None
                reasoning_content=reasoning_text if reasoning_text else None,
            )

        # ==== 步骤 5：触发 rerun ====
        # 让 Streamlit 重新执行整个脚本，此时：
        # - 消息已持久化到 session_state
        # - get_message_count() > 0，所以会走到 render_all_message() 分支
        # - 用户看到完整的聊天历史（包括刚刚的对话）
        # 如果不调用 rerun()，用户气泡和助手气泡会在屏幕上显示两次
        # （一次来自步骤 1/3 的实时渲染，一次来自 rerun 后的 render_all_message）
        st.rerun()


# Python 脚本的标准入口点
# 只有当直接运行 app.py 时才执行 main()，
# 如果被其他模块 import，则不会执行
if __name__ == "__main__":
    main()
```

#### 🎬 视频要点（~30min）
1. **数据流全景图（8min）**：用一张图展示从用户输入到页面刷新的完整路径
2. **5 步编排（12min）**：逐段讲解代码，每段对应数据流的一步
3. **`st.rerun()` 的必要性（5min）**：注释掉它 → 演示历史消息不刷新的 bug
4. **运行测试（5min）**：完整的端到端测试——发送消息、切换模型、清除历史

#### 📌 课后作业
- 在 `main()` 中添加日志输出（`print` 或 `st.toast`），追踪每次 rerun
- 尝试在数据流的第 3 步和第 4 步之间插入"保存到本地文件"的功能

#### 测试验证

```bash
python tests/test_day29_app_integration.py
```

测试覆盖：set_page_config 在第一个 st 调用、所有必需导入、5 步数据流完整性、
chat_disabled 逻辑、st.rerun() 调用顺序、页面配置参数。
端到端验证需启动 Streamlit 并使用有效的 API Key（见测试文件中的手动验证步骤）。

---

## 第九阶段：项目发布

### Day 30：README 文档 + GitHub 发布 + 课程总结

#### 🎯 教学目标
- 编写专业的 README.md
- 将项目推送到 GitHub
- 回顾 30 天学到的全部技能
- 提供后续学习路径

#### 📝 知识点
- **README 的必要元素**：项目简介、功能特性、快速开始、项目结构、技术栈、License
- **GitHub 仓库设置**：Public/Private、About、Topics、License
- **开源协议**：MIT License — 最宽松的协议，允许任何人使用、修改、商用

#### 🛠️ 实操步骤

```bash
# ===== 1. 确保所有文件已提交到本地 Git =====
# 查看工作区状态：确认没有未跟踪或未提交的文件
git status
# 将所有修改添加到暂存区
git add .
# 提交到本地仓库
# "feat:" 前缀表示这是一个新功能（feature），是 Conventional Commits 约定
git commit -m "feat: 完成 DeepSeek AI 聊天助手 v1.0"

# ===== 2. 在 GitHub 网站创建新仓库 =====
# 登录 GitHub → 点击右上角 + → New repository
# 仓库名称：deepseek-ai-chat-assistant
# 仓库描述：基于 Streamlit + DeepSeek API 的 AI 聊天助手
# 不要勾选 "Add a README file"（因为我们已有本地文件）
# 创建后会显示推送命令指引

# ===== 3. 关联远程仓库并推送 =====
# 将本地仓库与 GitHub 远程仓库关联
# origin 是远程仓库的默认别名（约定俗成的命名）
git remote add origin https://github.com/XianZS/deepseek-ai-chat-assistant.git
# 将当前分支重命名为 main（GitHub 的默认分支名）
# -M 强制重命名（即使目标分支已存在）
git branch -M main
# 将本地 main 分支推送到 GitHub
# -u 设置上游分支（upstream），之后只需 git push 即可
git push -u origin main
```
```

#### 📊 30 天技能树总结

```
第1-4天：环境与项目
   Python 环境管理 → 项目结构 → Git 版本控制 → .gitignore

第5-7天：配置与安全
   API 密钥 → .env 管理 → python-dotenv → 配置模块设计

第8-12天：API 客户端
   OpenAI SDK → Generator/yield → 流式响应 → 异常分类处理

第13-16天：Streamlit 入门
   执行模型 → Markdown/HTML → CSS 注入 → chat_input

第17-20天：聊天 UI
   消息气泡 → 折叠面板 → 欢迎页 → 历史消息渲染

第21-24天：状态管理
   Session State → 消息 CRUD → API 裁剪 → Token 估算

第25-27天：侧边栏
   密钥输入 → 模型选择 → 参数滑块 → 组件联动 → 会话管理

第28-29天：流式处理与整合
   占位符更新 → 思维链可视化 → 模块编排 → 数据流

第30天：发布
   README → GitHub → 开源协议 → 课程回顾
```

#### 🎬 视频要点（~35min）
1. **README 编写（8min）**：展示最终 README 的每个部分，解释为什么这么写
2. **GitHub 发布（10min）**：创建仓库 → push → 设置 About 和 Topics
3. **30 天回顾（12min）**：快速翻阅 9 个源文件，每个文件一句话总结——"这个文件在整个系统中扮演什么角色"
4. **后续学习路径（3min）**：
   - 部署到 Streamlit Cloud（免费）
   - 添加多用户支持
   - 集成更多模型（OpenAI、Claude）
   - 添加对话历史导出/导入

#### 📌 课后作业
- 将项目 Push 到自己的 GitHub 并设为 Public
- 在 README 中添加你的 Bilibili 频道链接
- 尝试将应用部署到 [Streamlit Community Cloud](https://streamlit.io/cloud)

#### 测试验证

```bash
python tests/test_day30_readme.py
```

测试覆盖：README.md 存在且内容充足、必需章节完整、技术栈说明、
requirements.txt 与 README 中依赖一致。GitHub 发布需手动验证。

---

## 📋 附录

### A. 最终项目文件列表

```
Intelligent_Chat_Programming_Assistant/
├── .env.example              # API Key 模板（可提交）
├── .env                      # API Key 真实值（不提交）
├── .gitignore                # Git 忽略规则
├── requirements.txt          # 项目依赖（3 个）
├── app.py                    # 主程序入口（~97 行）
├── README.md                 # 项目文档
├── src/
│   ├── __init__.py           # 包初始化 + 公共 API 导出
│   ├── config.py             # 配置管理（~77 行）
│   ├── deepseek_client.py    # API 客户端（~94 行）
│   ├── chat_manager.py       # 会话管理（~119 行）
│   ├── stream_handler.py     # 流式响应处理（~110 行）
│   └── ui/
│       ├── __init__.py       # UI 包初始化 + 公共 API 导出
│       ├── utils.py          # CSS 样式注入（~43 行）
│       ├── sidebar.py        # 侧边栏控件（~164 行）
│       └── chat_area.py      # 聊天区域渲染（~84 行）
└── TEACHING_PLAN.md          # 本教学大纲
```

### B. 每天对应创建/修改的文件

| 天数 | 新建文件 | 修改文件 |
|---|---|---|
| Day 1-2 | — | —（环境搭建，无代码） |
| Day 3 | `requirements.txt` | — |
| Day 4 | `.gitignore` | — |
| Day 5 | — | —（注册 API，无代码） |
| Day 6 | `.env.example`, `.env` | — |
| Day 7 | `src/__init__.py`, `src/config.py` | — |
| Day 8 | `src/deepseek_client.py`（临时版） | — |
| Day 9 | — | `src/config.py`（加测试） |
| Day 10 | — | —（Generator 练习） |
| Day 11 | — | `src/deepseek_client.py`（重写为流式版） |
| Day 12 | — | —（异常处理讲解） |
| Day 13 | `app.py`（骨架版） | — |
| Day 14 | — | —（Markdown 练习） |
| Day 15 | `src/ui/__init__.py`, `src/ui/utils.py` | — |
| Day 16 | — | `app.py`（加 chat_input） |
| Day 17 | `src/ui/chat_area.py`（上半） | — |
| Day 18 | — | `src/ui/chat_area.py`（加 expander） |
| Day 19 | — | `src/ui/chat_area.py`（加 welcome） |
| Day 20 | — | `src/ui/chat_area.py`（加 render_all）、`app.py` |
| Day 21 | — | —（session_state 练习） |
| Day 22 | `src/chat_manager.py`（上半） | — |
| Day 23 | — | `src/chat_manager.py`（下半） |
| Day 24 | — | `src/chat_manager.py`（加 Token 估算） |
| Day 25 | `src/ui/sidebar.py`（上半） | `app.py`（加 sidebar 调用） |
| Day 26 | — | `src/ui/sidebar.py`（加模型和参数） |
| Day 27 | — | `src/ui/sidebar.py`（加思维链和会话管理） |
| Day 28 | `src/stream_handler.py` | — |
| Day 29 | — | `src/__init__.py`（公共 API 导出）、`app.py`（完整编排） |
| Day 30 | `README.md` | — |

### C. 关键参数速查表

| 参数 | 默认值 | 范围 | 说明 |
|---|---|---|---|
| `temperature` | 0.7 | 0.0 ~ 2.0 | 越高越随机（思维链模式下无效） |
| `max_tokens` | 4096 | 256 ~ 8192 | 单次最大输出长度 |
| `CHARS_PER_TOKEN` | 2 | — | 字符/Token 估算比例 |
| `TOKEN_WARNING_THRESHOLD` | 50000 | — | 触发警告的 token 阈值 |

### D. 两个模型对比

| 特性 | DeepSeek V4 Flash | DeepSeek V4 Pro |
|---|---|---|
| 标识 | `deepseek-v4-flash` | `deepseek-v4-pro` |
| 定位 | 快速、经济 | 高性能、深度推理 |
| 思维链 | ❌ 不支持 | ✅ 支持 |
| Temperature | ✅ 有效 | 思维链模式下无效 |
| 适用场景 | 日常对话、简单问答 | 编程、数学、复杂分析 |

---

> 🎬 本大纲配套视频发布于 Bilibili 频道：[XianZS](https://space.bilibili.com/3690991649294439)
> 📺 系列合集：[Python 小 Demo 系列](https://space.bilibili.com/3690991649294439/lists/7284550)
> 📦 项目源码：[GitHub](https://github.com/XianZS)
