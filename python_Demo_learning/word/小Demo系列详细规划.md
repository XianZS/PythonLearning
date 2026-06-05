# 小Demo系列详细规划（人格化重构版）

> 创建日期：2026-06-01 ｜ 最后更新：2026-06-02

---

## Demo 总览

```
┌──────────────────────────────────────────────────────────────────┐
│  #   Demo名称                   集数   气质      核心卖点         │
├──────────────────────────────────────────────────────────────────┤
│  1   实时系统监控面板             3集   繁       黑客风终端仪表盘  │
│  2   图片→彩色字符画             2集   美       图片在终端里"活"了 │
│  3   词云生成器                  3集   意       数据变成艺术品     │
│  4   间谍情报术——图片隐写         2集   藏       两张一样的图藏了秘密│
│  5   二维码艺术生成器             2集   雅       扫出来那一刻的惊喜  │
│  6   终端贪吃蛇                  2集   趣       用代码写游戏       │
└──────────────────────────────────────────────────────────────────┘
```

---

---

## Demo 1：实时系统监控面板（第1~3集）

### 技术理论重述：psutil——操作系统审讯官

psutil 是一个"系统审讯官"——它不修改任何东西，只是**问**操作系统：你用了多少CPU？内存还剩多少？谁占了最多资源？每秒有多少数据从网卡流过？

传统教学把 psutil 讲成"获取系统信息的工具"。但这个Demo要换个视角：**psutil是在"审讯"操作系统，把藏在后台的数据全部拖出来示众**。CPU使用率不是"一个数字"，而是"你的电脑此时此刻有多忙"；进程列表不是"名字+内存"，而是"谁在背后偷你的资源"。

这个视角转换很重要：代码不是在"读取数据"，而是在"拷问系统"——观众会带着一种侦探式的好奇心学下去。

psutil 的核心概念模型：

```
操作系统内核
    │
    ├── CPU 统计 ──→ cpu_percent()      ──→ "CPU现在有多忙？"
    ├── 内存统计 ──→ virtual_memory()    ──→ "内存还剩多少？"
    ├── 磁盘统计 ──→ disk_usage()        ──→ "硬盘快满了吗？"
    ├── 网络统计 ──→ net_io_counters()   ──→ "网速是多少？"
    └── 进程列表 ──→ process_iter()      ──→ "谁在偷我的资源？"
```

每一行 `import psutil` 之后的代码，都是在向操作系统发射"审讯信号"。

---

### 第1集：你的电脑在说话——psutil获取系统信息

**时长：** ~10分钟

**学习目标：** 安装psutil，获取CPU/内存/磁盘/网络/进程/交换内存/磁盘I/O/电池/启动时间等全方位系统信息

**代码框架：**

```python
import psutil
import os
import time
from datetime import datetime

def get_process_top(n=8):
    """审讯所有进程：按内存占用排序，揪出最占资源的N个（带CPU%和内存）"""
    procs = []
    for p in psutil.process_iter(['name', 'memory_info', 'cpu_percent']):
        try:
            name = p.info['name'][:20]
            mem_mb = p.info['memory_info'].rss / 1024 / 1024
            cpu_pct = p.info['cpu_percent'] or 0
            procs.append((name, cpu_pct, mem_mb))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    procs.sort(key=lambda x: x[2], reverse=True)  # 按内存排序
    return procs[:n]

def get_battery():
    """审讯电池：剩多少电？插着电源吗？"""
    try:
        bat = psutil.sensors_battery()
        if bat:
            status = "🔌 充电中" if bat.power_plugged else "🔋 放电中"
            return f"{status} | {bat.percent:.0f}%"
    except Exception:
        pass
    return None

def get_temp():
    """审讯温度传感器：CPU多热了？"""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        for name in ['coretemp', 'k10temp', 'cpu_thermal', 'acpitz']:
            if name in temps and temps[name]:
                return temps[name][0].current
        first = next(iter(temps.values()))
        if first:
            return first[0].current
    except Exception:
        pass
    return None

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    # ===== 审讯 CPU =====
    # interval=0.5：观察0.5秒，返回整体使用率
    cpu = psutil.cpu_percent(interval=0.5)
    # percpu=True：逐个核心审讯，返回列表——"谁在偷懒一目了然"
    per_cpu = psutil.cpu_percent(interval=0, percpu=True)
    cpu_freq = psutil.cpu_freq()          # 当前主频
    cpu_count_logical = psutil.cpu_count()        # 逻辑核心数（含超线程）
    cpu_count_physical = psutil.cpu_count(logical=False)  # 物理核心数

    # ===== 审讯 内存 & 交换空间 =====
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()           # 交换空间——"内存不够时被赶去硬盘的数据"

    # ===== 审讯 磁盘 =====
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()   # 磁盘累计读写量

    # ===== 审讯 网络 =====
    net = psutil.net_io_counters()        # 网卡累计收发量

    # ===== 审讯 传感器 =====
    cpu_temp = get_temp()
    battery = get_battery()

    # ===== 审讯 启动时间 =====
    boot_time = datetime.fromtimestamp(psutil.boot_time())

    # ===== 信息面板——数据扑面而来 =====
    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║           ⚡ 系 统 监 控 面 板 ⚡                ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  系统启动于: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}         ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  🖥  CPU 总使用率:  {cpu:>5.1f}%                      ║")
    if cpu_freq:
        print(f"║  ⚡ CPU 主频:       {cpu_freq.current:>5.0f} MHz                  ║")
    print(f"║  🔢 CPU 核心:       {cpu_count_physical}物理 / {cpu_count_logical}逻辑            ║")
    # 每核热力图：█ 颜色深浅表示负载
    core_heat = ""
    for c in per_cpu:
        if c < 25:
            core_heat += f"\033[32m█\033[0m"    # 绿色：空闲
        elif c < 50:
            core_heat += f"\033[33m█\033[0m"    # 黄色：中等
        elif c < 75:
            core_heat += f"\033[38;5;208m█\033[0m"  # 橙色：忙碌
        else:
            core_heat += f"\033[31m█\033[0m"    # 红色：满载
    print(f"║  每核状态: {core_heat}     ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  🧠 内存: {mem.percent:>5.1f}%  ({mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB)   ║")
    if swap.total > 0:
        print(f"║  🔄 交换: {swap.percent:>5.1f}%  ({swap.used/1024**3:.1f}/{swap.total/1024**3:.1f} GB)   ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  💾 磁盘: {disk.percent:>5.1f}%  ({disk.used/1024**3:.1f}/{disk.total/1024**3:.1f} GB)   ║")
    print(f"║  📀 磁盘读: {disk_io.read_bytes/1024**3:>8.2f} GB    写: {disk_io.write_bytes/1024**3:>8.2f} GB ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  📡 网络 已发送: {net.bytes_sent/1024**3:>8.2f} GB  已接收: {net.bytes_recv/1024**3:>8.2f} GB ║")
    print(f"╠══════════════════════════════════════════════════╣")
    if cpu_temp:
        print(f"║  🌡  CPU 温度:      {cpu_temp:>5.0f}°C                     ║")
    if battery:
        print(f"║  🔋 电池:          {battery}                 ║")
    if cpu_temp or battery:
        print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  🔝 内存占用 Top 8:                                ║")
    for i, (name, cpu_pct, mem_mb) in enumerate(get_process_top(8), 1):
        print(f"║    {i}. {name:<22s} {mem_mb:>7.0f} MB  (CPU {cpu_pct:>5.1f}%)  ║")
    print(f"╚══════════════════════════════════════════════════╝")

    time.sleep(1)
```

> **代码说明：** `cpu_percent(interval=0.5)` 会让程序暂停0.5秒来测量CPU使用率，这是 psutil 的设计——它需要一段观察窗口来计算使用率。之后 `cpu_percent(interval=0, percpu=True)` 会复用刚才的测量窗口返回每核数据，不会再次阻塞。`cpu_freq()` 返回当前主频（部分平台不可用）。`swap_memory()` 在部分云服务器上 total=0（未配置交换空间），代码已做兜底。`sensors_battery()` 在台式机上返回 None。后续用Rich做Live刷新时会用更精细的方式处理。

**作业：** 尝试把刷新间隔改成0.5秒，观察CPU占用率的变化。

---

### 第2集：告别黑白——Rich让终端输出媲美网页

**时长：** ~10分钟

**学习目标：** Rich的Table、Panel、Progress、Layout、Live组件

**代码框架：**

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich import box
import time

console = Console()

# ========== 第1步：Console基础——彩色文字 & Emoji ==========
console.print("[bold cyan]🚀 Rich库体验开始[/bold cyan]")
console.print("[red]█[/red][yellow]█[/yellow][green]█[/green][blue]█[/blue][magenta]█[/magenta]")

# ========== 第2步：Table表格 + Panel面板——信息分类是"繁而不乱"的关键 ==========
table = Table(title="[bold]系统状态[/bold]", box=box.ROUNDED, border_style="cyan")
table.add_column("指标", style="yellow")
table.add_column("数值", style="bold green")
table.add_row("CPU", "23.5%")
table.add_row("内存", "8.2GB / 16GB")

panel = Panel(table, title="[bold white]⚡ 实时监控[/bold white]",
              border_style="green", padding=(1, 2))
console.print(panel)

# ========== 第3步：Progress进度条——"繁"的最佳载体 ==========
console.print("\n[bold]模拟任务进度：[/bold]")
with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
) as progress:
    task = progress.add_task("[cyan]加载系统模块...", total=100)
    while not progress.finished:
        progress.update(task, advance=2)
        time.sleep(0.02)

# ========== 第4步：Layout分栏 + Live动态刷新（核心！告别闪烁） ==========
layout = Layout()
layout.split(Layout(name="top"), Layout(name="bottom"))
layout["top"].update(Panel("CPU + 内存信息", title="[bold]上部[/bold]"))
layout["bottom"].update(Panel("网络 + 磁盘信息", title="[bold]下部[/bold]"))

console.print("\n[bold]Live动态刷新演示（3秒）：[/bold]")
with Live(layout, refresh_per_second=4) as live:
    for i in range(8):
        layout["top"].update(
            Panel(f"CPU: {23.5 + i*2:.1f}%  内存: {45.2 + i*3:.1f}%",
                  title="[bold]上部[/bold]"))
        time.sleep(0.3)
```

> **关键认知：** Rich 的核心价值不是"好看"，而是**让密集信息变得可读**。Table 把数字分类，Panel 把表格分组，Layout 把面板分区——这是"繁而不乱"的秘诀。

**作业：** 用Rich的Table把上集的psutil数据美化输出。

---

### 第3集：整合——赛博朋克风实时仪表盘

**时长：** ~10分钟

**学习目标：** psutil+Rich.Live整合，进度条可视化，网络速率/磁盘I/O差值计算，每核CPU热力图，进程Top8动态刷新，多维度系统信息集中展示

**完整代码：**

```python
import psutil
import time
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich import box

