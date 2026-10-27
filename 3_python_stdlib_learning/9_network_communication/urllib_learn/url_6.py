import urllib.request
import os


# 进阶-6：下载文件与进度显示
def download_file(url, save_path):
    """
    下载文件并且显示进度条
    """
    response = urllib.request.urlopen(url)
    # 获取文件的大小
    file_size = int(response.headers.get("Content-Length"), 0)
    print(f"[file_size]:{file_size}B")
    # 分块下载
    download_size = 0
    block_size = 1024 * 1024
    with open(save_path, "wb") as f:
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            download_size += len(buffer)
            f.write(buffer)
            # 计算并显示进度
            progress = (download_size / file_size) * 100 if file_size > 0 else 0
            print(
                f"\r[下载进度]:{download_size / 1024 / 1024:.2f}MB / {file_size / 1024 / 1024:.2f}MB ({progress:.2f}%)",
                end="",
            )
        print("下载完成\n")


url = "https://docs.python.org/zh-cn/3/archives/python-3.14-docs-html.zip"
save_path = "download_python_docs.zip"
download_file(url, save_path)
