"""
实战案例
功能：实现多线程图片下载器，利用threading提升网络I/O效率，结合queue来管理任务，利用lock保证打印安全。
"""

import threading
import requests
import os
from queue import Queue

image_urls = [
    "https://fastly.picsum.photos/id/0/5000/3333.jpg?hmac=_j6ghY5fCfSD6tvtcV74zXivkJSPIfR9B8w34XeQmvU",
    "https://fastly.picsum.photos/id/7/4728/3168.jpg?hmac=c5B5tfYFM9blHHMhuu4UKmhnbZoJqrzNOP9xjkV4w3o",
    "https://fastly.picsum.photos/id/12/2500/1667.jpg?hmac=Pe3284luVre9ZqNzv1jMFpLihFI6lwq7TPgMSsNXw2w",
    "https://fastly.picsum.photos/id/17/2500/1667.jpg?hmac=HD-JrnNUZjFiP2UZQvWcKrgLoC_pc_ouUSWv8kHsJJY",
    "https://fastly.picsum.photos/id/29/4000/2670.jpg?hmac=rCbRAl24FzrSzwlR5tL-Aqzyu5tX_PA95VJtnUXegGU",
    "https://fastly.picsum.photos/id/24/4855/1803.jpg?hmac=ICVhP1pUXDLXaTkgwDJinSUS59UWalMxf4SOIWb9Ui4",
]
# 设置下载线程数
thread_count = 3
# 保存文件位置
save_dir = "download_images"
os.makedirs(save_dir, exist_ok=True)

# --- 初始化 ---
# 任务队列
url_queue = Queue()
for url in image_urls:
    url_queue.put(url)
# 设置锁：避免多线程时，出现打印混乱的情况
print_lock = threading.Lock()


# --- 下载任务 ---
def download_worker(thread_name):
    while not url_queue.empty():
        url = url_queue.get()
        try:
            with print_lock:
                print(f"[{thread_name}] 开始下载 : [{url}]")
            res = requests.get(url, timeout=10)
            res.raise_for_status()  # 检查请求是否成功
            # 保存图片
            filename = f"image_{hash(url) % 10000}.jpg"
            save_path = os.path.join(save_dir, filename)
            with open(save_path, mode="wb") as f:
                f.write(res.content)
            # 打印下载完成
            with print_lock:
                print(f"[{thread_name}] 下载完成: {filename}")
        except Exception as e:
            with print_lock:
                print(f"[{thread_name}] 下载失败: {url}-{str(e)}")
        finally:
            url_queue.task_done()


# 启动线程
print(f"启动 {thread_count} 个下载线程，一共 {len(image_urls)} 张图片")
threads = list()
for i in range(thread_count):
    t = threading.Thread(target=download_worker, args=(f"线程-{i + 1}",))
    threads.append(t)
    t.start()

url_queue.join()
print("\n所有图片下载完成")