console = Console()

# ===================== 渲染工具函数 =====================

def make_bar(percent, width=28):
    """彩色进度条——绿(<50)/黄(50~80)/红(>80)，危险一眼可见"""
    if percent < 50:
        color = "green"
    elif percent < 80:
        color = "yellow"
    else:
        color = "red"
    filled = int(width * percent / 100)
    return f"[{color}]{'█' * filled}{'░' * (width - filled)}[/{color}] {percent:5.1f}%"

def make_core_heat(per_cpu):
    """
    每核CPU热力图——紧凑的一行彩色方块
    每个核心一个█字符，颜色表示负载：
    绿(<25%) / 黄(25~50%) / 橙(50~75%) / 红(>75%)
    视觉上像热成像——哪颗核心在"发烧"一目了然
    """
    result = ""
    for p in per_cpu:
        if p < 25:
            result += "[green]█[/green]"
        elif p < 50:
            result += "[yellow]█[/yellow]"
        elif p < 75:
            result += "[dark_orange]█[/dark_orange]"
        else:
            result += "[red]█[/red]"
    return result

# ===================== 数据采集函数 =====================

def get_process_list(n=8):
    """审讯所有进程：按内存排序Top N，同时采集CPU%"""
    procs = []
    for p in psutil.process_iter(['name', 'memory_info', 'cpu_percent']):
        try:
            name = p.info['name'][:18]
            mem_mb = p.info['memory_info'].rss / 1024 / 1024
            cpu_pct = p.info['cpu_percent'] or 0
            procs.append((name, cpu_pct, mem_mb))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    procs.sort(key=lambda x: x[2], reverse=True)
    return procs[:n]

def get_delta_speed(prev_val, cur_val, elapsed):
    """通用差值速率计算：用于网络和磁盘I/O"""
    if elapsed == 0:
        return 0
    return (cur_val - prev_val) / elapsed / 1024  # KB/s

def get_battery_info():
    """审讯电池（笔记本专属，台式机返回None）"""
    try:
        bat = psutil.sensors_battery()
        if bat is None:
            return None
        pct = bat.percent
        if pct < 20:
            color = "red"
        elif pct < 50:
            color = "yellow"
        else:
            color = "green"
        status = "🔌" if bat.power_plugged else "🔋"
        return f"[{color}]{status} {pct:.0f}%[/{color}]"
    except Exception:
        return None

def get_temp_info():
    """审讯CPU温度传感器（跨平台兜底）"""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None
        for name in ['coretemp', 'k10temp', 'cpu_thermal', 'acpitz']:
            if name in temps and temps[name]:
                return temps[name][0].current
        first = next(iter(temps.values()))
        if first:
            return first[0].current
    except Exception:
        return None

# ===================== 主程序 =====================

def main():
    # ===== 架构层：Layout 五区域分栏 =====
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),     # 标题栏
        Layout(name="body"),                # 中部：资源(左) + 网络&传感器(右)
        Layout(name="processes", size=13),  # 底部：进程Top8
    )
    layout["body"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1),
    )

    # ===== 数据层：初始化跟踪变量 =====
    prev_net = psutil.net_io_counters()
    prev_disk = psutil.disk_io_counters()
    prev_time = time.time()
    start_time = time.time()
    boot_time = psutil.boot_time()
    cpu_count_logical = psutil.cpu_count()
    cpu_count_physical = psutil.cpu_count(logical=False)

    # ===== 渲染层：Rich Live 无闪烁刷新 =====
    with Live(layout, refresh_per_second=4, screen=True) as live:
        while True:
            # ---------- 数据采集：审讯系统的9个维度 ----------
            # CPU：用 percpu=True 一次拿到整体+每核（更高效）
            per_cpu = psutil.cpu_percent(interval=0.3, percpu=True)
            cpu = sum(per_cpu) / len(per_cpu) if per_cpu else 0
            cpu_freq = psutil.cpu_freq()

            # 内存 & 交换
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            # 磁盘 & 磁盘I/O速率（和网速一样的差值算法）
            disk = psutil.disk_usage('/')
            cur_disk = psutil.disk_io_counters()
            now = time.time()
            elapsed = now - prev_time
            disk_read = get_delta_speed(prev_disk.read_bytes,
                                        cur_disk.read_bytes, elapsed)
            disk_write = get_delta_speed(prev_disk.write_bytes,
                                         cur_disk.write_bytes, elapsed)

            # 网络 & 网络速率
            cur_net = psutil.net_io_counters()
            net_up = get_delta_speed(prev_net.bytes_sent,
                                     cur_net.bytes_sent, elapsed)
            net_down = get_delta_speed(prev_net.bytes_recv,
                                       cur_net.bytes_recv, elapsed)

            # 传感器
            temp = get_temp_info()
            battery = get_battery_info()

            # 连接数（可能较慢，包在try里）
            connections = None
            try:
                connections = len(psutil.net_connections())
            except Exception:
                pass

            # 更新跟踪状态
            prev_net = cur_net
            prev_disk = cur_disk
            prev_time = now
            uptime = now - start_time

            # ---------- Header: 标题 + 运行时间 + 启动时间 ----------
            uptime_str = f"{int(uptime//3600):02d}:{int(uptime%3600//60):02d}:{int(uptime%60):02d}"
            boot_str = datetime.fromtimestamp(boot_time).strftime("%m-%d %H:%M")
            header_text = (
                f"[bold cyan]╔══════════════════════════════════════════════════════════════╗\n"
                f"║  ⚡ 系 统 监 控 仪 表 盘    运行 {uptime_str}    启动于 {boot_str} ║\n"
                f"╚══════════════════════════════════════════════════════════════╝[/bold cyan]"
            )
            layout["header"].update(Panel(header_text, border_style="cyan"))

            # ---------- Left: 系统资源面板 ----------
            left = Table(box=box.SIMPLE, expand=True, show_header=False,
                        padding=(0, 1))
            left.add_column("", style="bold yellow", width=10)
            left.add_column("")

            # CPU：总进度条 + 频率 + 每核热力图 + 核心数
            freq_str = f" @ [bold]{cpu_freq.current:.0f} MHz[/bold]" if cpu_freq else ""
            left.add_row("🖥  CPU",
                        make_bar(cpu) + freq_str)
            if per_cpu:
                left.add_row("   每核",
                            f"{make_core_heat(per_cpu)}  "
                            f"[dim]{cpu_count_physical}物理/{cpu_count_logical}逻辑[/dim]")

            # 内存 + 交换
            mem_used_gb = (mem.total - mem.available) / 1024**3
            mem_total_gb = mem.total / 1024**3
            left.add_row("🧠  内存",
                        make_bar(mem.percent) +
                        f"  [dim]{mem_used_gb:.1f}/{mem_total_gb:.1f} GB[/dim]")

            if swap.total > 0:
                swap_used_gb = swap.used / 1024**3
                swap_total_gb = swap.total / 1024**3
                left.add_row("🔄  交换",
                            make_bar(swap.percent) +
                            f"  [dim]{swap_used_gb:.1f}/{swap_total_gb:.1f} GB[/dim]")

            # 磁盘 + 磁盘I/O速率
            disk_used_gb = disk.used / 1024**3
            disk_total_gb = disk.total / 1024**3
            left.add_row("💾  磁盘",
                        make_bar(disk.percent) +
                        f"  [dim]{disk_used_gb:.1f}/{disk_total_gb:.1f} GB[/dim]")
            left.add_row("📀  磁盘I/O",
                        f"[green]读 {disk_read:.1f} KB/s[/green]  "
                        f"[yellow]写 {disk_write:.1f} KB/s[/yellow]")

            layout["left"].update(
                Panel(left, title="[bold]📊 系统资源[/bold]", border_style="green")
            )

            # ---------- Right: 网络 & 传感器面板 ----------
            right = Table(box=box.SIMPLE, expand=True, show_header=False,
                         padding=(0, 1))
            right.add_column("", style="cyan", width=8)
            right.add_column("", style="bold")

            right.add_row("⬆  上传", f"[yellow]{net_up:.1f} KB/s[/yellow]")
            right.add_row("⬇  下载", f"[green]{net_down:.1f} KB/s[/green]")
            right.add_row("📡  总发送",
                         f"{cur_net.bytes_sent/1024**3:.2f} GB")
            right.add_row("📥  总接收",
                         f"{cur_net.bytes_recv/1024**3:.2f} GB")
            if connections is not None:
                right.add_row("🔗  连接数", f"[bold]{connections}[/bold]")

            # 传感器信息（仅可用时显示）
            if battery or temp is not None:
                right.add_row("", "")  # 分隔行
            if battery:
                right.add_row("🔋  电池", battery)
            if temp is not None:
                color = "green" if temp < 60 else ("yellow" if temp < 80 else "red")
                right.add_row("🌡  温度", f"[{color}]{temp:.0f} °C[/{color}]")

            layout["right"].update(
                Panel(right, title="[bold]🌐 网络 & 传感器[/bold]", border_style="blue")
            )

            # ---------- Processes: 内存占用 Top8 ----------
            proc_table = Table(box=box.SIMPLE, expand=True, padding=(0, 1))
            proc_table.add_column("#", style="dim", width=3, justify="right")
            proc_table.add_column("进程名", style="yellow", width=20)
            proc_table.add_column("CPU%", style="cyan", width=6, justify="right")
            proc_table.add_column("内存", style="bold red", width=10, justify="right")
            for i, (name, cpu_pct, mem_mb) in enumerate(get_process_list(8), 1):
                proc_table.add_row(
                    str(i), name,
                    f"{cpu_pct:.1f}",
                    f"{mem_mb:.0f} MB"
                )
            layout["processes"].update(
                Panel(proc_table, title="[bold]🔝 内存占用 Top 8[/bold]",
                      border_style="magenta")
            )

            time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold green]👋 监控结束，再见！[/bold green]")
