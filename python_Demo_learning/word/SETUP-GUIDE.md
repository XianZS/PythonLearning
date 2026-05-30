# Hugo + Stack 主题完整配置指南

> 从零开始，搭建一个卡片式 Hugo 博客并部署到 GitHub Pages
>
> **配置方式：Hugo 默认单文件 `hugo.toml`**（不拆分 `config/_default/` 目录）

---

## 一、环境准备

### 1.1 安装 Git

```bash
# Windows: 下载安装 https://git-scm.com/download/win
# 验证
git --version
```

### 1.2 安装 Hugo（Extended 版本）

```bash
# Windows (winget 推荐)
winget install Hugo.Hugo.Extended

# Windows (Chocolatey)
choco install hugo-extended

# macOS
brew install hugo

# Linux (Arch)
sudo pacman -S hugo

# 验证 (必须看到 extended 字样)
hugo version
# 示例输出: hugo v0.162.1+extended windows/amd64
```

> ⚠️ **必须安装 Extended 版本**，Stack 主题依赖 SCSS 编译，普通版会报错。

---

## 二、创建 Hugo 项目

```bash
# 创建 Hugo 站点（自动生成 my-blog 目录）
hugo new site . --force
```

此时会生成以下目录结构：

```
my-blog/
├── hugo.toml           # 站点主配置（所有配置都写在这一个文件里）
├── archetypes/         # 文章模板
├── assets/             # Hugo 处理的资源
├── content/            # 文章和页面内容
├── data/               # 数据文件
├── layouts/            # 自定义模板
├── static/             # 静态文件（图片、CSS等）
└── themes/             # 主题文件夹
```

---

## 三、安装 Stack 主题

```bash
git init
# 使用 Git Submodule 安装（推荐，方便更新）
git submodule add https://github.com/CaiJimmy/hugo-theme-stack themes/stack
```

---

## 四、配置站点（Hugo 默认单文件方式）

> Hugo 默认使用单个 `hugo.toml` 文件管理所有配置。
> 下面把所有配置段合并写入同一个 `hugo.toml`，无需创建 `config/_default/` 目录。

直接用以下内容**替换** `hugo.toml` 的全部内容：

