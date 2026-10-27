# 导入系统基础模块，提供系统级交互能力
import os
# 导入时间模块，用于实现自动轮播的延时停留功能
import time
# 导入 pathlib 下的 Path 类，用于面向对象的路径处理，天然支持跨平台路径兼容
from pathlib import Path
# 导入 Pillow 库的 Image 类，负责图片的读取、格式转换、缩放等核心图像处理操作
from PIL import Image
# 导入 rich 库的 Console 类，用于终端彩色输出、清屏等控制台高级操作
from rich.console import Console
# 导入 rich 库的 Text 类，用于构建支持逐字符着色的富文本对象，是实现真彩色字符画的核心载体
from rich.text import Text

# 初始化全局控制台对象，后续所有终端输出、清屏操作均通过该对象完成
console = Console()

# ===== 支持的图片格式 =====
# 使用集合存储支持读取的图片后缀名，统一为小写格式
# 集合的查找效率高于列表，同时用于后续文件格式校验时不区分大小写
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"}


def image_to_color_ascii(image_path, width=80):
    """
    图片 → 真彩色字符画（终端直接显示彩色照片！）
    核心原理：保留每个像素的 RGB 三通道颜色信息，用实心方块字符作为显示载体
    与灰度字符画的本质区别：不丢弃颜色信息，直接通过终端颜色能力还原原图色彩

    参数：
    - image_path: 输入图片的文件路径（字符串或 Path 对象）
    - width: 输出字符画的宽度（单位：字符数），高度会根据原图比例自动计算

    返回值：
    - rich.text.Text 对象，包含完整的带 RGB 颜色样式的字符画内容
    """
    # 打开目标图片，并强制转换为 RGB 三通道模式
    # 确保无论原图是灰度、RGBA 还是其他模式，都能统一读取到 r,g,b 三色值
    img = Image.open(image_path).convert("RGB")

    # 计算原图的宽高比（高度 / 宽度），用于后续等比缩放，保证图片不变形
    aspect_ratio = img.height / img.width

    # 计算输出字符画的高度（单位：字符行数）
    # 乘以 0.5 是为了修正终端字符的物理高宽比：终端单个字符的高度约为宽度的 2 倍
    # 如果不做该修正，输出的画面会在纵向被拉长一倍，导致比例失真
    height = int(width * aspect_ratio * 0.5)

    # 使用 LANCZOS 高质量重采样算法将图片缩放到目标尺寸
    # 该算法在缩小图片时能更好地保留细节、减少锯齿，是高质量缩放的常用选择
    img = img.resize((width, height), Image.LANCZOS)

    # 初始化空的 Rich Text 对象，用于逐字符拼接带颜色样式的字符画
    text = Text()

    # 外层循环：逐行遍历像素（纵向遍历）
    for y in range(height):
        # 内层循环：逐列遍历像素（横向遍历）
        for x in range(width):
            # 获取当前坐标 (x, y) 像素的红、绿、蓝三通道值，取值范围均为 0-255
            r, g, b = img.getpixel((x, y))
            # 向 Text 对象追加一个实心方块字符，并设置该字符的 RGB 颜色样式
            # 用统一的方块字符作为载体，靠颜色差异还原图像，本质是在终端模拟像素点
            text.append("█", style=f"rgb({r},{g},{b})")
        # 一行像素处理完成后，追加换行符，实现分行显示，对应图片的一行像素
        text.append("\n")

    # 返回构建完成的彩色字符画富文本对象，交由控制台渲染
    return text


def get_image_files(folder_path="imgs"):
    """
    扫描指定文件夹，筛选出所有支持格式的图片文件，并按文件名排序
    保证每次程序运行时，图片的播放顺序一致且可预测

    参数：
    - folder_path: 待扫描的图片文件夹路径，默认值为当前目录下的 imgs 文件夹

    返回值：
    - list[Path]：符合格式要求的图片文件路径列表，按文件名升序排列
    """
    # 将输入的路径字符串转换为 Path 对象，方便后续进行路径相关操作
    folder = Path(folder_path)

    # 校验目标文件夹是否存在，不存在则输出红色错误提示，并返回空列表终止后续逻辑
    if not folder.exists():
        console.print(f"[red]错误：文件夹 '{folder_path}' 不存在[/red]")
        return []

    # 初始化空列表，用于存储筛选出的图片文件路径
    files = []

    # 遍历文件夹内的所有子项（文件、子文件夹）
    for file in folder.iterdir():
        # 筛选条件：必须是文件（排除子文件夹），且文件后缀（转小写后）在支持的格式集合中
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
            # 符合条件的文件加入结果列表
            files.append(file)

    # 按文件名对文件列表进行升序排序，确保每次运行的播放顺序一致
    files.sort(key=lambda f: f.name)

    # 返回筛选并排序后的图片文件列表
    return files