```

> **架构说明：** 三层分离是这个Demo最重要的编程思维——数据层（psutil）只负责"审讯"，控制层（`get_delta_speed`等函数）负责"计算差值"，渲染层（Rich Live+Layout）负责"展示"。以后写任何实时应用都适用这个模式。
>
> **新增数据说明：**
> - **每核热力图**：`cpu_percent(interval=0.3, percpu=True)` 一次调用同时拿到整体和每核数据，绿色方块=空闲，红色方块=满载——比单个数字直观得多
> - **磁盘I/O速率**：和网速完全相同的差值算法，`(本次读写量 - 上次读写量) / 时间间隔`。首次运行时差值为0是正常的
> - **交换空间**：`swap_memory()` 在云服务器上可能 total=0（未配置），代码用 `if swap.total > 0` 做了兜底，这行不会显示
> - **电池/温度**：台式机上 `sensors_battery()` 返回 None，自动隐藏电池行；温度传感器在不同平台名称不同（`coretemp`/`k10temp`/`cpu_thermal`），已做遍历兜底
> - **连接数**：`net_connections()` 在部分系统上较慢或需要权限，包在 try/except 里静默跳过

**作业：** 给仪表盘增加一个"GPU信息"显示行（Windows上用 `GPUtil` 或 WMI，Linux/macOS 用 `nvidia-smi`），看看你的显卡有多忙。

---

---

## Demo 2：图片→彩色字符画（第4~5集）

> 气质：**美** —— 挑战"终端=黑白文字"的刻板印象。当你的照片在终端里以真彩色还原时，观众的认知会被打破——"这是终端吗？"

### 技术理论重述：Pillow——每个像素都有颜色，每个颜色都值得还原

传统字符画教程把一个彩色世界压扁成"`@%#*+=-:. `"几个灰度等级。这就像是把一幅油画变成铅笔素描——技艺再高也是降维。

但这个Demo的核心理念相反：**终端有真彩色能力（16.7M色），凭什么只用黑白的字符？**

Pillow在这里不是"图像处理库"，而是"颜色翻译官"：

```
照片（现实世界）──→ Pillow读取像素 ──→ Rich的rgb(r,g,b)渲染 ──→ 终端还原
     │                    │                      │
  3000万色              每个像素               █字符块+真彩色
                         (r,g,b)元组            在终端显示
```

关键认知：`Image.open()` 之后得到的不是一个"图片对象"，而是**一个 (r,g,b) 元组的二维矩阵**。你要做的事就是把每个元组翻译成终端能理解的色彩指令。这就是"美"的本质——不是创造，是忠实还原。

上一集用灰度字符画做铺垫是必要的：它让学生理解"像素→字符"的映射逻辑。但灰度只是跳板——**第二集的真彩色才是目的地**。

---

### 第4集：从像素到字符——灰度字符画

**时长：** ~10分钟

**学习目标：** PIL读取图片→缩放→灰度化→像素映射到字符→终端输出

**代码框架：**

```python
from PIL import Image

# ===== 字符集：画家的调色盘 =====
# 从暗到亮排列（视觉密度递减）
# @ 最密（笔画最多，代表最暗的像素）→ 空格最疏（代表最亮的像素）
# 你可以自定义这个序列——不同的字符集产生不同的艺术风格
CHARS = "@%#*+=-:. "

def image_to_ascii(image_path, width=120):
    """
    图片 → 灰度字符画（灰度版是彩色版本的"草稿"）
    
    算法流程：
    1. 打开图片，计算缩放后的尺寸
    2. 等比例缩放（保持构图比例）
    3. 转灰度（去掉颜色，只留明暗信息）
    4. 逐像素映射：亮度值(0~255) → 字符索引(0~len(CHARS)-1)
    5. 返回完整的字符串（可直接print）
    
    参数：
    - image_path: 图片路径（支持 jpg/png/bmp 等常见格式）
    - width: 输出的字符宽度（越大越精细，但终端可能显示不全）
    """
    img = Image.open(image_path)

    # 计算缩放后的高度
    # 终端字符的高宽比约2:1（一个字符的高度约等于两个字符的宽度）
    # 所以高度 = 宽度的像素比 × 0.5（补偿终端字符的扁长形状）
    # 示例：1920×1080照片，width=120
    #   aspect_ratio = 1080/1920 = 0.5625
    #   height = int(120 × 0.5625 × 0.5) = int(33.75) = 33
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)

    # 高质量缩放（将百万像素压缩为几千个字符的网格）
    # Image.LANCZOS：Lanczos滤波器，质量最高，适合缩小图片
    # （Pillow ≥10.0 中用 LANCZOS 替代了旧名称 ANTIALIAS）
    img = img.resize((width, height), Image.LANCZOS)

    # 转灰度模式 "L"
    # 转换公式：L = 0.299×R + 0.587×G + 0.114×B（人眼对不同颜色敏感度不同）
    # 之后 getpixel((x,y)) 返回单个整数 0(纯黑)~255(纯白)
    img = img.convert("L")

    # 逐像素映射：亮度 → 字符
    result = ""
    for y in range(height):
        for x in range(width):
            gray = img.getpixel((x, y))   # 0(黑) ~ 255(白)
            # 线性映射：gray=0→chars_idx=0('@'), gray=255→chars_idx=9(' ')
            # gray * (len(CHARS) - 1) // 255 是整数运算版本的归一化
            char_idx = gray * (len(CHARS) - 1) // 255
            result += CHARS[char_idx]
        result += "\n"   # 每行结束加换行

    return result

# ===== 使用示例 =====
ascii_art = image_to_ascii("your_photo.jpg", width=150)
print(ascii_art)

# 保存为txt文件——方便截图分享到评论区
with open("ascii_output.txt", "w", encoding="utf-8") as f:
    f.write(ascii_art)
```

> **代码说明：** `Image.LANCZOS` 是高质量缩放算法（Pillow 新版替代了旧名称 `ANTIALIAS`）。`getpixel((x,y))` 在"L"模式下返回单个灰度值（0-255）。

**作业：** 换一张自己的照片，调整 width 参数（试试60/100/150），看不同宽度的效果。

---

### 第5集：真彩色字符画——让终端"还原"你的照片

**时长：** ~10分钟

**学习目标：** 保留颜色→逐像素RGB→Rich彩色渲染→终端真彩色输出。**本集是视觉巅峰。**

**代码框架：**

```python
from PIL import Image
from rich.console import Console
from rich.text import Text

console = Console()

def image_to_color_ascii(image_path, width=80):
    """
    图片 → 真彩色字符画（终端直接显示彩色照片！）
    
    与灰度版本的关键区别：
    - 灰度版：img.convert("L") → 丢掉颜色 → 只映射亮度到字符
    - 彩色版：img.convert("RGB") → 保留(r,g,b)三元组 → Rich的rgb()直接渲染
    
    这就是"美"的本质——不是创造颜色，是忠实还原每一个像素本来的颜色。
    
    参数：
    - image_path: 图片路径
    - width: 输出宽度（字符数）。建议80~120，太大会导致终端渲染缓慢
    """
    # 保持 "RGB" 三通道模式——每个像素保留完整的颜色信息
    # （如果原图有透明通道alpha，convert("RGB")会丢弃它）
    img = Image.open(image_path).convert("RGB")

    # 计算高度（与灰度版本相同的算法——补偿终端字符2:1的高宽比）
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)

    # 高质量缩放
    img = img.resize((width, height), Image.LANCZOS)

    # Rich的Text对象——支持每个字符独立样式
    text = Text()
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))   # 返回(r, g, b)元组，每个0~255
            # 核心魔法：Rich的 rgb(r,g,b) 样式标记
            # "█" (U+2588) 是满格方块——没有任何空隙，最纯的颜色呈现
            # 每个"█"都带着自己独有的RGB颜色，拼在一起就还原了照片
            text.append("█", style=f"rgb({r},{g},{b})")
        text.append("\n")   # Rich的Text也支持换行

    return text

# ===== 使用示例 =====
# console.print() 将 Rich 的 Text 对象渲染到终端
# 终端必须支持真彩色（Windows Terminal / iTerm2 / 几乎所有现代终端都支持）
console.print(image_to_color_ascii("your_photo.jpg", width=100))
# 提示：如果照片颜色偏暗或偏白，可以先在PIL中调整亮度/对比度再处理
```

> **性能说明：** 宽度100的图片约有数千个字符，每个带独立RGB样式——Rich首次渲染可能需要1~3秒，属于正常。如果渲染太慢，缩小 width 参数即可。

> **审美建议：** 录制时建议准备一张颜色丰富（有蓝天绿草或霓虹灯）的照片——颜色越多，冲击力越强。黑白/单色照片效果不明显。

**作业：** 用自己的照片生成彩色字符画，截图发到评论区/动态——**这是本系列第一个"转发级"作业**。

---

---

## Demo 3：词云生成器（第6~8集）

### 技术理论重述：jieba + wordcloud——语言理解 + 视觉表达

词云生成器实际上是一个**翻译管道**，把"语言的温度"翻译成"视觉的重量"：

```
文本（人类的表达）
    │
    ▼  jieba 分词——"理解"这句话在说什么
词汇列表（每个词的"身份"被识别：名词/动词/形容词...）
    │
    ▼  wordcloud 生成——按词频决定"视觉权重"
词云图（字大的=说得多的=在意的）
```

**jieba 不是"切割字符串"，而是"理解语言"：**
- 精确模式：最准确的分词，像认真听别人说话
- 全模式：把可能的词都列出来，像头脑风暴
- 搜索引擎模式：在精确基础上再切长词，像做笔记时划重点
- 词性标注：识别"名词/动词/形容词"——这对词云很关键，因为**名词最能代表一段话的主题**
- TF-IDF提取：自动找出"这段话最重要的词"——不需要人工判断

**wordcloud 不是"画图"，而是"表达"：**
- 词频高的词字大 = 这段文字里最"重"的词
- 遮罩（mask）决定形状 = 心形词云不是炫技，是"把对你的思念画成一颗心"
- 配色方案 = 同一段文字，暖色调表达温情，冷色调表达理性，赛博朋克表达酷

这个Demo的情感链条是：**你的聊天记录 → jieba理解你在说什么 → wordcloud把"在意"可视化**。技术全程隐形，观众只看到结果。

---

### 第6集：三分钟搞懂中文分词——jieba入门

**时长：** ~10分钟

**学习目标：** 中文分词原理、jieba三种模式、词性标注、关键词提取、自定义词典

**代码框架：**

