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
# 确认 Python 已安装且版本 ≥ 3.8
python --version
# 预期输出：Python 3.11.x 或 Python 3.12.x

# 确认 pip 可用
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
# 1. 创建虚拟环境（指定 Python 3.11）
conda create -n PythonLearning python=3.11 -y

# 2. 激活虚拟环境
conda activate PythonLearning

# 3. 验证——注意命令行前面出现 (PythonLearning) 前缀
python --version    # Python 3.11.x
pip --version       # 位于 .../envs/PythonLearning/...

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
# 确保环境已激活
conda activate PythonLearning

# 创建项目目录结构
mkdir Intelligent_Chat_Programming_Assistant
cd Intelligent_Chat_Programming_Assistant
mkdir -p src/ui

# 创建 requirements.txt
echo "openai>=1.0.0" > requirements.txt
echo "streamlit>=1.28.0" >> requirements.txt
echo "python-dotenv>=1.0.0" >> requirements.txt

# 安装
pip install -r requirements.txt

# 验证安装
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
# Python
__pycache__/
*.pyc

# 环境变量（包含真实 API 密钥）
.env

# 虚拟环境
venv/
.conda/

# IDE
.vscode/
.idea/
```

#### 🛠️ 实操步骤

```bash
cd Intelligent_Chat_Programming_Assistant
git init
git add .
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
# DeepSeek API 密钥
# 获取方式：访问 https://platform.deepseek.com/api_keys 注册并创建 Key
DEEPSEEK_API_KEY=example-key
```

**.env**（本地文件，不提交）：
```bash
DEEPSEEK_API_KEY=sk-你的真实密钥
```

#### 🐍 临时测试脚本（`test_env.py`，演示后删除）

```python
import os
from dotenv import load_dotenv

load_dotenv()  # 自动查找当前目录的 .env 文件

api_key = os.environ.get("DEEPSEEK_API_KEY")
print(f"读取到的密钥：{api_key[:5]}***（已脱敏）")
```

运行：
```bash
python test_env.py
# 输出：读取到的密钥：sk-31***（已脱敏）
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

**src/__init__.py**（空文件，标记 src 为 Python 包）：
```python
```

**src/config.py**：
```python
"""配置管理：从环境变量读取 API 密钥和默认设置"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载 .env 文件（模块导入时自动执行一次）
load_dotenv()

# ---- API 配置 ----
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ---- 模型标识 ----
MODEL_FLASH = "deepseek-v4-flash"
MODEL_PRO = "deepseek-v4-pro"

# ---- 模型元数据 ----
MODELS: dict[str, dict] = {
    MODEL_FLASH: {
        "name": "DeepSeek V4 Flash",
        "description": "快速、经济实惠的通用模型，适合日常对话",
        "supports_thinking": False,
    },
    MODEL_PRO: {
        "name": "DeepSeek V4 Pro",
        "description": "高性能模型，支持思维链推理，适合复杂任务",
        "supports_thinking": True,
    },
}

# ---- 默认参数 ----
DEFAULT_MODEL = MODEL_FLASH
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
MIN_MAX_TOKENS = 256
MAX_MAX_TOKENS = 8192
TOKEN_STEP = 256

# ---- Token 估算常量 ----
TOKEN_WARNING_THRESHOLD = 50000
CHARS_PER_TOKEN = 2


# ---- 密钥管理 ----
def get_api_key() -> Optional[str]:
    """获取 API 密钥（优先读取环境变量）"""
    return os.environ.get("DEEPSEEK_API_KEY")


def set_api_key(api_key: str) -> None:
    """运行时设置 API 密钥（用户从侧边栏输入时调用）"""
    os.environ["DEEPSEEK_API_KEY"] = api_key


# ---- 配置校验 ----
def validate_config() -> tuple[bool, str]:
    """校验配置是否就绪，返回 (是否有效, 说明信息)"""
    api_key = get_api_key()
    if not api_key:
        return False, "⚠️ 请设置 DEEPSEEK_API_KEY（通过 .env 文件或侧边栏输入）"
    if api_key == "your_api_key_here":
        return False, "⚠️ 请将 .env 中的 DEEPSEEK_API_KEY 替换为你的真实密钥"
    if not api_key.startswith("sk-"):
        return False, "⚠️ API 密钥格式不正确，DeepSeek 密钥应以 'sk-' 开头"
    return True, "✅ 配置就绪"


# ---- 模型查询 ----
def get_model_label(model_id: str) -> str:
    """获取模型的显示名称（中文）"""
    return MODELS.get(model_id, {}).get("name", model_id)


def supports_thinking(model_id: str) -> bool:
    """判断模型是否支持思维链模式"""
    return MODELS.get(model_id, {}).get("supports_thinking", False)
```

