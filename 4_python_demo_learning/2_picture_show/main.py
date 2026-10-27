# 终端渲染真彩色图片
import os
import time
from pathlib import Path
from PIL import Image
from rich.console import Console
from rich.text import Text

console = Console()

SUPPORTED_EXTEMNSIONS = {".jpg", ".png", "jpeg", ".bmp"}


def image_to_color_ascii(image_path, width=80):
    img = Image.open(image_path).convert("RGB")
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.5)
    img = img.resize((width, height), Image.LANCZOS)  # type:ignore
    text = Text()
    # 外层循环，纵向遍历
    for y in range(height):
        # 内层循环，横向遍历
        for x in range(width):
            r, g, b = img.getpixel((x, y))  # type:ignore
            text.append("■", style=f"rgb({r},{g},{b})")
        text.append("\n")
    return text


def get_image_files(folder_path="imgs"):
    folder = Path(folder_path)
    if not folder.exists():
        console.print(f"[red]错误：文件夹{folder_path}不存在[/red]")
        return []
    files = []
    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTEMNSIONS:
            files.append(file)
    files.sort(key=lambda f: f.name)
    return files


if __name__ == "__main__":
    IMG_FOLDER = "imgs"
    OUTPUT_WIDTH = 500
    PLAY_INTERVAL = 2
    image_files = get_image_files(IMG_FOLDER)
    if not image_files:
        console.print(
            f"[yellow]文件夹{IMG_FOLDER}之中没有找到任何可以渲染的图片[/yellow]"
        )
    else:
        console.print(
            f"[bold cyan]准备播放，一共{len(image_files)}张图片，每张停留{PLAY_INTERVAL}秒。[/bold cyan]"
        )
        console.print("[dim]输入ctrl+c即可停止程序[/dim]")
        input("按下 Enter 键开始播放")
        try:
            while True:
                for i, img_path in enumerate(image_files, 1):
                    console.clear()
                    console.print("[bold cyan]循环播放之中[/bold cyan]")
                    console.print(f"[bold green]{img_path.name}[/bold green]")
                    console.print(f"{'-' * 60}")
                    ascii_art = image_to_color_ascii(str(img_path), width=OUTPUT_WIDTH)
                    console.print(ascii_art)
                    time.sleep(PLAY_INTERVAL)
        except KeyboardInterrupt:
            console.clear()
            console.print("[bold green]已经退出自动播放[/bold green]")