```toml
# ============================================================
# ① 站点基础配置
# ============================================================
baseURL                = 'https://xianzs.github.io/'
locale                 = 'zh-cn'
title                  = '我的博客'
theme                  = 'stack'
defaultContentLanguage = 'zh'
hasCJKLanguage         = true

# 分页：每页显示 5 篇文章
[pagination]
    pagerSize = 5

# 永久链接格式：文章 URL = /p/文章slug/
[permalinks]
    post = '/p/:slug/'
    page = '/:slug/'


# ============================================================
# ② 主题功能配置
# ============================================================
[params]
    mainSections   = ['post']
    rssFullContent = true
    favicon        = '/img/avatar.png'

    # 页脚版权起始年份
    [params.footer]
        since = 2025

    # 侧栏：头像、表情、签名
    [params.sidebar]
        emoji    = '📚'
        subtitle = '卡片式博客，记录我的所思所想。'
        avatar   = '/img/avatar.png'

    # 文章版权协议
    [params.article]
        [params.article.license]
            enabled = true
            default = 'Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)'

    # 首页和文章页的侧栏小组件
    [params.widgets]
        homepage = [
            { type = 'search' },
            { type = 'archives', params = { limit = 5 } },
            { type = 'categories', params = { limit = 10 } },
            { type = 'tag-cloud', params = { limit = 10 } },
        ]
        page     = [{ type = 'toc' }]

    # 评论系统（默认关闭）
    [params.comments]
        enabled  = false
        provider = 'disqus'

    # Cookie  consent（默认关闭）
    [params.cookies]
        enabled = false
        [params.cookies.categories]
            analytics  = false
            functional = false


# ============================================================
# ③ 语言配置（仅中文站点，无需多语言切换）
# ============================================================
[languages.zh]
    locale = 'zh-cn'
    label  = '简体中文'
    title  = '我的博客'
    weight = 1


# ============================================================
# ④ 导航菜单 + 社交链接
#    注意：[[social]] 和 [[main]] 是 TOML 数组表，
#    每个 [[...]] 代表数组中的一个元素
# ============================================================

# -- 社交链接（显示在侧栏） --
[[social]]
    identifier = 'github'
    name       = 'GitHub'
    url        = 'https://github.com/xianzs'
    [social.params]
        icon = 'brand-github'

[[social]]
    identifier = 'twitter'
    name       = 'Twitter'
    url        = 'https://twitter.com'
    [social.params]
        icon = 'brand-twitter'

# -- 顶部导航菜单 --
[[main]]
    name       = '文章'
    url        = '/post'
    weight     = 1
    [main.params]
        icon = 'home'

[[main]]
    name       = '分类'
    url        = '/categories'
    weight     = 2
    [main.params]
        icon = 'categories'

[[main]]
    name       = '归档'
    url        = '/archives'
    weight     = 3
    [main.params]
        icon = 'archives'

[[main]]
    name       = '关于'
    url        = '/about'
    weight     = 4
    [main.params]
        icon = 'user'

[[main]]
    name       = '搜索'
    url        = '/search'
    weight     = 5
    [main.params]
        icon = 'search'


# ============================================================
# ⑤ Markdown 渲染 + 代码高亮
# ============================================================
[markup.goldmark]
    # 允许 Markdown 中嵌入 HTML
    [markup.goldmark.renderer]
        unsafe = true

    # 数学公式定界符：$$...$$ 是块级公式，\(...\) 是行内公式
    [markup.goldmark.extensions]
        [markup.goldmark.extensions.passthrough]
            enable = true
            [markup.goldmark.extensions.passthrough.delimiters]
                block  = [['\\[', '\\]'], ['$$', '$$']]
                inline = [['\\(', '\\)']]

# 文章目录（Table of Contents）
[markup.tableOfContents]
    endLevel   = 4
    ordered    = true
    startLevel = 2

# 代码块语法高亮
[markup.highlight]
    noClasses          = false
    codeFences         = true
    guessSyntax        = true
    lineNoStart        = 1
    lineNos            = true
    lineNumbersInTable = true
    tabWidth           = 4


# ============================================================
# ⑥ 相关文章推荐
# ============================================================
[related]
    includeNewer = true
    threshold    = 60
    toLower      = false
    indices      = [
        { name = 'tags', weight = 100 },
        { name = 'categories', weight = 200 },
    ]
```

### 配置结构速查

上面这个 `hugo.toml` 包含 6 个配置段，对应关系如下：

| 段 | TOML 键 | 说明 |
|----|---------|------|
| ① 站点基础 | 顶级键 (`baseURL`, `title`, …) | 站点域名、标题、主题、分页、永久链接 |
| ② 主题功能 | `[params]` | 侧栏、小组件、评论、Cookie |
| ③ 语言配置 | `[languages.zh]` | 中文站点语言与侧栏文案 |
| ④ 导航菜单 | `[[social]]` / `[[main]]` | 社交图标链接 + 顶部导航栏 |
| ⑤ Markdown | `[markup]` | Goldmark 扩展、代码高亮、目录 |
| ⑥ 相关文章 | `[related]` | 文章底部"相关推荐"的匹配规则 |

> 💡 **TOML 语法提示**：
> - `[section]` 定义一个表（字典），子键用 `[section.sub]` 嵌套
> - `[[array]]` 定义一个**数组表**，每个 `[[array]]` 向数组中追加一个元素
> - `{ key = 'value' }` 是内联表，等价于 `[parent]\n  key = 'value'`

---

## 五、创建内容页面

### 5.1 创建目录结构

```bash
mkdir -p content/post
mkdir -p content/page/about
mkdir -p content/page/archives
mkdir -p content/page/search
mkdir -p content/categories
mkdir -p static/img
```

### 5.2 首页 `content/_index.md`

```markdown
---
menu:
    main:
        name: 首页
        weight: -100
        params:
            icon: home
---
```

### 5.3 关于页 `content/page/about/index.md`

```markdown
---
title: 关于
description: 关于我
date: 2025-01-01
menu:
    main:
        weight: -90
        params:
            icon: user
---

## 👋 关于我

写一段自我介绍...

## 📬 联系方式

- GitHub: [你的用户名](https://github.com/)
- Email: your@email.com
```

