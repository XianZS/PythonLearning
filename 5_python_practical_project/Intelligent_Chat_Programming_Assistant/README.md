# 🤖 DeepSeek AI 聊天助手

基于 **Streamlit + DeepSeek API** 构建的 AI 聊天应用，支持流式对话与思维链推理。

> 🎬 Bilibili 教程配套项目：[XianZS](https://space.bilibili.com/3690991649294439)

---

## ✨ 功能特性

- ⚡ **流式对话** — Token 级别实时输出，聊感流畅
- 🧠 **思维链推理** — 深度思考过程可视化，支持折叠查看（DeepSeek V4 Pro）
- 🔄 **模型切换** — 一键在 V4 Flash（快速）和 V4 Pro（强力）之间切换
- 💬 **多轮对话** — 完整会话历史，上下文连贯
- 🎛️ **参数可调** — Temperature、Max Tokens 自由调节
- 🛡️ **错误处理** — 认证失败/限流/超时等场景的中文友好提示
- 🔑 **安全密钥管理** — .env 文件 + 侧边栏输入双通道

---

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.8+ 并激活虚拟环境：

```bash
conda activate PythonLearning
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install openai streamlit python-dotenv
```

### 3. 获取 API 密钥

访问 [DeepSeek 开放平台](https://platform.deepseek.com/api_keys) 注册账号并创建 API Key。

### 4. 配置密钥

**方式一：.env 文件（推荐）**

```bash
# 复制模板文件
cp .env.example .env

# 编辑 .env，填入你的真实密钥
DEEPSEEK_API_KEY=sk-your-real-key-here
```

**方式二：启动后在侧边栏手动输入**

### 5. 启动应用

```bash
streamlit run app.py
```

浏览器将自动打开 `http://localhost:8501`，开始对话吧！🎉

---

## 📁 项目结构

```
python_practical_project/
├── .env.example              # API Key 模板
├── requirements.txt          # 项目依赖
├── app.py                    # Streamlit 主入口
├── src/
│   ├── config.py             # 配置管理
│   ├── deepseek_client.py    # DeepSeek API 封装
│   ├── chat_manager.py       # 会话管理
│   └── ui/
│       ├── sidebar.py        # 侧边栏组件
│       ├── chat_area.py      # 聊天区域渲染
│       └── utils.py          # UI 工具
└── README.md
```

---

## 🎮 使用指南

### 基础对话

1. 启动后在底部输入框输入问题
2. 按 Enter 发送
3. AI 将流式返回回复

### 模型切换

侧边栏「模型选择」下拉框：

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| DeepSeek V4 Flash | 快速、经济 | 日常对话、简单问答 |
| DeepSeek V4 Pro | 高性能、可推理 | 复杂任务、编程、分析 |

### 思维链推理

选择 **DeepSeek V4 Pro** 后，勾选「🧠 思维链推理」：

- AI 会展示推理过程（可折叠面板）
- Temperature 参数将被忽略（DeepSeek API 限制）

### 参数调节

- **Temperature**：0.0 → 更确定，2.0 → 更有创意
- **最大输出长度**：控制单次回复的最大长度

---

## 🔧 技术栈

| 技术 | 用途 |
|------|------|
| [Streamlit](https://streamlit.io/) | Web UI 框架 |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | API 调用（DeepSeek 兼容） |
| [DeepSeek API](https://platform.deepseek.com/docs) | 大模型服务 |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | 环境变量管理 |

---

## 📺 Bilibili 教程

本项目为 Bilibili 系列教程「Python 小 Demo」的第 N 集配套代码。

- 频道主页：[XianZS](https://space.bilibili.com/3690991649294439)
- 系列合集：[Python 小 Demo 系列](https://space.bilibili.com/3690991649294439/lists/7284550)

---

## 📄 License

MIT © [XianZS](https://github.com/XianZS)