```python
import jieba                        # 核心分词库
import jieba.posseg as pseg         # 词性标注子模块（posseg = Part-Of-Speech tagging + SEGmentation）
import jieba.analyse                # 关键词提取子模块（基于TF-IDF和TextRank算法）

# 演示文本——用自己的真实介绍更有代入感
text = """我是一名哔哩哔哩视频教学博主，现在粉丝量差不多在800+。
我采取的教学措施是视频教学加代码仓库，现阶段我已经讲完了Python基础、
Python进阶和Python标准库的内容。"""

# ===== 第1层：分词（拆开）=====
# jieba的核心机制：基于前缀词典的高效词图扫描，生成有向无环图（DAG），
# 然后用动态规划找出最大概率的切分路径
print("=" * 40)
print("三种分词模式对比：")
print("=" * 40)

# 精确模式：基于概率最大，每个字只属于一个词——最准确，适合词云和文本分析
# 返回可迭代的generator，用"/".join()拼成可视化字符串
print("精确模式:", "/".join(jieba.cut(text)))

# 全模式：把所有可能的词都扫出来——速度快但会有冗余，适合"看看有哪些可能的词"
# cut_all=True 触发全模式，同一个字可能出现在相邻的多个词中
print("全模式:", "/".join(jieba.cut(text, cut_all=True)))

# 搜索引擎模式：在精确模式基础上，对长词再次切分——适合搜索场景
# 例如"视频教学"会被切成"视频"和"教学"两个短词，提高搜索召回率
print("搜索模式:", "/".join(jieba.cut_for_search(text)))

# ===== 第2层：词性标注（理解）=====
# pseg.cut() 不仅分词，还标注每个词的词性（名词n、动词v、形容词a、副词d等）
# 词云一般用名词效果最好——名词最能代表一段话的"主题"
print("\n" + "=" * 40)
print("词性标注——筛选名词：")
print("=" * 40)
words = pseg.cut(text)   # 返回生成器，每个元素是(word, flag)对
# w.flag 是词性标记，如 'n'=名词, 'nr'=人名, 'ns'=地名, 'v'=动词
# startswith('n') 捕获所有名词子类（普通名词、人名、地名、机构名等）
nouns = [w.word for w in words if w.flag.startswith('n')]
print("名词:", nouns)
# 对比：如果不过滤词性，动词/副词/助词（如"是""的""在"）也会出现在词云里——不够"意"

# ===== 第3层：关键词提取（提炼）=====
# TF-IDF：词频×逆文档频率。一个词在当前文本中出现越频繁（TF高），
# 但在整个语料库中出现越少（IDF高），它的权重就越大
print("\n" + "=" * 40)
print("TF-IDF关键词提取：")
print("=" * 40)
# topK=5：提取前5个关键词；withWeight=True：同时返回权重值
keywords = jieba.analyse.extract_tags(text, topK=5, withWeight=True)
for word, weight in keywords:
    # weight 是归一化后的TF-IDF值，越高=在文本中越"关键"
    print(f"  {word}: {weight:.4f}（权重越高=越重要）")

# ===== 自定义词典（进阶） =====
# 默认词典不认识专有名词（如"北屿青禾"会被切成"北屿/青/禾"）
# 自定义词典让jieba正确识别这些词，格式：词 词频（可省略） 词性（可省略）
# jieba.load_userdict("my_dict.txt")
# my_dict.txt 内容示例：
#   北屿青禾 5 nz
#   小Demo 10 n
```

**作业：** 找一段不少于200字的中文文本（可以是自己写的日记/文章），用jieba分词并提取关键词。

---

### 第7集：一张图看懂全文——wordcloud初体验

**时长：** ~10分钟

**学习目标：** wordcloud基础用法、中文字体配置、停用词过滤、参数调优、matplotlib展示+保存

**代码框架：**

```python
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# ===== 1. 读取文本 =====
# 文本来源：聊天记录导出、文章、日记、小说章节……任何中文文本都可以
with open("sample.txt", "r", encoding="utf-8") as f:
    text = f.read()

# ===== 2. 分词：jieba把连续中文切成独立的词 =====
# wordcloud 需要空格分隔的词语列表，所以用 " ".join() 拼接
# 英文天然有空格分隔，中文必须先用jieba切分
words = " ".join(jieba.cut(text))

# ===== 3. 自动查找中文字体（跨平台关键！） =====
# 中文词云最大坑：不指定font_path→所有中文显示为方框□□□
# 下面自动检测三大平台的常见中文字体路径
font_path = None
candidates = [
    "C:/Windows/Fonts/msyh.ttc",                      # Windows 微软雅黑
    "C:/Windows/Fonts/simhei.ttf",                     # Windows 黑体
    "/System/Library/Fonts/PingFang.ttc",              # macOS 苹方
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",    # Linux 文泉驿
]
for f in candidates:
    if os.path.exists(f):
        font_path = f
        break

if font_path is None:
    raise FileNotFoundError(
        "未找到中文字体！请手动指定 font_path\n"
        "Windows用户: 下载微软雅黑或黑体\n"
        "macOS用户: PingFang.ttc 通常在 /System/Library/Fonts/"
    )

print(f"✅ 使用字体: {font_path}")

# ===== 4. 停用词：去掉噪音，留下"心意" =====
# 这些词出现频率极高但无实义——"的/了/是/我/你"
# 如果不过滤，词云里最大的字会是"的"——没有任何信息量
stopwords = set([
    "的", "了", "是", "我", "你", "他", "她", "它", "们", "这", "那",
    "也", "都", "就", "和", "在", "不", "有", "要", "会", "可以",
    "一个", "没有", "这个", "那个", "什么", "怎么",
])

# ===== 5. 生成词云 =====
# WordCloud 的核心参数解析：
wc = WordCloud(
    font_path=font_path,       # ⚠️ 中文必须指定，否则全是方框
    width=1920,                # 输出图片宽度（像素），越大越清晰
    height=1080,               # 输出图片高度（像素），16:9适合视频展示
    background_color="white",  # 背景色（white/black/'#FF5733'）
    max_words=200,             # 最多显示多少个词（太多会拥挤）
    stopwords=stopwords,       # 要过滤的无意义词集合
    max_font_size=120,         # 最大字号（最频繁的词的字号）
    min_font_size=8,           # 最小字号（小于此字号的词不显示）
    # 配色方案——选colormap=选情绪：
    # viridis: 科技感（绿→黄→紫），plasma: 温暖（蓝→粉→黄）
    # inferno: 激烈（黑→红→黄），magma: 暗黑（黑→紫→橙）
    # 更多选项见: matplotlib.org/stable/tutorials/colors/colormaps.html
    colormap="viridis",
    random_state=42,           # 固定随机种子→每次生成布局一致（方便视频展示）
)
# generate() 接收空格分隔的词语字符串，内部统计词频后自动布局
wc.generate(words)

# ===== 6. 显示（matplotlib） & 保存到文件 =====
# matplotlib 负责在屏幕上显示词云图
plt.figure(figsize=(16, 9), dpi=150)      # 16:9画布，150dpi高清
plt.imshow(wc, interpolation="bilinear")   # bilinear平滑渲染（让词云边缘柔和）
plt.axis("off")                             # 隐藏坐标轴
plt.tight_layout(pad=0)                    # 去除白边
plt.show()                                  # 弹出窗口显示

# 同时保存为PNG文件——方便在视频/动态中使用
wc.to_file("wordcloud.png")
print("✅ 词云已保存为 wordcloud.png")
```

> **关键认知：** `colormap` 决定了词云的情绪基调。`viridis`（绿→黄→紫）偏科技感，`plasma`（蓝→粉→黄）更温暖，`inferno`（黑→红→黄）更激烈。选配色就是选情绪。

**作业：** 把自己的微信聊天记录导出成txt，生成个人专属词云。

---

### 第8集：进阶——自定义形状、配色与实时数据词云

**时长：** ~10分钟

**学习目标：** 图片遮罩、ImageColorGenerator取色、自定义color_func、动态数据源

**代码框架：**

```python
import jieba
import numpy as np
import random
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

# ===== 1. 准备文本 =====
with open("sample.txt", "r", encoding="utf-8") as f:
    text = f.read()
words = " ".join(jieba.cut(text))

# ===== 2. 加载遮罩（决定词云的形状——形状=心意） =====
# 准备一张图片：白色（填充）区域是你想要的形状，黑色是背景
# 注意：白色区域=填词，黑色区域=不填词！（和直觉相反）
mask = np.array(Image.open("heart_mask.png"))

# ===== 3. 生成词云 =====
# ⚠️ 重要：mode="RGBA" 和 contour_width/contour_color 互斥！
# contour 内部用 RGB(3通道) 运算，RGBA(4通道) 会导致：
#   ValueError: operands could not be broadcast together with shapes (H,W,4) (H,W,3)
# 两种修复方式（二选一）：
#   方案A：保留透明背景 → 去掉 contour_width/contour_color
#   方案B：需要轮廓线   → 改用 mode="RGB" + background_color="white"
wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",
    mask=mask,
    background_color=None,          # 透明背景——方便叠加到其他设计上
    mode="RGBA",                    # RGBA模式支持透明通道（4通道）
    max_words=300,
    # contour_width=2,             # ❌ RGBA模式下不能用contour，会报错
    # contour_color='#FF6B6B',     # 如需轮廓线请改用 mode="RGB"
    random_state=42,
)
wc.generate(words)

# ===== 4. 配色方案（三选一） =====

# 方案A：从原图提取颜色——颜色浑然一体
image_colors = ImageColorGenerator(mask)
wc.recolor(color_func=image_colors)

# 方案B：赛博朋克配色——表达"酷"
# def cyberpunk_color(word, font_size, position, orientation,
#                     font_path=None, random_state=None, **kwargs):
#     """赛博朋克配色：品红/青色/黄色/粉红"""
#     colors = [
#         (255, 0, 255),    # 品红
#         (0, 255, 255),    # 青色
#         (255, 255, 0),    # 黄色
#         (255, 0, 128),    # 粉红
#     ]
#     rng = random.Random(hash(word))  # 同一个词始终同一种颜色
#     return rng.choice(colors)
#
# wc.recolor(color_func=cyberpunk_color)

# 方案C：莫兰迪配色——表达"温柔"
# def morandi_color(word, font_size, position, orientation,
#                   font_path=None, random_state=None, **kwargs):
#     """莫兰迪色系：低饱和度、灰度感"""
#     colors = [
#         (188, 170, 164),   # 灰粉
#         (163, 177, 138),   # 灰绿
#         (145, 160, 180),   # 灰蓝
#         (194, 178, 154),   # 灰棕
#     ]
#     rng = random.Random(hash(word))
#     return rng.choice(colors)
#
# wc.recolor(color_func=morandi_color)

# ===== 5. 展示 & 保存 =====
plt.figure(figsize=(16, 9), dpi=150)
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()

wc.to_file("shaped_wordcloud.png")
print("✅ 形状词云已保存！")
```

> **遮罩避坑1：** mask的规则是**白填黑不填**。要做心形词云，需要白色心形+黑色背景的图片——这和直觉相反，录制时务必强调。
>
> **遮罩避坑2：** `mode="RGBA"`（透明背景）和 `contour_width`/`contour_color`（轮廓线）**不能同时使用**。原因是 contour 内部生成的是 3 通道 RGB 数组，而 RGBA 模式产生 4 通道数组，做数组乘法时形状不匹配，会报 `ValueError: operands could not be broadcast together with shapes (H,W,4) (H,W,3)`。如需轮廓线效果，改用 `mode="RGB"` + `background_color="white"`。

> **颜色函数说明：** `color_func` 被wordcloud内部调用，每次画一个词时传入该词的信息。`**kwargs` 是预留参数位，保证兼容不同版本的wordcloud。`hash(word)` 确保同一个词每次显示同一种颜色——视觉一致性。

**作业：** 找一张自己喜欢的剪影图做遮罩，生成专属形状词云，发评论区展示——**这是本系列互动率最高的作业。**