#### 🐍 验证

```bash
# 测试模块导入
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
"""DeepSeek API 客户端封装"""
from openai import OpenAI
from .config import DEEPSEEK_BASE_URL


def _create_client(api_key: str) -> OpenAI:
    """创建 DeepSeek API 客户端

    以下划线 _ 开头表示这是模块内部使用的"私有函数"，
    外部使用者不应直接调用它。
    """
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def chat_once(api_key: str, prompt: str) -> str:
    """发送一次对话，返回回复文本（非流式，仅用于学习）"""
    client = _create_client(api_key)

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4096,
    )

    # response 的结构：response.choices[0].message.content
    return response.choices[0].message.content
```

#### 🐍 临时测试

```bash
python -c "
from dotenv import load_dotenv
load_dotenv()
import os
from src.deepseek_client import chat_once
reply = chat_once(os.environ['DEEPSEEK_API_KEY'], '用一句话介绍Python')
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
"""config 模块的简单验证"""
import os
from src.config import validate_config, set_api_key

# 测试 1：无密钥
os.environ.pop("DEEPSEEK_API_KEY", None)
valid, msg = validate_config()
print(f"测试1（无密钥）: {valid=}, {msg=}")
assert not valid

# 测试 2：假密钥
set_api_key("your_api_key_here")
valid, msg = validate_config()
print(f"测试2（示例值）: {valid=}, {msg=}")
assert not valid

# 测试 3：格式错误
set_api_key("invalid-key-format")
valid, msg = validate_config()
print(f"测试3（格式错）: {valid=}, {msg=}")
assert not valid

# 测试 4：正确密钥
set_api_key("sk-correct-key-format-12345")
valid, msg = validate_config()
print(f"测试4（正确）: {valid=}, {msg=}")
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
# 示例 1：普通函数
def get_numbers():
    return [1, 2, 3, 4, 5]

# 示例 2：Generator（等价但惰性）
def generate_numbers():
    for i in range(1, 6):
        print(f"产出: {i}")
        yield i

# 对比
print("普通函数：")
nums = get_numbers()      # 立即生成整个列表
print(nums)

print("\nGenerator：")
gen = generate_numbers()  # 不执行任何代码，返回生成器对象
print(next(gen))          # 产出 1
print(next(gen))          # 产出 2
# ...
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
"""DeepSeek API 客户端封装：流式对话与异常处理"""
from collections.abc import Generator
from openai import OpenAI, AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError
from .config import DEEPSEEK_BASE_URL


def _create_client(api_key: str) -> OpenAI:
    """创建 DeepSeek API 客户端"""
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def chat_stream(
    api_key: str,
    messages: list[dict[str, str]],
    model: str = "deepseek-v4-flash",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    enable_thinking: bool = False,
) -> Generator[dict, None, None]:
    """流式对话生成器

    Yields:
        {"type": "reasoning", "text": "..."}   — 思维链推理
        {"type": "content",   "text": "..."}   — 回复内容
        {"type": "done",      "usage": {...}}  — 完成信号
        {"type": "error",     "message": "..."} — 错误信息
    """
    try:
        client = _create_client(api_key)

        kwargs: dict = {
            "model": model,
            "messages": messages,
            "stream": True,
            "max_tokens": max_tokens,
        }

        # 思维链模式：仅 deepseek-v4-pro 支持
        if enable_thinking and model == "deepseek-v4-pro":
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
            # 注意：思维链模式下不能传 temperature
        else:
            kwargs["temperature"] = temperature

        response = client.chat.completions.create(**kwargs)

        for chunk in response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta is None:
                continue

            # 思维链内容
            reasoning = getattr(delta, "reasoning_content", None) or ""
            if reasoning:
                yield {"type": "reasoning", "text": reasoning}

            # 普通回复内容
            if delta.content:
                yield {"type": "content", "text": delta.content}

        yield {"type": "done", "usage": None}

    except AuthenticationError:
        yield {"type": "error", "message": "🔑 API 密钥无效，请检查后重试。"}
    except RateLimitError:
        yield {"type": "error", "message": "⏳ API 请求频率超限，请稍等片刻后重试。"}
    except APITimeoutError:
        yield {"type": "error", "message": "⏰ 请求超时，请检查网络连接后重试。"}
    except APIConnectionError:
        yield {"type": "error", "message": "🌐 无法连接到 DeepSeek 服务器，请检查网络连接。"}
    except Exception as e:
        error_msg = str(e)
        if "400" in error_msg:
            yield {"type": "error", "message": "⚠️ 请求参数错误，请尝试清除对话历史后重试。"}
        elif "500" in error_msg:
            yield {"type": "error", "message": "⚠️ DeepSeek 服务器内部错误，请稍后重试。"}
        else:
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
"""DeepSeek AI 聊天助手 — 主程序入口"""
import streamlit as st

# ⚠️ set_page_config 必须是第一个 Streamlit 调用
st.set_page_config(
    page_title="DeepSeek AI 助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 DeepSeek AI 聊天助手")
st.markdown("基于 DeepSeek V4 大模型，支持流式对话与思维链推理")

# 聊天输入框
if prompt := st.chat_input("输入你的问题..."):
    st.markdown(f"你说：**{prompt}**")
```

