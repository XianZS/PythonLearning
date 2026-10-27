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
        console.print("\n[bold green]ヾ(•ω•`)o 监控结束，再见[/bold green]")