---

---

## Demo 4：间谍情报术——把秘密藏进照片（第9~10集）

### 技术理论重述：LSB隐写术——信息藏在"看不见的地方"

像素的最低有效位（Least Significant Bit, LSB）隐藏着图片隐写的核心秘密。

一个像素的RGB三个通道各占8位（0-255）：

```
像素 = (R: 1010110[1], G: 0101101[0], B: 1110001[1])
                          ↑                    ↑          这些最低位
        值 = 173          值 = 90             值 = 225

如果我把最低位从1改成0：
        R: 1010110[0] = 172  （人眼完全无法分辨172和173的区别）
```

**人眼对亮度变化的最小可分辨差异约5~10个灰度级，而修改最低位只改变1个灰度级——完全不可见。**

这就意味着：**每个像素的RGB三个通道各可以"借用"1个bit来存秘密信息，而画面看起来完全不变。**

```
一张 1920×1080 的照片 = 2,073,600 像素
每个像素 3 通道 × 1 bit = 3 bits/像素
总容量 = 2,073,600 × 3 bits ÷ 8 = 777,600 字节 ≈ 760 KB
```

这张照片可以在肉眼完全看不出变化的情况下，藏下一整本书。

这就是"藏"的哲学：**信息不是被加密了，而是被"溶解"在画面里——它无处不在，但你完全看不见。**

技术链路：

```
秘密文字 ──→ UTF-8编码 ──→ 二进制流
                                │
照片 ──→ 逐像素取RGB ──→ 替换最低位 ──→ 视觉完全相同的"密文照片"
                                │
密文照片 ──→ 逐像素提取最低位 ──→ 拼接二进制 ──→ 解码 ──→ 秘密文字
```

核心规则：
1. **最低位替换**：`(pixel & 0xFE) | bit` —— 清空最后一位，填入秘密数据
2. **结束标记**：`11111111` 重复3次（24个1）—— 解码器知道何时停止
3. **必须用PNG**：JPEG是有损压缩，会破坏最低位数据

---

### 第9集：看不见的文字——LSB隐写术原理与实现

**时长：** ~10分钟

**学习目标：** LSB隐写原理→编码函数→解码函数→实际演示

**代码框架：**

```python
from PIL import Image
import os

# ===== 核心工具函数 =====

def text_to_binary(text):
    """
    文本 → 二进制字符串（UTF-8编码，支持中文和emoji）
    原理：每个字符先编码为1~4字节的UTF-8序列，再把每个字节展开为8个bit
    示例：'A' → b'A' = 0x41 = 01000001 → "01000001"
          '秘' → b'\xe7\xa7\x98' → "11100111 10100111 10011000"
    """
    # text.encode('utf-8')：字符串 → bytes（每个元素0~255）
    # format(b, '08b')：整数 → 8位二进制字符串（不足左侧补0）
    # ''.join(...)：把所有8位串拼接成一个长字符串
    return ''.join(format(b, '08b') for b in text.encode('utf-8'))

def binary_to_text(binary):
    """
    二进制字符串 → 文本（UTF-8解码）
    原理：每8个bit为一组 → 整数（字节值）→ bytes → UTF-8解码为字符串
    """
    # 先对齐到8位边界（丢弃末尾不足8位的碎片bit）
    binary = binary[:len(binary) - len(binary) % 8]
    byte_array = bytearray()
    # 每8位一组，转成整数后放入字节数组
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]          # 切片取8个字符，如 "01000001"
        if len(byte) == 8:            # 只有完整的8位才处理
            byte_array.append(int(byte, 2))  # int('01000001', 2) = 65 = 'A'
    # errors='replace'：遇到无效UTF-8字节时用�替代，避免程序崩溃
    return byte_array.decode('utf-8', errors='replace')

# ===== 编码：把秘密藏进图片 =====

def encode_image(image_path, secret_text, output_path):
    """
    将秘密文字隐藏到图片中（LSB隐写编码）
    
    算法流程：
    1. 打开图片，获取像素矩阵
    2. 秘密文字 → UTF-8二进制流 + 结束标记(24个1)
    3. 逐像素遍历，把每个像素R/G/B通道的最低位替换为1 bit秘密数据
    4. 保存为PNG（无损格式，不破坏最低位）
    
    核心操作：(pixel & 0xFE) | bit
    - 0xFE = 0b11111110，& 操作清空最低位
    - | bit 操作把最低位设置为秘密数据bit
    - 像素值最多变化±1（如173→172），人眼完全无法分辨
    """
    # 转换为RGB三通道（避免PNG的RGBA四通道引入alpha干扰）
    img = Image.open(image_path).convert("RGB")
    # load() 返回 PixelAccess 对象，支持 [x, y] 快速读写像素
    pixels = img.load()
    width, height = img.size

    # 文本→二进制，末尾拼接结束标记（24个连续的1）
    # 结束标记的作用：解码时遇到24个1就知道数据到此为止
    # 24个1 = 3个字节全是0xFF，在UTF-8中是非法的，所以不会出现在正常文本里
    binary = text_to_binary(secret_text) + '11111111' * 3

    # 检查容量——图片够不够大？
    max_bits = width * height * 3  # 每像素3个通道，每个通道借1bit = 3 bits/像素
    if len(binary) > max_bits:
        raise ValueError(
            f"秘密太长了！图片只能藏 {max_bits // 8} 个字符，"
            f"你的秘密有 {len(secret_text)} 个字符"
        )

    data_index = 0  # 指向当前要嵌入的bit位置
    for y in range(height):
        for x in range(width):
            if data_index >= len(binary):  # 所有数据嵌入完毕
                break
            r, g, b = pixels[x, y]

            # 依次替换R、G、B三个通道的最低有效位（LSB）
            # (channel & 0xFE)：将最低位清零（0xFE = 0b11111110）
            # | int(binary[data_index])：填入秘密数据的1个bit
            if data_index < len(binary):
                r = (r & 0xFE) | int(binary[data_index])
                data_index += 1
            if data_index < len(binary):
                g = (g & 0xFE) | int(binary[data_index])
                data_index += 1
            if data_index < len(binary):
                b = (b & 0xFE) | int(binary[data_index])
                data_index += 1

            pixels[x, y] = (r, g, b)  # 写回修改后的像素

    # ⚠️ 必须保存为PNG！JPEG的有损压缩会重新计算像素值，最低位数据全部丢失
    img.save(output_path, "PNG")
    return output_path

# ===== 解码：从图片提取秘密 =====

def decode_image(image_path):
    """
    从图片中提取隐藏的文字（LSB隐写解码）
    
    算法流程：
    1. 打开图片，获取像素矩阵
    2. 逐像素提取每个通道的最低位，拼接成二进制流
    3. 找到结束标记（24个连续的1），截断
    4. 二进制流 → UTF-8文本
    """
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    binary = ""
    # 按编码时的相同顺序（逐行，逐列，R→G→B）提取最低位
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # (channel & 1)：提取最低位——0x01 = 0b00000001
            # 只有最低位可能包含秘密数据，高位都是原始像素信息
            binary += str(r & 1)  # R通道最低位 → "0" 或 "1"
            binary += str(g & 1)  # G通道最低位
            binary += str(b & 1)  # B通道最低位

    # 在二进制流中查找结束标记（24个连续的1）
    end_marker = '11111111' * 3
    end_idx = binary.find(end_marker)
    if end_idx == -1:
        return "[未检测到隐藏信息]"  # 这张图可能没有藏数据

    # 截取从开头到结束标记之前的有效数据，转为文本
    return binary_to_text(binary[:end_idx])

# ===== 完整演示 =====
secret = """🔒 绝密情报：
目标将在今晚8点于老地方接头。
暗号：今天天气不错。
—— 特工007"""

# 编码：把秘密藏进图片
encode_image("original.png", secret, "secret.png")

# 解码：从图片中提取秘密
decoded = decode_image("secret.png")

print(f"隐藏的文字：\n{decoded}")
print(f"\n📁 原始文件大小: {os.path.getsize('original.png') / 1024:.1f} KB")
print(f"📁 密文文件大小: {os.path.getsize('secret.png') / 1024:.1f} KB")
# 注意：两张PNG文件大小可能略有不同（PNG压缩算法的微小差异），
# 但视觉上完全一致——这就是LSB隐写的魔力
print(f"💡 两张图在视觉上完全一致——但其中一张藏了 {len(secret)} 个字符的秘密")
```

> **关键规则：** 保存格式必须是PNG——JPEG的有损压缩会改变像素值，最低位数据全部丢失。录制时务必强调这一点。

**作业：** 用自己的照片隐藏一段文字，然后把"密文图片"发给朋友，看他能不能发现。

---

### 第10集：间谍升级——数据压缩、加密与批量处理

**时长：** ~10分钟

**学习目标：** zlib压缩→base64编码→XOR密码加密→批量处理→容量计算

**代码框架：**