#### 🛠️ 运行

```bash
streamlit run app.py
```

#### 🎬 视频要点（~22min）
1. **Rerun 演示（10min）**：输入文字 → 按 Enter → 脚本重跑 → 新内容出现。用 `st.write("rerun!")` 证明每次都在重跑
2. **`:=` 海象运算符（5min）**：`if prompt := st.chat_input(...)` 等价于 `prompt = st.chat_input(...)` + `if prompt:`，但更简洁
3. **页面配置（5min）**：逐一修改 `page_title`、`layout` 等参数，展示效果变化

#### 📌 课后作业
- 修改 `page_icon` 为 🚀，修改 `layout` 为 `"centered"`，感受差异
- 在 `app.py` 中添加 `st.write(f"页面加载次数：{st.session_state.get('count', 0)}")` 观察 rerun 次数

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
# 1. 纯 Markdown
st.markdown("## 二级标题")
st.markdown("**粗体** 和 *斜体*")

# 2. HTML（需要允许）
st.markdown(
    '<div style="color: #ff6b6b; font-size: 1.5em;">红色大字</div>',
    unsafe_allow_html=True,
)

# 3. 混合使用
st.markdown("""
    ## 标题
    这是**Markdown**内容
    <div style="background: #333; padding: 10px;">
        这是 HTML 内容
    </div>
""", unsafe_allow_html=True)
```

#### 🎬 视频要点（~20min）
1. **三种模式展示（10min）**：纯 Markdown、纯 HTML、混合，逐一演示效果
2. **安全机制解释（5min）**：为什么不默认允许 HTML？——防止恶意用户注入 `<script>` 标签
3. **什么时候需要 HTML（3min）**：Streamlit 原生组件不支持的样式（如颜色、边框、hover 效果）

#### 📌 课后作业
- 用 `st.markdown` 在 `app.py` 中添加一段带背景色和边框的提示文字
- 尝试不用 `unsafe_allow_html=True` 渲染 HTML，观察结果

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

**src/ui/__init__.py**（空文件，标记为 Python 包）：
```python
```

**src/ui/utils.py**：
```python
"""UI 工具函数：CSS 样式注入"""
import streamlit as st


