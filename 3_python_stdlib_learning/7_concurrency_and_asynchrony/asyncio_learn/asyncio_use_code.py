"""
asyncio 异步编程实战
功能：实现高并发网页爬虫，批量获取网页信息内容
（这里获取的网页信息内容是标签，当然，也可以是其它东西）
"""

# 异步数据写入
import asyncio

# 异步网络请求
import aiohttp

# 解析网络代码 pip install beautifulsoup4
from bs4 import BeautifulSoup

# 格式标准库
from typing import List, Tuple

# 目标URL列表
URLS = [
    "https://www.python.org",
    "https://www.example.com",
    "https://httpbin.org/html",
    "https://stackoverflow.com",
    "https://github.com",
]


# 异步爬取函数
async def fetch_page_title(session: aiohttp.ClientSession, url: str) -> Tuple[str, str]:
    """异步获取单个网页的标题"""
    try:
        async with session.get(url, timeout=10) as response:  # type:ignore
            # 检查http状态码
            response.raise_for_status()
            # 异步读取html内容
            html_res = await response.text()
            # 解析标题
            soup_title = BeautifulSoup(html_res, "html.parser")
            title = (
                soup_title.title.string.strip()  # type:ignore
                if soup_title.title
                else "No title found"
            )
            return (url, title)
    except Exception as e:
        print(f"[Error]:{e}")
        return (url, f"Error: {str(e)}")


async def main(urls: List[str]):
    """主协程：并发爬取所有的URL网页"""
    print(f"Starting crawl of {len(urls)} URLs ...")
    # 创建异步http会话（复用连接池的形式）
    async with aiohttp.ClientSession() as session:
        # 创建所有爬取任务
        tasks = [fetch_page_title(session, url) for url in urls]
        # 通过gather并发执行所有的爬取任务
        results = await asyncio.gather(*tasks)
        # print(f"[results]:{results}")
        res_list = list(results)
        for cho in res_list:
            print(f"[{cho[0]}]: ({cho[1]})")


if __name__ == "__main__":
    asyncio.run(main(URLS))