# ===== 主流程：自动循环渲染图片 =====
# 程序入口判断：仅当直接运行该脚本文件时，才执行以下主流程代码
# 若该文件被其他 Python 文件作为模块导入，则不执行主逻辑
if __name__ == "__main__":
    # 配置项：图片资源存放的文件夹路径
    IMG_FOLDER = "imgs"
    # 配置项：字符画输出的宽度（字符数），数值越大画面越精细，但对终端宽度要求越高
    OUTPUT_WIDTH = 500
    # 配置项：每张图片的停留播放时长，单位为秒，可根据播放节奏需求自由调整
    PLAY_INTERVAL = 2  

    # 调用扫描函数，获取目标文件夹内所有符合条件的图片文件列表
    image_files = get_image_files(IMG_FOLDER)

    # 判断：如果未找到任何图片文件，执行警告提示逻辑
    if not image_files:
        # 输出黄色警告文本，告知用户文件夹内未找到图片
        console.print(
            f"[yellow]警告：在 '{IMG_FOLDER}' 文件夹中没有找到图片文件[/yellow]"
        )
        # 输出当前程序支持的所有图片格式，方便用户排查
        console.print(f"支持的格式：{', '.join(SUPPORTED_EXTENSIONS)}")
    else:
        # 输出播放准备提示，显示图片总数量和单张停留时长
        console.print(
            f"[bold cyan]准备播放：共 {len(image_files)} 张图片，每张停留 {PLAY_INTERVAL} 秒[/bold cyan]"
        )
        # 输出灰色弱化提示，告知用户退出方式
        console.print("[dim]按 Ctrl+C 可随时退出播放[/dim]\n")
        # 阻塞等待用户按下回车键，确认后再开始自动播放，给用户预留准备时间
        input("按 Enter 开始自动循环播放...")

        # try-except 结构：用于捕获用户主动中断的信号，实现优雅退出
        try:
            # 外层无限循环，实现图片列表的循环轮播
            # 一轮播放完毕后会自动从头开始，持续循环直到用户主动终止
            while True:
                # 遍历所有图片文件，enumerate 同时获取播放序号（从 1 开始）和文件路径
                for i, img_path in enumerate(image_files, 1):
                    # 渲染新图片前先清空终端屏幕
                    # 保证终端界面上始终只显示当前一张图片，上一张内容被完全清除
                    console.clear()
                    
                    # 打印顶部状态栏，包含播放进度、单张停留时长、退出提示
                    console.print(
                        f"[bold cyan]循环播放中 [{i}/{len(image_files)}] | 单张停留 {PLAY_INTERVAL}s | 按 Ctrl+C 退出[/bold cyan]"
                    )
                    # 打印黄色分隔线，用于区分状态栏和图片内容，优化视觉层级
                    console.print(f"[bold yellow]{'─' * 60}[/bold yellow]")
                    # 打印当前正在播放的图片文件名
                    console.print(f"[bold green]{img_path.name}[/bold green]")
                    # 打印第二条黄色分隔线，闭合标题区域
                    console.print(f"[bold yellow]{'─' * 60}[/bold yellow]")
                    
                    # 调用核心转换函数，将当前图片生成真彩色字符画对象
                    ascii_art = image_to_color_ascii(str(img_path), width=OUTPUT_WIDTH)
                    # 在终端控制台渲染输出彩色字符画
                    console.print(ascii_art)
                    
                    # 程序暂停指定秒数，保持当前图片的显示状态
                    # 休眠结束后进入下一次循环，切换到下一张图片
                    time.sleep(PLAY_INTERVAL)
        except KeyboardInterrupt:
            # 捕获用户按下 Ctrl+C 触发的键盘中断异常
            # 避免程序直接抛出报错栈，改为友好的退出提示
            # 先清屏再输出退出信息，保持终端干净
            console.clear()
            console.print("[bold green]已退出自动播放[/bold green]")