### 5.4 归档页 `content/page/archives/index.md`

```markdown
---
title: "归档"
date: 2026-05-28
layout: "archives"
slug: "archives"
menu:
    main:
        weight: -70
        params:
            icon: archives
---
```

### 5.5 搜索页 `content/page/search/index.md`

```markdown
---
title: "搜索"
slug: "search"
layout: "search"
outputs:
    - html
    - json
menu:
    main:
        weight: -60
        params:
            icon: search
---
```

---

## 六、创建第一篇文章

### 6.1 建立文章目录

```bash
mkdir -p content/post/hello-stack
```

### 6.2 创建文章 `content/post/hello-stack/index.md`

由于站点默认语言已设为 `zh`，文章文件直接命名为 `index.md` 即可（无需 `index.zh.md`）：

```markdown
---
title: "你好 Stack！我的第一篇博客"
slug: "hello-stack"
description: "使用 Hugo Stack 主题搭建博客的初体验"
date: 2025-05-30
lastmod: 2025-05-30
categories:
    - Blog
tags:
    - Hugo
    - Stack
    - 教程
image: cover.jpg
---

## 🚀 开始写博客

Stack 主题的**卡片式布局**让每篇文章都像一张精美的卡片。

### 代码高亮

​```python
def hello():
    print("Hello, Hugo Stack!")
​```

### 表格

| 功能 | 说明 |
|------|------|
| 暗色模式 | 自动跟随系统 |
| 搜索 | Fuse.js 全文搜索 |
| 图片 | PhotoSwipe 灯箱 |

### 数学公式

行内公式 $E = mc^2$ 和块级公式：

$$
\int_{a}^{b} f(x)\,dx
$$

### 摘要分隔

`<!--more-->` 以上的内容显示在首页卡片中作为摘要，点击"阅读全文"后能看到以下内容。

> 千里之行，始于足下。开始记录你的想法吧！
```

---

## 七、放入头像和封面图

```bash
# 头像：放到 static/img/avatar.png
# 尺寸建议 256×256，支持 png/jpg/webp

# 封面图：放在文章目录里
# content/post/hello-stack/cover.jpg
# 建议 1200×630 或 1920×1080
```

> 如果暂时没有图片，Hugo 也能正常运行，只是没有封面图和头像。

---

## 八、本地预览

```bash
# 启动开发服务器（含草稿）
hugo server -D

# 或者指定端口
hugo server -D --port 8080
```

**打开浏览器** → `http://localhost:8080`

此时你应该看到：

```
┌──────────────────────────────────────────┐
│  📚 我的博客                               │
│  卡片式博客，记录我的所思所想。               │
│                                          │
│  ┌──────────────────────┐ ┌───────────┐ │
│  │                      │ │ 🔍 搜索   │ │
│  │  你好 Stack！         │ │ 📂 归档   │ │
│  │  我的第一篇博客        │ │ 🏷️ 标签   │ │
│  │                      │ │           │ │
│  └──────────────────────┘ └───────────┘ │
└──────────────────────────────────────────┘
```

Hugo 支持**热重载**：修改任何文件保存后，浏览器自动刷新。

---

## 九、自定义调整

### 9.1 修改主题配色

Stack 主题默认支持亮色/暗色模式，配色通过 CSS 变量控制。创建 `assets/scss/variables.scss`：

```scss
// 亮色模式
:root {
    --card-background: #ffffff;
    --body-background: #f5f5f5;
}
```

