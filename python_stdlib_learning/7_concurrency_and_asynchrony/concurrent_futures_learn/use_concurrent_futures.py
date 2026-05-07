"""
实战案例
批量图片下载和灰度处理
"""

import concurrent.futures
import requests
import os
import time
from PIL import Image

IMAGE_URLS = [
    "https://picsum.photos/200/300?random=1",
    "https://picsum.photos/200/300?random=2",
    "https://picsum.photos/200/300?random=3",
    "https://picsum.photos/200/300?random=4",
]

DOWNLOAD_DIR = "download_images"
GRAYSCALE_DIR = "grayscale_dir"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(GRAYSCALE_DIR, exist_ok=True)


# 多线程下载：IO密集型任务，线程比较适合
def download_image(url):
    """下载单张图片，返回保存路径"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_name = f"image_{hash(url) % 10000}.jpg"
        save_path = os.path.join(DOWNLOAD_DIR, file_name)
        with open(save_path, mode="wb") as f:
            f.write(response.content)
        print(f"{file_name}图片下载完成")
        return save_path
    except Exception as e:
        print(f"下载失败:{url};\n{e}")
        return None


# 多进程转为灰度图：CPU密集型任务，进程比较适合
def to_grayscale(image_path):
    if not image_path:
        return None
    try:
        with Image.open(image_path) as img:
            gray_img = img.convert("L")
            file_name = os.path.basename(image_path)
            save_path = os.path.join(GRAYSCALE_DIR, f"gray_{file_name}")
            gray_img.save(save_path)
            print(f"{file_name}图片灰度处理完成")
            return save_path
    except Exception as e:
        print(f"灰度处理失败:{e}")
        return None


if __name__ == "__main__":
    start_time = time.time()
    # 多线程下载
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        download_paths = list(executor.map(download_image, IMAGE_URLS))
    spend_time_use_thread = time.time() - start_time
    print(f"多线程下载消耗时间为:{spend_time_use_thread:.2f}秒")
    # 多进程转为灰度图
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        gray_paths = list(executor.map(to_grayscale, download_paths))
    spend_time_use_Process = time.time() - start_time
    print(f"多进程转灰度消耗时间为:{spend_time_use_Process}")