def inject_custom_css() -> None:
    """注入自定义 CSS 样式"""
    st.markdown(
        """
        <style>
            /* 隐藏 Made with Streamlit 页脚 */
            footer { display: none; }

            /* 主内容区域上边距 */
            .block-container {
                padding-top: 2rem;
            }

            /* 思维链展开面板字体 */
            .streamlit-expanderHeader {
                font-size: 0.9em;
                color: #888;
            }

            /* 侧边栏 API Key 使用等宽字体 */
            [data-testid="stSidebar"] [data-testid="stTextInput"] input {
                font-family: monospace;
            }

            /* 聊天消息间距 */
            .stChatMessage {
                padding: 0.5rem 1rem;
            }

            /* 建议卡片 hover 效果 */
            [data-testid="stMarkdownContainer"]
            div[style*="cursor: pointer"]:hover {
                border-color: #4a9eff !important;
                transition: border-color 0.3s;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
```

#### 🎬 视频要点（~25min）
1. **Chrome DevTools 教学（10min）**：打开 F12 → 找到 Streamlit 渲染的 HTML → 找到 `data-testid` 属性 → 写 CSS 选择器
2. **逐条 CSS 解释（10min）**：每条规则为什么需要，注释说明
3. **模块化思想（3min）**：为什么把 CSS 放在 `utils.py` 而不是直接写在 `app.py` 里？

#### 📌 课后作业
- 用 Chrome DevTools 找到 Streamlit 聊天消息的 `data-testid`
- 添加一条 CSS 规则：修改侧边栏背景色为深灰色

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

st.set_page_config(
    page_title="DeepSeek AI 助手", page_icon="🤖",
    layout="wide", initial_sidebar_state="expanded",
)

from src.ui.utils import inject_custom_css
from src.config import get_api_key, validate_config

inject_custom_css()

valid, status_msg = validate_config()

# 根据配置状态切换输入框
chat_disabled = not valid

if prompt := st.chat_input(
    "输入你的问题..." if not chat_disabled else "请先在侧边栏配置 API 密钥",
    disabled=chat_disabled,
):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

# 状态提示
if valid:
    st.sidebar.success(status_msg)
else:
    st.sidebar.warning(status_msg)
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
"""聊天区域渲染：消息展示、思维链折叠、欢迎页面"""
import streamlit as st
from typing import Optional


def render_message(
    role: str,
    content: str,
    reasoning_content: Optional[str] = None,
) -> None:
    """渲染单条消息气泡

    Args:
        role: "user" 或 "assistant"
        content: 消息正文（支持 Markdown）
        reasoning_content: 思维链推理内容（仅 assistant 可能有）
    """
    avatar = "🧑‍💻" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
```

#### 🎬 视频要点（~20min）
1. **气泡对比（5min）**：分别展示 user 和 assistant 的气泡样式
2. **上下文管理器（5min）**：`with` 的用法——进入时创建气泡，退出时关闭
3. **Markdown 支持（5min）**：在消息中写 `**粗体**`、代码块等

#### 📌 课后作业
- 在 `app.py` 中手动调用 `render_message("user", "你好")` 和 `render_message("assistant", "你好，有什么可以帮你的？")` 观察效果
- 尝试用图片 URL 替代 emoji 作为 avatar

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
def render_message(role, content, reasoning_content=None):
    avatar = "🧑‍💻" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        # 思维链内容：折叠面板展示
        if reasoning_content and role == "assistant":
            with st.expander("🧠 查看思考过程", expanded=False):
                st.markdown(
                    f'<div style="color: #888; font-size: 0.9em; '
                    f'line-height: 1.6;">{reasoning_content}</div>',
                    unsafe_allow_html=True,
                )

        # 消息正文
        st.markdown(content)
```

#### 🎬 视频要点（~18min）
1. **Expander 交互演示（5min）**：点击展开/折叠，展示两种状态
2. **HTML 样式解释（5min）**：`color: #888`（灰色文字）、`font-size: 0.9em`（略小）、`line-height: 1.6`（增加行间距）
3. **条件渲染（5min）**：只有 assistant 且有 reasoning_content 时才显示折叠面板

#### 📌 课后作业
- 尝试将 `expanded` 改为 `True`，观察默认展开效果
- 添加一个按钮，点击后将所有折叠面板同时展开

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
    """渲染欢迎屏幕（无对话历史时显示）"""
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

    # 示例提示词
    st.markdown("#### 💡 试试这些：")
    cols = st.columns(3)
    suggestions = [
        ("📝", "帮我写一段Python代码", "用 Python 实现一个简单的 HTTP 服务器"),
        ("🔍", "解释概念", "请通俗易懂地解释什么是机器学习"),
        ("💡", "头脑风暴", "我想做一个个人博客网站，给我一些技术选型建议"),
    ]
    for i, (icon, title, desc) in enumerate(suggestions):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #333;
                    border-radius: 10px;
                    padding: 15px;
                    height: 100%;
                    cursor: pointer;
                ">
                    <div style="font-size: 1.5em;">{icon}</div>
                    <div style="font-weight: bold; margin: 8px 0;">{title}</div>
                    <div style="color: #888; font-size: 0.85em;">{desc}</div>
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

---

### Day 20：`render_all_messages()` — 历史消息渲染

#### 🎯 教学目标
- 实现 `render_all_messages()` 遍历历史消息
- 集成 `get_all_messages()` 模块导入
- 理解条件渲染：欢迎页 vs 聊天历史

#### 📝 知识点
- **数据来源**：消息数据存储在 `st.session_state.messages` 中（Day 21 会深入讲解）
- **`get_all_messages()`**：返回消息列表（从 `chat_manager` 模块导入）
- **业务逻辑分离**：`chat_area.py` 只负责"渲染"，不负责"数据管理"

#### 📄 补充代码（`chat_area.py` 顶部添加导入）

```python
from ..chat_manager import get_all_messages


def render_all_messages() -> None:
    """渲染所有历史消息"""
    messages = get_all_messages()
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        reasoning = msg.get("reasoning_content")
        render_message(role, content, reasoning)
```

#### 📄 更新 `app.py`

```python
from src.ui.chat_area import render_all_messages, render_welcome
from src.chat_manager import init_messages, get_message_count

# 在 main() 中：
init_messages()

if get_message_count() == 0:
    render_welcome()
else:
    render_all_messages()
```

#### 🎬 视频要点（~18min）
1. **两种页面状态切换（5min）**：无消息 → 欢迎页；有消息 → 聊天历史
2. **`get_all_messages()` 导入链（5min）**：`chat_area.py` → `chat_manager.py` → `st.session_state`
3. **容错处理（5min）**：`msg.get("role", "user")` — 万一数据不完整，用默认值兜底

#### 📌 课后作业
- 手动在 `st.session_state.messages` 中添加几条假消息，观察渲染效果
- 实现：当鼠标悬停在消息上时，显示删除按钮

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

# 普通变量——每次 rerun 都会重置为 0
count_normal = 0

# session_state 变量——跨 rerun 持久
if "count_persistent" not in st.session_state:
    st.session_state.count_persistent = 0

if st.button("+1"):
    count_normal += 1
    st.session_state.count_persistent += 1

st.write(f"普通变量: {count_normal}")          # 永远是 1
st.write(f"持久变量: {st.session_state.count_persistent}")  # 每次 +1
```

#### 🎬 视频要点（~22min）
1. **对比实验（10min）**：上面这段代码，反复点击按钮，一个数永远是 1，另一个持续增长——直观展示区别
2. **原理图解（8min）**：画图解释 "rerun 时脚本从头执行，但 `session_state` 是保存在内存中的独立空间"
3. **字典 vs 属性访问（2min）**：两种写法等价，属性访问更简洁

#### 📌 课后作业
- 写一个简单的计数器应用：两个按钮分别 +1 和 -1，数值保持在 session_state 中
- 思考：如果没有 session_state，Streamlit 还能用来做什么？

---

### Day 22：`chat_manager.py` — 消息存储与读写

#### 🎯 教学目标
- 创建 `chat_manager.py` 封装所有 session_state 操作
- 实现消息初始化、添加用户消息、添加助手消息
- 理解封装的价值：调用方不需要知道底层是 session_state

#### 📝 知识点
- **封装原则**：`app.py` 不应该直接操作 `st.session_state.messages`，应该通过 `chat_manager` 的函数
- **消息数据结构**：
  ```python
  # 用户消息
  {"role": "user", "content": "你好"}

  # 助手消息
  {"role": "assistant", "content": "你好！", "reasoning_content": "让我想想..."}
  ```
- **`init_messages()` 的懒初始化**：只在第一次调用时创建空列表

#### 📄 创建文件

**src/chat_manager.py**（上半部分）：
```python
"""会话管理：多轮对话历史、思维链裁剪、上下文限制"""
from typing import Optional
import streamlit as st


# ---- 消息初始化 ----

def init_messages() -> None:
    """初始化消息列表（如果不存在）"""
    if "messages" not in st.session_state:
        st.session_state.messages = []


# ---- 消息操作 ----

def add_user_message(text: str) -> None:
    """添加用户消息到对话历史"""
    init_messages()
    st.session_state.messages.append({
        "role": "user",
        "content": text,
    })


def add_assistant_message(
    content: str,
    reasoning_content: Optional[str] = None,
) -> None:
    """添加助手回复（含可选的思维链推理内容）

    Args:
        content: 助手回复正文（Markdown 格式）
        reasoning_content: 思维链内容，仅用于本地展示，不会发给 API
    """
    init_messages()
    st.session_state.messages.append({
        "role": "assistant",
        "content": content,
        "reasoning_content": reasoning_content,
    })
```

#### 🎬 视频要点（~22min）
1. **封装演示（8min）**：对比直接操作 `st.session_state.messages.append(...)` vs 调用 `add_user_message(...)`——后者更清晰、更不容易出错
2. **数据结构设计（5min）**：为什么每条消息是 dict？为什么有 `reasoning_content` 字段？
3. **`Optional[str]` 类型注解（3min）**：Python 3.10+ 的 `Optional[X]` = `X | None`
4. **`init_messages()` 防御性编程（3min）**：每个函数调用前都先 `init_messages()`，保证不会 KeyError

#### 📌 课后作业
- 写一个辅助函数 `get_last_user_message()` 返回最近一条用户消息
- 思考：如果消息量很大（1000+ 条），当前的数据结构会有什么问题？

---

### Day 23：`chat_manager.py` — 查询、清空与 API 消息构建

#### 🎯 教学目标
- 实现消息查询函数（计数、获取全部）
- 实现 `clear_history()` 清空功能
- 实现 `build_api_messages()` — 最关键的 API 消息转换

#### 📝 知识点
- **本地消息 vs API 消息**：本地消息包含 `reasoning_content`（给用户看），API 消息不能包含（协议要求）
- **DeepSeek API 的关键约束**：多轮对话时，历史 assistant 消息中的 `reasoning_content` 字段会导致 400 错误
- **消息裁剪策略**：`build_api_messages()` 遍历所有消息，只保留 `role` 和 `content`

#### 📄 补充代码（`chat_manager.py` 下半部分）

```python
# ---- 消息查询 ----

def get_message_count() -> int:
    """当前消息总数"""
    init_messages()
    return len(st.session_state.messages)


def get_all_messages() -> list[dict]:
    """获取所有消息（含 reasoning_content，用于本地展示）"""
    init_messages()
    return st.session_state.messages


def clear_history() -> None:
    """清空所有对话历史"""
    init_messages()
    st.session_state.messages = []


# ---- API 消息构建 ----

def build_api_messages() -> list[dict[str, str]]:
    """构建发送给 DeepSeek API 的消息列表

    【关键规则】多轮对话中，必须移除历史 assistant 消息中的
    reasoning_content 字段，否则 API 返回 400 错误。

    由于消息在流式结束后才持久化到 session_state，
    所有历史消息中的 reasoning_content 都应该被剪掉。
    """
    init_messages()

    api_messages = []
    for msg in st.session_state.messages:
        clean_msg = {
            "role": msg["role"],
            "content": msg["content"],
            # 注意：不包含 reasoning_content！
        }
        api_messages.append(clean_msg)

    return api_messages
```

#### 🎬 视频要点（~25min）
1. **对比实验（8min）**：`print(get_all_messages())` vs `print(build_api_messages())`，直观看到 `reasoning_content` 被移除
2. **为什么必须裁剪（8min）**：用 DeepSeek 官方文档截图证明——如果发送 `reasoning_content`，API 直接返回 400
3. **`clear_history()` 的 rerun（5min）**：清空后必须 `st.rerun()` 才能看到欢迎页——因为 Streamlit 不自动刷新

#### 📌 课后作业
- 构造一条含 `reasoning_content` 的假消息，验证 `build_api_messages()` 是否正确裁剪
- 思考：如果 API 协议改变了，允许 reasoning_content，需要修改哪些代码？

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

#### 📄 在 `chat_manager.py` 末尾补充：
```python
from .config import CHARS_PER_TOKEN, TOKEN_WARNING_THRESHOLD


def estimate_token_count() -> int:
    """估算当前对话的总 token 数

    使用粗略的字符/token 比例：
    - 中文 ~1.5-2 字符/token
    - 英文 ~4 字符/token
    - 取保守值 2 字符/token（宁可多估）
    """
    init_messages()

    total_chars = 0
    for msg in st.session_state.messages:
        total_chars += len(msg.get("content", ""))
        # 思维链内容也占用 token
        if msg.get("reasoning_content"):
            total_chars += len(msg["reasoning_content"])

    return total_chars // CHARS_PER_TOKEN


def should_warn_token_limit() -> bool:
    """是否应发出 token 限制警告"""
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
"""Streamlit 侧边栏：模型选择、参数调节、会话管理"""
import streamlit as st
from ..config import (
    MODELS, DEFAULT_MODEL,
    get_api_key, set_api_key, validate_config,
)


def render() -> dict:
    """渲染侧边栏，返回当前用户设置字典"""
    st.sidebar.markdown("## ⚙️ 设置")

    # ---- API Key ----
    st.sidebar.markdown("### 🔑 API 密钥")
    env_key = get_api_key()
    valid, status_msg = validate_config()

    if valid:
        st.sidebar.success(status_msg)       # 绿色 ✅
    else:
        st.sidebar.warning(status_msg)       # 黄色 ⚠️

    # 密码输入框
    api_key_input = st.sidebar.text_input(
        "DeepSeek API Key",
        type="password",
        value=env_key or "",
        placeholder="sk-...",
        help="输入你的 DeepSeek API 密钥。可在 platform.deepseek.com/api_keys 获取。",
    )

    # 运行时更新密钥
    if api_key_input and api_key_input != env_key:
        set_api_key(api_key_input)

    st.sidebar.markdown("---")

    return {
        "api_key": api_key_input,
        # Day 26-27 继续补充其他字段
    }
```

#### 🐍 在 `app.py` 中调用：
```python
from src.ui.sidebar import render as render_sidebar

settings = render_sidebar()
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
from ..config import (
    MODELS, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS,
    MIN_MAX_TOKENS, MAX_MAX_TOKENS, TOKEN_STEP,
    get_model_label,    # 显示 "DeepSeek V4 Flash" 而非 "deepseek-v4-flash"
)

# ---- 模型选择 ----
st.sidebar.markdown("### 🤖 模型选择")

model_options = list(MODELS.keys())
default_index = model_options.index(DEFAULT_MODEL)

# 初始化或恢复选中的模型
if "selected_model" not in st.session_state:
    st.session_state.selected_model = model_options[default_index]

selected_model = st.sidebar.selectbox(
    "选择模型",
    options=model_options,
    format_func=get_model_label,  # 显示中文名称
    index=model_options.index(st.session_state.selected_model),
    key="model_selector",
)
st.session_state.selected_model = selected_model

# 显示模型描述
model_info = MODELS.get(selected_model, {})
st.sidebar.caption(model_info.get("description", ""))

st.sidebar.markdown("---")

# ---- 对话参数 ----
st.sidebar.markdown("### 🎛️ 对话参数")

# Temperature 滑块
temperature = st.sidebar.slider(
    "🌡️ Temperature",
    min_value=0.0,
    max_value=2.0,
    value=DEFAULT_TEMPERATURE,
    step=0.1,
    help="控制回复的随机性。越高越有创意，越低越确定。",
)

# Max Tokens 滑块
max_tokens = st.sidebar.slider(
    "📏 最大输出长度",
    min_value=MIN_MAX_TOKENS,
    max_value=MAX_MAX_TOKENS,
    value=DEFAULT_MAX_TOKENS,
    step=TOKEN_STEP,
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

```python
from ..config import supports_thinking
from ..chat_manager import (
    get_message_count, clear_history,
    should_warn_token_limit, estimate_token_count,
)

# ---- 思维链开关 ----
model_supports_thinking = supports_thinking(selected_model)

# 初始化
if "enable_thinking" not in st.session_state:
    st.session_state.enable_thinking = False

# 模型不支持时自动关闭
if not model_supports_thinking and st.session_state.enable_thinking:
    st.session_state.enable_thinking = False

enable_thinking = st.sidebar.checkbox(
    "🧠 思维链推理",
    value=st.session_state.enable_thinking,
    disabled=not model_supports_thinking,
    help="启用后展示推理过程。仅 V4 Pro 支持。",
)
st.session_state.enable_thinking = enable_thinking

thinking_mode = enable_thinking and model_supports_thinking

# Temperature 在思维链模式下无效
if thinking_mode:
    st.sidebar.caption("💡 思维链模式下 Temperature 参数无效")

st.sidebar.markdown("---")

# ---- 会话管理 ----
st.sidebar.markdown("### 💬 会话管理")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("消息数", get_message_count())
with col2:
    st.metric("估 Token", f"{estimate_token_count()}")

if should_warn_token_limit():
    st.sidebar.warning("⚠️ 对话已较长，建议清除历史")

if st.sidebar.button("🗑️ 清除对话历史", use_container_width=True):
    clear_history()
    st.rerun()

st.sidebar.markdown("---")

# ---- 关于 ----
st.sidebar.markdown("### 📖 关于")
st.sidebar.markdown("""
    **DeepSeek AI 聊天助手**
    基于 Streamlit + DeepSeek API 构建

    🎬 Bilibili 教程：[XianZS](https://space.bilibili.com/3690991649294439)
""")

# ---- 返回完整设置 ----
return {
    "api_key": api_key_input,
    "model": selected_model,
    "temperature": temperature,
    "max_tokens": max_tokens,
    "enable_thinking": enable_thinking,
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
- 如何使用 st.empty() 占位符实现渐进式 UI 更新
- 如何将 UI 渲染逻辑从业务编排中分离
- 如何抽象重复的 HTML 模板为可复用函数
"""
import streamlit as st
from .deepseek_client import chat_stream


def _render_reasoning_html(text: str, *, streaming: bool) -> str:
    """生成思维链折叠面板 HTML

    Args:
        text: 推理文本（已累积的全部内容）
        streaming: True → 展开面板 "🧠 思考中..."
                   False → 折叠面板 "🧠 查看思考过程"
    """
    return (
        f'<details{" open" if streaming else ""}>'
        f'<summary style="color: #888; cursor: pointer; font-size: 0.9em;">'
        f'{"🧠 思考中..." if streaming else "🧠 查看思考过程"}</summary>'
        f'<div style="color: #aaa; font-size: 0.85em; line-height: 1.6; '
        f'padding: 8px; border-left: 3px solid #555; margin-top: 4px;">'
        f'{text}</div></details>'
    )


def process_stream(
    api_key: str,
    api_messages: list[dict[str, str]],
    settings: dict,
    reasoning_placeholder,
    content_placeholder,
) -> tuple[str, str, bool]:
    """处理流式 LLM 响应并更新 UI 占位符

    调用方应在 with st.chat_message("assistant"): 内调用，
    调用前创建两个 st.empty() 占位符。

    Returns:
        (reasoning_text, content_text, has_error)
    """
    reasoning_text = ""
    content_text = ""
    has_error = False

    for chunk in chat_stream(
        api_key=api_key,
        messages=api_messages,
        model=settings["model"],
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        enable_thinking=settings["enable_thinking"],
    ):
        chunk_type = chunk["type"]

        if chunk_type == "reasoning":
            reasoning_text += chunk["text"]
            reasoning_placeholder.markdown(
                _render_reasoning_html(reasoning_text, streaming=True),
                unsafe_allow_html=True,
            )

        elif chunk_type == "content":
            content_text += chunk["text"]
            content_placeholder.markdown(content_text + "▌")

        elif chunk_type == "done":
            if reasoning_text:
                reasoning_placeholder.markdown(
                    _render_reasoning_html(reasoning_text, streaming=False),
                    unsafe_allow_html=True,
                )
            else:
                reasoning_placeholder.empty()
            content_placeholder.markdown(content_text)

        elif chunk_type == "error":
            if reasoning_text:
                reasoning_placeholder.empty()
            content_placeholder.error(chunk["message"])
            has_error = True
            break

    # 边界情况：模型未返回任何内容
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
  2. `build_api_messages()` → 裁剪后的消息列表
  3. `process_stream()` → 流式 UI 更新
  4. `add_assistant_message()` → 持久化回复
  5. `st.rerun()` → 刷新页面

#### 📄 最终版 `app.py`

```python
"""Streamlit 主程序入口：编排 UI 和业务逻辑"""
import streamlit as st

# ⚠️ set_page_config 必须是第一个 Streamlit 调用
st.set_page_config(
    page_title="DeepSeek AI 助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.ui.utils import inject_custom_css
from src.ui.sidebar import render as render_sidebar
from src.ui.chat_area import render_all_messages, render_welcome
from src.config import get_api_key, validate_config
from src.chat_manager import (
    init_messages,
    add_user_message,
    add_assistant_message,
    get_message_count,
    build_api_messages,
)
from src.stream_handler import process_stream


def main() -> None:
    """主程序入口：编排应用生命周期"""

    inject_custom_css()
    init_messages()

    # ---- 侧边栏 ----
    settings = render_sidebar()
    api_key = settings["api_key"] or get_api_key()
    valid, _ = validate_config()

    # ---- 主聊天区域 ----
    if get_message_count() == 0:
        render_welcome()
    else:
        render_all_messages()

    # ---- 聊天输入 ----
    chat_disabled = not valid

    if prompt := st.chat_input(
        "输入你的问题..." if not chat_disabled else "请先在侧边栏配置 API 密钥",
        disabled=chat_disabled,
    ):
        # 1. 记录用户消息
        add_user_message(prompt)
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # 2. 构建 API 消息（不含 reasoning_content）
        api_messages = build_api_messages()

        # 3. 流式处理 LLM 响应
        with st.chat_message("assistant", avatar="🤖"):
            reasoning_placeholder = st.empty()
            content_placeholder = st.empty()

            reasoning_text, content_text, _ = process_stream(
                api_key=api_key,
                api_messages=api_messages,
                settings=settings,
                reasoning_placeholder=reasoning_placeholder,
                content_placeholder=content_placeholder,
            )

        # 4. 持久化助手消息
        if content_text or reasoning_text:
            add_assistant_message(
                content=content_text if content_text else "（模型未返回文本内容）",
                reasoning_content=reasoning_text if reasoning_text else None,
            )

        # 5. 触发 rerun 刷新历史消息展示
        st.rerun()


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
# 1. 确保所有文件已提交
git status
git add .
git commit -m "feat: 完成 DeepSeek AI 聊天助手 v1.0"

# 2. 在 GitHub 创建新仓库
# 名称：deepseek-ai-chat-assistant
# 描述：基于 Streamlit + DeepSeek API 的 AI 聊天助手

# 3. 关联远程仓库并推送
git remote add origin https://github.com/XianZS/deepseek-ai-chat-assistant.git
git branch -M main
git push -u origin main
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
| Day 29 | — | `app.py`（完整编排） |
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
