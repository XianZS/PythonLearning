# rich 实现终端输出媲美网页
from re import L
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress,BarColumn,TextColumn
from rich import box
import time

console=Console()
# 设置基础配置
console.print("[bold cyan] rich 体验 [/bold cyan]")
console.print("[red]■[/red][yellow]■[/yellow]")

# 创建表格
table=Table(title="[bold]表格标题[/bold]",box=box.ROUNDED,border_style="cyan")
table.add_column("指标",style="yellow")
table.add_column("数值",style="bold green")
table.add_row("CPU","23.3%")
table.add_row("内存","8.2GB / 16 GB")

# 添加进度条
console.print("\n[bold]任务模拟进度[/bold]")
with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage}%")
        ) as progress:
    task=progress.add_task("[cyan]加载系统模块...",total=100)
    while not progress.finished:
        progress.update(task,advance=2)
        time.sleep(0.1)
# 如何处理排版，分栏
layout=Layout()
layout.split(Layout(name="top"),Layout(name="bottom"))
layout["top"].update(Panel("CPU + 内存信息",title="[bold]上部[/bold]"))
layout["bottom"].update(Panel("网络 + 磁盘信息",title="[bold]下部[/bold]"))
console.print("\n[bold]模拟动态刷新[/bold]")
# 通过Live模拟动态刷新
with Live(layout,refresh_per_second=4) as live:
    for i in range(8):
        layout["top"].update(
                Panel(f"CPU: {23+i*2}% ; 内存:{45+i-2}%",title="[bold]上部[/bold]")
                )
        time.sleep(1)