```python
from PIL import Image
import zlib      # 内置压缩库，提供 DEFLATE 算法
import base64    # 将二进制数据编码为 ASCII 可打印字符
import os

class Steganographer:
    """
    图片隐写工具箱 —— 数字时代的隐形墨水
    
    四层处理管道（编码时正向，解码时反向）：
    原始文本 → zlib压缩 → base64编码 → XOR加密 → LSB嵌入(像素最低位)
    
    每一层的作用：
    - zlib压缩：减小数据量，让图片能藏更多字
    - base64编码：把压缩后的二进制转为ASCII字符串（避免null字节干扰）
    - XOR加密：可选的密码保护（演示级安全，不是真正的加密）
    - LSB嵌入：把最终数据"溶解"到像素的最低有效位中
    """

    # ===== 底层：二进制↔文本转换（与第9集相同） =====

    @staticmethod
    def text_to_binary(text):
        """文本 → 二进制字符串（UTF-8）"""
        return ''.join(format(b, '08b') for b in text.encode('utf-8'))

    @staticmethod
    def binary_to_text(binary):
        """二进制字符串 → 文本（UTF-8），自动处理8位对齐"""
        binary = binary[:len(binary) - len(binary) % 8]
        byte_array = bytearray()
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                byte_array.append(int(byte, 2))
        return byte_array.decode('utf-8', errors='replace')

    # ===== 中层：LSB像素级操作（核心引擎） =====

    @classmethod
    def _lsb_encode(cls, image_path, data, output_path):
        """
        LSB编码核心——把数据逐bit写入像素最低位
        data 应该是纯ASCII字符串（已经过base64处理），
        这样每个字符正好8bit，逐个bit嵌入RGB通道
        """
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        # 拼接二进制流 + 结束标记
        binary = cls.text_to_binary(data) + '11111111' * 3

        # 容量检查
        max_bits = width * height * 3
        if len(binary) > max_bits:
            raise ValueError(
                f"数据太长！图片容量 {max_bits // 8} 字符，数据需 {len(data)} 字符"
            )

        data_index = 0
        for y in range(height):
            for x in range(width):
                if data_index >= len(binary):
                    break
                r, g, b = pixels[x, y]
                # (channel & 0xFE)：清除最低位，(channel & 0xFE) | bit：填入数据
                if data_index < len(binary):
                    r = (r & 0xFE) | int(binary[data_index]); data_index += 1
                if data_index < len(binary):
                    g = (g & 0xFE) | int(binary[data_index]); data_index += 1
                if data_index < len(binary):
                    b = (b & 0xFE) | int(binary[data_index]); data_index += 1
                pixels[x, y] = (r, g, b)

        img.save(output_path, "PNG")  # ⚠️ 必须PNG，JPEG会破坏LSB数据
        return output_path

    @classmethod
    def _lsb_decode(cls, image_path):
        """
        LSB解码核心——从像素最低位逐bit提取数据
        返回提取的原始字符串（在 hide/reveal 中进一步处理）
        """
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        binary = ""
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # (channel & 1)：只取最低位——这正是我们写入的bit
                binary += f"{r & 1}{g & 1}{b & 1}"

        # 查找并截断到结束标记
        end_idx = binary.find('11111111' * 3)
        if end_idx == -1:
            raise ValueError("未检测到隐藏数据（可能这张图没有藏信息）")

        return cls.binary_to_text(binary[:end_idx])

    # ===== 上层：公开接口（压缩+编码+加密+嵌入 一条龙） =====

    @classmethod
    def hide(cls, image_path, text, output_path, password=None):
        """
        加密隐藏（编码管道）
        原始文本 → zlib压缩 → base64编码 → XOR加密(可选) → LSB嵌入
        """
        # 第1层：zlib压缩——压缩率通常30%~70%（中文压缩效果较好）
        # compress() 返回 bytes，内容包含二进制数据（可能有null字节）
        compressed = zlib.compress(text.encode('utf-8'))

        # 第2层：base64编码——把二进制bytes转成纯ASCII字符串
        # 因为LSB嵌入是按字符处理的，二进制null字节会截断字符串
        # base64确保所有字符都是可打印的ASCII（A-Za-z0-9+/=）
        # 代价：数据膨胀约33%（每3字节→4字符）
        encoded = base64.b64encode(compressed).decode('ascii')

        # 第3层：XOR简单加密（可选）
        # 密钥 = 密码所有字符ASCII码之和 mod 256（0~255的单字节密钥）
        # XOR的数学性质：a ^ k ^ k = a，所以加密和解密用同一个操作
        if password:
            key = sum(ord(c) for c in password) % 256
            encoded = ''.join(chr(ord(c) ^ key) for c in encoded)

        # 第4层：LSB嵌入
        return cls._lsb_encode(image_path, encoded, output_path)

    @classmethod
    def reveal(cls, image_path, password=None):
        """
        解密提取（解码管道——hide的反向操作）
        LSB提取 → XOR解密(可选) → base64解码 → zlib解压 → 原始文本
        """
        # 第4层反向：LSB提取
        encoded = cls._lsb_decode(image_path)

        # 第3层反向：XOR解密（与加密操作完全一致——XOR的自反性）
        if password:
            key = sum(ord(c) for c in password) % 256
            encoded = ''.join(chr(ord(c) ^ key) for c in encoded)

        # 第2层反向：base64解码（ASCII→原始压缩bytes）
        decoded = base64.b64decode(encoded)

        # 第1层反向：zlib解压（bytes→原始文本）
        return zlib.decompress(decoded).decode('utf-8')

    # ===== 工具方法 =====

    @staticmethod
    def capacity(image_path):
        """
        计算图片的理论最大隐藏容量（字符数，仅LSB层）
        
        注意：这是原始LSB容量，不包括压缩/加密/base64的影响。
        zlib压缩率 + base64膨胀(+33%) 的净效果取决于文本内容：
        - 英文文本：压缩率≈50%，base64后≈67%原始，所以有效容量≈理论×1.5
        - 中文文本：压缩率≈40%，base64后≈53%原始，有效容量≈理论×1.9
        - 已压缩数据（如zip）：压缩无效＋base64膨胀，有效容量≈理论×0.75
        
        粗略估算公式：有效字符 ≈ 理论容量 × 压缩率 / 1.33
        """
        img = Image.open(image_path)
        total_pixels = img.width * img.height
        bits = total_pixels * 3          # RGB各1bit = 3 bits/像素
        chars = bits // 8 - 24           # 减去24字节结束标记
        return chars


# ===== 完整演示 =====

# 1. 查看图片能藏多少字
print(f"📊 理论最大容量: {Steganographer.capacity('photo.png')} 个字符")
# 对于1920×1080的图片：2,073,600×3÷8-24 ≈ 777,576字符 ≈ 760KB
# 实际有效容量取决于文本内容和压缩效果

# 2. 加密隐藏——四层管道一气呵成
Steganographer.hide(
    "original.png",
    "特工007：今晚行动代号'月下独酌'。",
    "secret.png",
    password="007"   # 错误密码将解出乱码
)

# 3. 解密提取——四层管道反向运行
revealed = Steganographer.reveal("secret.png", password="007")
print(f"🔓 解密结果: {revealed}")

# 4. 批量打隐形水印（版权保护实战）
# 遍历文件夹，给所有PNG/BMP图片嵌入相同的版权信息
# 注意：跳过JPEG——有损压缩不兼容LSB隐写
# for f in os.listdir("photos/"):
#     if f.endswith(('.png', '.bmp')):
#         Steganographer.hide(
#             f"photos/{f}",
#             "Copyright © XianZS 2026",
#             f"watermarked/{f}"
#         )
```

> **技术注释：** XOR加密的密钥来自密码字符的ASCII码之和取模256——这是演示级加密，不适用于真正的安全场景。但"间谍工具"的氛围感已经拉满。

**作业：** 做一个"图片版权保护"脚本，给所有自己的照片打上隐形水印。

---

---

## Demo 5：二维码艺术生成器（第11~12集）

### 技术理论重述：qrcode——优雅藏在数学结构里

二维码不是一个随机的黑白方块矩阵——它是一个**经过精密数学设计的纠错编码系统**。三个"回"字形定位图案、定时图案、格式信息、数据区域、纠错码——每一个元素都有其数学上的必要性。

而"雅"的核心在于：**尊重数学结构，但改变它的表达方式。**

```
传统二维码                          优雅的二维码
    │                                   │
 黑白方块                            圆角模块（RoundedModuleDrawer）
 直角转角                            圆形模块（CircleModuleDrawer）
 纯黑纯白                            径向渐变（RadialGradiantColorMask）
 无Logo                              嵌入Logo（利用30%容错空间）
 有背景色                            透明背景（融入任何设计）
```

qrcode库的 `StyledPilImage` 体系就是一个"二维码美颜引擎"：

```
QRCode 核心（数学结构）
    │
    ├── ModuleDrawer（模块形状层）
    │   ├── SquareModuleDrawer     —— 传统方块
    │   ├── RoundedModuleDrawer    —— 圆角（像App图标）
    │   ├── CircleModuleDrawer     —— 圆形（像波尔卡圆点）
    │   └── VerticalBarsDrawer     —— 竖条（像条形码的艺术变体）
    │
    ├── ColorMask（色彩层）
    │   ├── SolidFillColorMask     —— 纯色填充
    │   └── RadialGradiantColorMask —— 径向渐变（从中心向边缘过渡）
    │
    └── Logo叠加（在中心位置，利用H级容错的30%冗余空间）
```

关键参数 `error_correction`：
- **L (7%)**：基本纠错，Logo空间小
- **M (15%)**：中等纠错
- **Q (25%)**：较高纠错
- **H (30%)**：最高纠错——Logo能占码面30%，依然能扫

优雅的二维码不是"装饰过的码"，而是**在不破坏可扫性的前提下，把数学结构变成视觉享受**。

---

### 第11集：三行代码出码——qrcode基础+实用场景

**时长：** ~10分钟

**学习目标：** 二维码原理科普、qrcode基础、参数调优、WiFi/VCard/日历等实用二维码

**代码框架：**

```python
import qrcode

# ===== 一行出码 =====
img = qrcode.make("https://space.bilibili.com/3690991649294439")
img.save("bilibili_basic.png")
print("✅ 基础二维码已生成！")

# ===== 精细控制——参数是"优雅"的起点 =====
qr = qrcode.QRCode(
    version=3,                                          # 尺寸：1~40，越大码越密
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30%容错——为Logo/样式留空间
    box_size=10,                                        # 每个模块的像素大小
    border=2,                                           # 边框宽度（最小2，保证可扫）
)
qr.add_data("https://github.com/XianZS/PythonLearning")
qr.make(fit=True)  # fit=True：自动选择最合适的version
img = qr.make_image(fill_color="#1a1a2e", back_color="#e94560")
img.save("github_styled.png")

# ===== 实用场景：WiFi二维码——扫了直接连网 =====
# 格式：WIFI:T:加密方式;S:WiFi名;P:密码;;
wifi_qr = qrcode.make("WIFI:T:WPA;S:MyWiFi;P:password123;;")
wifi_qr.save("wifi.png")
print("✅ WiFi二维码已生成！扫一扫即可连网")

# ===== 实用场景：VCard名片——扫了直接存联系人 =====
vcard = """BEGIN:VCARD
VERSION:3.0
FN:杨贤志森
TEL:13800138000
EMAIL:xianzhisen_yang@outlook.com
URL:https://space.bilibili.com/3690991649294439
END:VCARD"""
qrcode.make(vcard).save("vcard.png")
print("✅ 名片二维码已生成！扫一扫即可保存联系人")

print("\n📱 拿出手机扫一扫，试试效果~")
```

> **关键认知：** 二维码不是"图片"，是"被编码的数据"。WiFi码、VCard名片码不是不同格式的图片——它们只是把不同格式的**文本**编码进了二维码的数据区。

**作业：** 生成自己B站空间的二维码+WiFi二维码，发动态让粉丝试试。

---

### 第12集：让二维码变成海报——彩色、Logo、圆角、渐变全解锁

**时长：** ~10分钟

**学习目标：** StyledPilImage模块样式、嵌入Logo、渐变色、透明背景

**代码框架：**