[完整配色变量参考](https://stack.jimmycai.com/p/change-theme-color/)

### 9.2 开启评论（Giscus）

1. 去 [giscus.app](https://giscus.app) 配置你的仓库
2. 修改 `hugo.toml` 中的 `[params.comments]` 段：

```toml
[params.comments]
    enabled  = true
    provider = 'giscus'

    [params.comments.giscus]
        repo               = '用户名/仓库名'
        repoID             = 'R_kgDO...'
        category           = 'Announcements'
        categoryID         = 'DIC_kw...'
        mapping            = 'pathname'
        lightTheme         = 'light'
        darkTheme          = 'dark_dimmed'
        reactionsEnabled   = 1
        emitMetadata       = 0
```

### 9.3 添加快捷新建文章脚本

Linux/macOS 创建 `new-post.sh`：

```bash
#!/bin/bash
SLUG=$1
mkdir -p content/post/$SLUG
cat > content/post/$SLUG/index.md << EOF
---
title: "$SLUG"
slug: "$SLUG"
description: ""
date: $(date +%Y-%m-%d)
categories: []
tags: []
image: cover.jpg
draft: true
---

EOF
echo "✅ 创建成功: content/post/$SLUG/index.md"
```

Windows PowerShell 创建 `new-post.ps1`：

```powershell
param($slug)
$dir = "content/post/$slug"
New-Item -ItemType Directory -Path $dir -Force
$date = Get-Date -Format "yyyy-MM-dd"
@"
---
title: "$slug"
slug: "$slug"
description: ""
date: $date
categories: []
tags: []
image: cover.jpg
draft: true
---
"@ | Out-File -FilePath "$dir/index.md" -Encoding UTF8
Write-Host "✅ 创建成功: $dir/index.md"
```

---

## 十、部署到 GitHub Pages

### 10.1 创建仓库

- **个人站点**：创建 `<用户名>.github.io`
- **项目站点**：建任意仓库，开启 Pages 后 URL 为 `<用户名>.github.io/<项目名>`

### 10.2 本地构建站点

```bash
hugo --minify
```

构建完成后，静态网站在 `public/` 目录下。把这个目录的内容推送到 `gh-pages` 分支即可。

### 10.3 推送到 gh-pages 分支

**首次部署（二选一）**：

#### 方式 A：手动命令

```bash
# 1. 构建站点
hugo --minify

# 2. 进入 public 目录，初始化为独立 git 仓库
cd public
git init
git checkout -b gh-pages

# 3. 关联远程仓库（替换为你的仓库地址）
git remote add origin git@github.com:xianzs/xianzs.github.io.git

# 4. 提交并强制推送到 gh-pages 分支
git add --all
git commit -m "首次部署"
git push -f origin gh-pages

# 5. 返回项目根目录
cd ..
```

> `-f` 强制推送只在第一次需要（覆盖可能存在的旧 gh-pages）。后续部署可去掉 `-f`。

#### 方式 B：一键部署脚本（推荐）

Linux/macOS 创建 `deploy.sh`：

```bash
#!/bin/bash
set -e

REPO="git@github.com:你的用户名/你的用户名.github.io.git"

echo "🔨 构建站点..."
hugo --minify

echo "📦 部署到 gh-pages..."
cd public
git init
git checkout -B gh-pages
git add --all
git commit -m "Deploy: $(date +%Y-%m-%d-%H:%M:%S)"
git remote add origin $REPO 2>/dev/null || true
git push -f origin gh-pages
cd ..

echo "✅ 部署完成！等 1-2 分钟后访问 https://你的用户名.github.io"
```

Windows PowerShell 创建 `deploy.ps1`：

```powershell
$ErrorActionPreference = "Stop"
$repo = "git@github.com:你的用户名/你的用户名.github.io.git"
$timestamp = Get-Date -Format "yyyy-MM-dd-HH:mm:ss"

Write-Host "🔨 构建站点..." -ForegroundColor Cyan
hugo --minify

Write-Host "📦 部署到 gh-pages..." -ForegroundColor Cyan
Push-Location public
git init
git checkout -B gh-pages
git add --all
git commit -m "Deploy: $timestamp"
git remote add origin $repo 2>$null
git push -f origin gh-pages
Pop-Location

Write-Host "✅ 部署完成！等 1-2 分钟后访问 https://你的用户名.github.io" -ForegroundColor Green
```

**后续部署**只需要运行脚本（或重复方式 A 的命令），每次写完文章后执行一次。

### 10.4 启用 GitHub Pages

1. 打开仓库 → **Settings** → **Pages**
2. **Source**：选择 **"Deploy from a branch"**
3. **Branch**：选择 **`gh-pages`**，目录选 **`/ (root)`**
4. 点击 **Save**

> **说明**：这个流程是在本地用 Hugo 构建站点，然后把 `public/` 目录推送到仓库的 `gh-pages` 分支。GitHub Pages 直接从 `gh-pages` 分支提供服务。不需要 GitHub Actions，完全在本地控制。

### 10.5 推送源代码（可选但推荐）

博客的源代码（`hugo.toml`、`content/`、`themes/` 等）建议也推送到 `main` 分支备份：

```bash
git add .
git commit -m "初始化 Hugo Stack 博客"
git branch -M main
git push -u origin main
```

> `main` 分支存源代码，`gh-pages` 分支存生成的网站。两者互不干扰。

### 10.6 常见问题排查

| 现象 | 原因 | 解决 |
|------|------|------|
| 网站 404 | Pages 未启用或分支选错 | 按 10.4 检查 Source 选 `gh-pages`、目录选 `/ (root)` |
| 网站样式错乱 | `baseURL` 配置不对 | 检查 `hugo.toml` 中 `baseURL` 是否以 `/` 结尾 |
| `public/` 目录为空 | Hugo 构建未成功 | 运行 `hugo --minify` 查看是否有报错 |
| 推送时权限错误 | SSH Key 未配置 | `ssh -T git@github.com` 测试连接 |
| `gh-pages` 分支不存在 | 首次部署前需要推送 | 先执行 10.3 的推送命令 |

---

## 十一、常用命令速查

| 操作 | 命令 |
|------|------|
| 本地预览 | `hugo server -D` |
| 构建站点 | `hugo` |
| 构建（压缩） | `hugo --minify` |
| 一键部署 | `bash deploy.sh` / `powershell .\deploy.ps1` |
| 新建文章 | `hugo new content post/文章名/index.md` |
| 更新主题 | `cd themes/stack && git pull && cd ../..` |
| 查看所有页面 | `hugo list all` |
| 查看草稿 | `hugo server -D` |

---

## 附录：文件职责速查表

| 文件/目录 | 作用 | 改什么 |
|-----------|------|--------|
| `hugo.toml` | **所有站点配置**（默认单文件方式） | 标题、域名、主题开关、导航、代码高亮等 |
| `content/post/*/index.md` | 文章 | **写博客文章** |
| `content/post/*/cover.jpg` | 文章封面 | 替换为你的封面图 |
| `content/page/about/index.md` | 关于页 | 自我介绍 |
| `content/page/archives/index.md` | 归档页 | 无需改动 |
| `content/page/search/index.md` | 搜索页 | 无需改动 |
| `static/img/avatar.png` | 头像 | 替换为你的头像 |
| `assets/scss/variables.scss` | 自定义主题配色 | CSS 变量覆盖 |
| `themes/stack/` | 主题源码 | **不要改** |
| `deploy.sh` / `deploy.ps1` | 一键部署脚本 | 本地构建并推送到 gh-pages 分支 |
| `public/` | 生成的静态网站 | Hugo 自动生成，**不要手动编辑** |

---

## 附录 B：TOML 语法快速参考

Hugo 默认使用 TOML 格式的 `hugo.toml` 作为配置文件。以下是单文件配置中常见的语法：

```toml
# 1. 顶级键值对 — 直接写
baseURL = 'https://example.org/'
theme  = 'stack'

# 2. 表（字典/分组）— 用 [名称]
[pagination]
    pagerSize = 5

# 3. 嵌套表 — 用点号连接
[params.sidebar]
    emoji    = '📚'
    subtitle = '一句话介绍'

# 4. 数组表（列表中的字典）— 用 [[名称]]
#    每个 [[...]] 是数组中的一个元素
[[main]]
    name   = 'Posts'
    url    = '/post'
    weight = 1

[[main]]
    name   = 'About'
    url    = '/about'
    weight = 2

# 5. 内联数组/表 — 用方括号/花括号
indices = [
    { name = 'tags', weight = 100 },
    { name = 'categories', weight = 200 },
]

# 6. 字符串可以用单引号或双引号，效果相同
title = '我的博客'
title = "我的博客"
```

> 更多 TOML 语法参考：[toml.io](https://toml.io/cn/)