```python
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    RoundedModuleDrawer,     # 圆角方块——像App图标
    CircleModuleDrawer,      # 圆形模块——像波尔卡圆点
    VerticalBarsDrawer,      # 竖条模块——现代设计感
)
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask,  # 径向渐变（注意：库中拼写是Gradiant不是Gradient）
    SolidFillColorMask,       # 纯色填充
)
from PIL import Image

# ===== 准备QR核心 =====
qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # H级容错=为设计留空间
    box_size=10,
    border=2,
)
qr.add_data("https://space.bilibili.com/3690991649294439")
qr.make(fit=True)

# ===== 风格1：圆角模块 + 柔和配色（优雅入门） =====
img1 = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(
        front_color=(255, 107, 107),    # 暖珊瑚色
        back_color=(255, 245, 245),     # 浅粉背景
    ),
)
img1.save("style_rounded.png")

# ===== 风格2：圆形模块 + 径向渐变（视觉焦点） =====
img2 = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=RadialGradiantColorMask(
        back_color=(255, 255, 255),     # 边缘白色
        center_color=(100, 50, 200),    # 中心紫色
        edge_color=(255, 100, 50),      # 边缘橙色过渡
    ),
)
img2.save("style_gradient.png")

# ===== 风格3：竖条模块 + 暗黑高级风 =====
img3 = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=VerticalBarsDrawer(),
    color_mask=SolidFillColorMask(
        front_color=(0, 255, 200),      # 青绿色
        back_color=(20, 20, 40),        # 深色背景
    ),
)
img3.save("style_dark.png")

# ===== 嵌入Logo——设计的点睛之笔 =====
logo = Image.open("logo.png")
# Logo尺寸 ≤ 码面尺寸的25%（H级容错的安全范围）
logo_size = min(img1.size) // 4
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

for img_path, style_name in [
    ("style_rounded.png", "final_rounded"),
    ("style_gradient.png", "final_gradient"),
    ("style_dark.png", "final_dark"),
]:
    img = Image.open(img_path).convert("RGBA")

    # 给Logo添加白色衬底（保证在任何配色上都清晰可见）
    padding = 10
    bg_size = logo_size + padding * 2
    bg = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 255))
    bg_pos = ((img.size[0] - bg_size) // 2, (img.size[1] - bg_size) // 2)
    img.paste(bg, bg_pos)

    # 粘贴Logo（用Logo自身的alpha通道做mask）
    logo_pos = ((img.size[0] - logo.size[0]) // 2,
                (img.size[1] - logo.size[1]) // 2)
    logo_mask = logo if logo.mode == 'RGBA' else None
    img.paste(logo, logo_pos, logo_mask)
    img.save(f"{style_name}_with_logo.png")

print("✅ 五种风格二维码+Logo已生成！")
print("📱 拿出手机扫一扫——优雅，但依然能扫")
```

> **避坑提示：** `RadialGradiantColorMask` 的类名拼写是库本身的typo（Gradiant而不是Gradient），不是代码写错了。Logo尺寸不超过码面的25%是安全实践——超过30%可能影响扫码成功率。

**作业：** 做一张自己专属风格的艺术二维码，发评论区展示。

---

---

## Demo 6：终端贪吃蛇（第13~14集）

### 技术理论重述：游戏循环——快乐的"心跳"

所有电子游戏都在运行同一个核心结构：

```
         ┌──────────────────────────────────┐
         │         游戏主循环                 │
         │                                  │
         │  ① 输入（玩家按了什么键？）         │
         │     ↓                            │
         │  ② 更新（蛇的位置变了、吃到食物了？）│
         │     ↓                            │
         │  ③ 渲染（把新画面画出来）           │
         │     ↓                            │
         │  ④ 等待（控制游戏速度——太快没法玩）  │
         │     ↓                            │
         │  回到①                            │
         └──────────────────────────────────┘
```

这个循环每秒运行约12~15次（取决于 `time.sleep(0.08)` 的速度），每一次循环都是一次"决策→行动→反馈"的完整周期。这就是"趣"的本质——**高频的、可预测的反馈循环产生心流。**

贪吃蛇的数据结构选择也充满趣味：

| 结构 | 操作 | 复杂度 | 说明 |
|------|------|--------|------|
| `deque`（双端队列） | 蛇头插入 | O(1) | `appendleft` 瞬间完成 |
| `deque` | 蛇尾删除 | O(1) | `pop` 瞬间完成 |
| `in snake` | 碰撞检测 | O(n) | 蛇身不长时很快 |

`collections.deque` 是蛇身的最佳数据结构——因为它"吃头去尾"的动作完美对应 `appendleft` + `pop` 两个O(1)操作。

"趣"的编程课和其他Demo不同——**写完代码的那一刻，学生不是看到结果，而是"开始玩"结果。** 这种参与感是独一无二的。

---

### 第13集：让它动起来——游戏循环+键盘控制+蛇的移动

**时长：** ~10分钟

**学习目标：** 游戏主循环、键盘监听、蛇的数据结构(deque)、碰撞检测、食物生成

**代码框架：**

```python
import os
import time
import random
from collections import deque   # 双端队列——蛇身的完美数据结构
import keyboard                  # Windows可直接用；Linux/macOS需root或改用 pynput

# ===== 游戏参数 =====
WIDTH, HEIGHT = 40, 20                         # 游戏地图大小（字符格）
# 蛇的初始状态：只有一个头，位于屏幕中央
snake = deque([(WIDTH // 2, HEIGHT // 2)])     # deque 存储 (x, y) 坐标序列
direction = (1, 0)                              # 初始方向：(1,0)=向右，(0,-1)=向上
# 第一个食物随机生成
food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
score = 0
game_over = False

# ===== 游戏三大组件 =====

def render():
    """
    渲染游戏画面——把游戏状态"画"在终端里
    
    渲染顺序：清屏 → 上边框 → 逐行绘制（蛇头/蛇身/食物/空地）→ 下边框 → 状态栏
    每一帧都完整重绘整个画面——这是经典游戏渲染模式
    """
    # 清屏：Windows用cls，Linux/macOS用clear
    os.system('cls' if os.name == 'nt' else 'clear')

    # 上边框：┌ + WIDTH个─ + ┐
    print('┌' + '─' * WIDTH + '┐')

    for y in range(HEIGHT):
        row = ""   # 逐字符拼接当前行（比逐个print快）
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                row += '█'       # 蛇头（实心方块，最显眼）
            elif (x, y) in snake:
                row += '▓'       # 蛇身（纹理方块，区别于头部）
            elif (x, y) == food:
                row += '🍎'       # 食物（emoji，视觉吸引力）
            else:
                row += ' '        # 空地
        print('│' + row + '│')   # 行边框 + 内容 + 行边框

    # 下边框 + 状态栏
    print('└' + '─' * WIDTH + '┘')
    print(f'得分: {score}  |  蛇长: {len(snake)}  |  方向: {direction}')

def get_direction():
    """
    获取键盘输入——返回新的方向向量
    
    防反向规则（核心游戏规则）：
    - 蛇不能原地掉头——例如向右移动时不能按a突然向左
    - 实现方式：如果当前纵向移动(dy≠0)，忽略w/s（纵向上）的输入
    - 同理，横向移动(dx≠0)时忽略a/d
    - 但如果按键方向与当前方向一致或垂直，则允许
    """
    global direction
    dx, dy = direction

    # W键：想向上(0,-1)。如果当前不是向下(dy≠1)，允许
    if keyboard.is_pressed('w') and dy != 1:
        return (0, -1)   # 上
    # S键：想向下(0,1)。如果当前不是向上(dy≠-1)，允许
    elif keyboard.is_pressed('s') and dy != -1:
        return (0, 1)    # 下
    # A键：想向左(-1,0)。如果当前不是向右(dx≠1)，允许
    elif keyboard.is_pressed('a') and dx != 1:
        return (-1, 0)   # 左
    # D键：想向右(1,0)。如果当前不是向左(dx≠-1)，允许
    elif keyboard.is_pressed('d') and dx != -1:
        return (1, 0)    # 右

    return direction  # 无有效按键，保持原方向

def update():
    """
    更新游戏状态——游戏循环的核心逻辑
    
    执行顺序：
    1. 读取方向（键盘输入）
    2. 计算新蛇头位置
    3. 碰撞检测（撞墙/撞自己 → 游戏结束）
    4. 移动蛇头（appendleft）
    5. 食物检测（吃到了 → 不去尾=增长；没吃到 → pop去掉蛇尾）
    """
    global direction, food, score, game_over

    # 读取玩家输入
    direction = get_direction()

    # 计算新蛇头位置
    head = snake[0]  # deque[0] 取最左侧=最前面=蛇头
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # 碰撞检测——撞墙
    if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        game_over = True
        return

    # 碰撞检测——撞自己
    # 注意：new_head in snake 检查新蛇头是否与当前蛇身任何位置重叠
    if new_head in snake:
        game_over = True
        return

    # 移动：蛇头前进一步
    snake.appendleft(new_head)  # deque.appendleft = O(1)，在左侧插入

    # 食物检测——"趣"的即时反馈核心
    if new_head == food:
        score += 10  # 吃到食物 +10分
        # 生成新食物——确保不刷在蛇身上
        # 理论上如果蛇填满了整个地图，while True会死循环（但实际游戏到不了这一步）
        while True:
            food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if food not in snake:
                break
        # 注意：吃到食物时不去尾 → 身体长度+1
    else:
        snake.pop()  # deque.pop = O(1)，去掉最右侧=最末尾=蛇尾

# ===== 主循环——游戏的心跳 =====
print("🐍 终端贪吃蛇 - WASD移动，按任意键开始...")
keyboard.read_key()  # 阻塞等待任意按键，让玩家准备好

# 游戏主循环：update（改变状态） → render（画出来） → sleep（控制速度）
while not game_over:
    update()
    render()
    # 控制游戏速度：sleep越短蛇越快。0.08秒 ≈ 12.5步/秒
    # 这是一个"趣"的平衡：太快来不及反应，太慢缺乏挑战
    time.sleep(0.08)

# 游戏结束
print(f"\n💀 游戏结束！最终得分: {score}")
print(f"🐍 蛇最终长度: {len(snake)}")
```

> **平台提示：** `keyboard` 库在Linux/macOS上需要root权限。如果不想用sudo，可以把 `keyboard` 换成 `pynput`（`pip install pynput`），用法略有不同但逻辑相同。Windows上无此问题。

**作业：** 调整 `time.sleep` 的值改变游戏速度（试试0.05/0.10/0.15），找到自己最舒服的难度。

---

### 第14集：终端游戏也能这么好看——Rich美化+加速+排行榜

**时长：** ~10分钟

**学习目标：** Rich渲染游戏画面、彩色蛇身渐变、加速机制、本地最高分存档、暂停功能

**完整代码：**

```python
import time
import json
import random
from collections import deque
import keyboard
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich import box

console = Console()

WIDTH, HEIGHT = 40, 20
SAVE_FILE = "snake_highscore.json"

class SnakeGame:
    """
    贪吃蛇游戏核心类
    
    架构说明（MVC简化版）：
    - 状态数据（snake/food/direction/score/speed）封装为实例属性
    - update() 负责状态变更——纯逻辑层，不涉及渲染
    - render() 负责生成 Rich Layout 对象——纯渲染层，不修改状态
    - 主循环在类外部，用 Rich Live 驱动 update + render 的交替执行
    
    数据结构选择：
    - deque：蛇身（双端队列），appendleft 吃头 O(1) + pop 去尾 O(1)
    - JSON：最高分持久化，跨游戏会话保存
    """

    def __init__(self):
        # --- 蛇的初始状态 ---
        # deque 双端队列：左侧=蛇头，右侧=蛇尾
        self.snake = deque([(WIDTH // 2, HEIGHT // 2)])   # 初始：一个头在屏幕中央
        self.direction = (1, 0)                            # 方向向量 (dx, dy)，初始向右

        # --- 食物 ---
        self.food = self._spawn_food()   # 第一个食物（确保不在蛇身上）

        # --- 分数系统 ---
        self.score = 0                                    # 当前局分数
        self.high_score = self._load_highscore()           # 历史最高分（跨会话持久化）

        # --- 游戏状态标志 ---
        self.game_over = False
        self.paused = False

        # --- 难度曲线 ---
        self.speed = 0.08                # 基础速度：每步0.08秒 ≈ 12.5步/秒
        self.food_eaten = 0              # 已吃食物计数（用于加速触发判断）

        # --- 输入防抖 ---
        self._prev_space = False         # 上一帧空格是否被按下（上升沿检测）

    def _spawn_food(self):
        """生成食物——确保不刷在蛇身上"""
        while True:
            pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def _load_highscore(self):
        """加载本地最高分——"趣"的竞争驱动"""
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f).get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def _save_highscore(self):
        """保存最高分——让"再来一局"有目标"""
        if self.score > self.high_score:
            self.high_score = self.score
            with open(SAVE_FILE, 'w') as f:
                json.dump({'high_score': self.high_score}, f)

    def update(self):
        """
        每帧调用一次，更新游戏状态（纯逻辑，不渲染任何内容）
        
        执行流程：
        1. 检查暂停切换（空格上升沿检测 → 翻转 paused 标志）
        2. 读取方向输入（WASD → 防反向判断 → 更新 direction）
        3. 计算新蛇头位置 + 碰撞检测（撞墙/撞自己 → game_over）
        4. 移动蛇头（appendleft）
        5. 食物检测（吃到 → 不去尾=增长+加速；没吃到 → pop去尾）
        
        返回值：无（直接修改 self 的状态属性）
        """
        if self.game_over:
            return

        # --- 暂停切换（空格上升沿检测机制）---
        # 问题：如果只用 keyboard.is_pressed('space')，一帧内检测多次，
        # 按住空格会疯狂切换暂停状态（闪烁）
        # 解决：用 _prev_space 记住上一帧的空格状态，
        # 只在"没按→按下"的瞬间（上升沿）才切换暂停
        space_pressed = keyboard.is_pressed('space')
        if space_pressed and not self._prev_space:
            self.paused = not self.paused      # 翻转暂停状态
        self._prev_space = space_pressed       # 记住这一帧，供下一帧比较

        if self.paused:
            return  # 暂停时不更新任何游戏状态（蛇/食物/方向全部冻结）

        # --- 方向控制（防反向 + 优先级 W > S > A > D）---
        dx, dy = self.direction
        # 防反向原理：例如当前向上(0,-1)，dy=-1
        # 按S键条件 dy!=-1 → -1!=-1 → False → 忽略（防止向下掉头）
        if keyboard.is_pressed('w') and dy != 1:
            self.direction = (0, -1)    # 上
        elif keyboard.is_pressed('s') and dy != -1:
            self.direction = (0, 1)     # 下
        elif keyboard.is_pressed('a') and dx != 1:
            self.direction = (-1, 0)    # 左
        elif keyboard.is_pressed('d') and dx != -1:
            self.direction = (1, 0)     # 右

        # --- 移动蛇头 ---
        head = self.snake[0]   # deque[0] = 最左侧 = 蛇头
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # --- 碰撞检测 ---
        # 撞墙：蛇头坐标超出地图边界
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            self.game_over = True
            self._save_highscore()   # 保存最高分（如果本局破了纪录）
            return
        # 撞自己：蛇头坐标与蛇身任何位置重叠
        if new_head in self.snake:
            self.game_over = True
            self._save_highscore()
            return

        # --- 前进：蛇头加入队列前端 ---
        self.snake.appendleft(new_head)  # O(1) 操作

        # --- 食物检测 ---
        if new_head == self.food:
            self.score += 10                    # 吃到一个 +10分
            self.food_eaten += 1               # 累计已吃数量
            self.food = self._spawn_food()      # 重新生成食物

            # 加速机制：每吃5个食物，速度提升10%
            # self.speed 是步间间隔（秒），越小=越快
            # max(0.02, ...) 限制最快速度为每0.02秒一步（50步/秒上限）
            # speed * 0.9：每次减少10%的间隔 → 约快11%
            if self.food_eaten % 5 == 0:
                self.speed = max(0.02, self.speed * 0.9)
        else:
            # 没吃到食物：去尾（保持蛇身长度不变）
            self.snake.pop()  # O(1) 操作，去掉最右侧=蛇尾

    def render(self):
        """
        生成 Rich Layout 渲染对象（每帧调用，由Live管理实际终端输出）
        
        布局结构：
        ┌──────────────────────────────────────┐
        │  Layout (root)                       │
        │  ├── game (ratio=3, 左侧3/4宽度)      │
        │  │   └── Panel: 逐字符拼接的游戏画面   │
        │  └── info (ratio=1, 右侧1/4宽度)      │
        │      └── Panel: Table 计分板          │
        └──────────────────────────────────────┘
        
        注意：此方法只生成 Rich 对象（纯数据结构），不产生终端 I/O。
        实际的终端输出由外部的 Live.update() 完成。
        """
        layout = Layout()
        layout.split_row(
            Layout(name="game", ratio=3),   # 左侧占3份宽度：游戏画面
            Layout(name="info", ratio=1),   # 右侧占1份宽度：信息面板
        )

        # ===== 左侧：游戏画面 =====
        game_str = ""
        for y in range(HEIGHT):
            row = ""
            for x in range(WIDTH):
                if (x, y) == self.snake[0]:
                    row += "[bold red]█[/bold red]"      # 蛇头：红色
                elif (x, y) in self.snake:
                    # 蛇身渐变：紧邻红色蛇头的第一节是绿色(0,200,0)，
                    # 越靠近尾部越偏金黄(255,100,0)，形成红→绿→金的渐变
                    # index()返回该坐标在蛇身中的位置（0=蛇头，1=第一节身体...）
                    idx = list(self.snake).index((x, y))
                    # ratio：0.0=紧邻头部的第一节身体，1.0=蛇尾
                    ratio = idx / max(len(self.snake) - 1, 1)
                    # R通道从头到尾递增（0→255）：头部附近偏绿，尾部偏红/橙
                    r = int(255 * ratio)
                    # G通道从头到尾递减（200→100）：头部附近更绿，尾部绿色减弱
                    g = 200 - int(100 * ratio)
                    # B=0固定，所以颜色在 绿(0,200,0) → 金橙(255,100,0) 之间渐变
                    row += f"[rgb({r},{g},0)]█[/rgb({r},{g},0)]"
                elif (x, y) == self.food:
                    row += "🍎"
                else:
                    row += " "
            game_str += row + "\n"

        layout["game"].update(
            Panel(game_str, title="[bold]🐍 贪吃蛇[/bold]", border_style="green")
        )

        # --- 信息面板 ---
        info = Table(box=box.SIMPLE, show_header=False, expand=True)
        info.add_column("", style="cyan", width=10)
        info.add_column("", style="bold yellow")
        info.add_row("🏆 最高分", str(self.high_score))
        info.add_row("📊 当前分", str(self.score))
        info.add_row("🐍 蛇长", str(len(self.snake)))
        info.add_row("⚡ 速度", f"{self.speed:.3f}s")
        info.add_row("🍎 已吃", str(self.food_eaten))

        # 状态行
        if self.paused:
            info.add_row("⏸️  状态", "[bold yellow]暂停中[/bold yellow]")
        elif self.game_over:
            info.add_row("💀 状态", "[bold red]游戏结束[/bold red]")
        else:
            info.add_row("▶️  状态", "[bold green]运行中[/bold green]")

        layout["info"].update(
            Panel(info, title="[bold]📋 状态[/bold]", border_style="blue")
        )

        return layout

# ===== 启动游戏 =====
game = SnakeGame()
console.clear()
console.print("[bold cyan]🐍 终端贪吃蛇 v2.0[/bold cyan]")
console.print("WASD移动 | 空格暂停 | Esc退出")
console.print(f"🏆 历史最高分: {game.high_score}")
console.print("\n按任意键开始...")
keyboard.read_key()   # 阻塞等待玩家按下任意键——给玩家准备时间

# ===== 主循环：Rich Live 驱动 =====
# Live 上下文管理器自动处理清屏、隐藏光标、增量刷新
# screen=True：全屏模式（自动隐藏滚动条和光标）
# refresh_per_second=15：每秒最多刷新终端15次（40×20画面绰绰有余）
with Live(game.render(), refresh_per_second=15, screen=True) as live:
    last_update = 0   # 上次调用 update() 的时间戳
    while True:
        try:
            now = time.time()
            # 时间差控制更新频率：
            # 只有经过 >= game.speed 秒才调用一次 update()
            # speed 越小 → update 越频繁 → 蛇移动越快
            # 但 render() 和 live.update() 每帧都执行（保持画面流畅）
            if now - last_update >= game.speed:
                game.update()          # 更新游戏逻辑（改变蛇位置等）
                last_update = now      # 重置计时器

            # render() 生成 Rich 对象，live.update() 将它推送到终端
            # Live 内部会做 diff——只有变化的部分才重新渲染到终端
            live.update(game.render())

            # Esc 键：退出游戏
            if keyboard.is_pressed('esc'):
                break

            # 游戏结束：停留2秒，让玩家看清死亡位置和最终分数
            if game.game_over:
                time.sleep(2)
                break

        except KeyboardInterrupt:   # Ctrl+C：优雅退出
            break

# ===== 结算画面 =====
console.print(
    f"\n[bold yellow]🎮 游戏结束！得分: {game.score}  "
    f"最高分: {game.high_score}[/bold yellow]"
)
# 破纪录提示：用 >= 包含平记录的情况（与历史最高持平也展示）
if game.score >= game.high_score:
    console.print("[bold gold]🏆 新纪录！[/bold gold]")
```

> **改进说明：** 暂停功能使用了**防抖机制**——按下和松开空格才算一次完整操作，避免单次按键被多帧重复检测。吃食物后速度逐渐加快（每5个+10%），增加"低开高走"的挑战曲线。

**作业：** 给贪吃蛇增加一个"障碍物"模式——地图中间随机生成墙壁，增加难度。
