import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser
import csv
import time
from http.cookiejar import CookieJar


class BookHTMLParser(HTMLParser):
    """自定义HTML解析器，提取豆瓣读书书籍信息"""

    def __init__(self):
        super().__init__()
        self.books = []  # 存储所有书籍信息
        self.current_book = {}  # 存储当前正在解析的书籍
        self.in_subject_item = False  # 是否在书籍条目内
        self.in_title = False  # 是否在书名标签内
        self.in_pub = False  # 是否在出版信息标签内
        self.in_rating = False  # 是否在评分标签内
        self.in_rating_count = False  # 是否在评价人数标签内
        self.in_detail = False  # 是否在简介标签内

    def handle_starttag(self, tag, attrs):
        """处理开始标签"""
        attrs_dict = dict(attrs)

        # 进入书籍条目
        if tag == "li" and attrs_dict.get("class") == "subject-item":
            self.in_subject_item = True
            self.current_book = {}

        # 进入书名标签
        elif self.in_subject_item and tag == "a" and "title" in attrs_dict:
            self.in_title = True
            self.current_book["title"] = attrs_dict["title"]
            self.current_book["url"] = attrs_dict["href"]

        # 进入出版信息标签
        elif self.in_subject_item and tag == "div" and attrs_dict.get("class") == "pub":
            self.in_pub = True

        # 进入评分标签
        elif (
            self.in_subject_item
            and tag == "span"
            and attrs_dict.get("class") == "rating_nums"
        ):
            self.in_rating = True

        # 进入评价人数标签
        elif self.in_subject_item and tag == "span" and attrs_dict.get("class") == "pl":
            self.in_rating_count = True

        # 进入简介标签
        elif (
            self.in_subject_item and tag == "p" and attrs_dict.get("class") == "detail"
        ):
            self.in_detail = True

    def handle_data(self, data):
        """处理标签内的文本数据"""
        data = data.strip()
        if not data:
            return

        if self.in_pub:
            # 出版信息格式：作者 / 出版社 / 出版日期 / 价格
            pub_parts = [part.strip() for part in data.split("/")]
            self.current_book["author"] = (
                pub_parts[0] if len(pub_parts) >= 1 else "未知"
            )
            self.current_book["publisher"] = (
                pub_parts[-3] if len(pub_parts) >= 3 else "未知"
            )
            self.current_book["pub_date"] = (
                pub_parts[-2] if len(pub_parts) >= 2 else "未知"
            )
            self.current_book["price"] = (
                pub_parts[-1] if len(pub_parts) >= 1 else "未知"
            )

        elif self.in_rating:
            self.current_book["rating"] = data

        elif self.in_rating_count:
            # 提取评价人数中的数字
            import re

            count_match = re.search(r"(\d+)", data)
            self.current_book["rating_count"] = (
                count_match.group(1) if count_match else "0"
            )

        elif self.in_detail:
            self.current_book["summary"] = data

    def handle_endtag(self, tag):
        """处理结束标签"""
        if tag == "li" and self.in_subject_item:
            # 离开书籍条目，将当前书籍加入列表
            self.in_subject_item = False
            # 补充缺失字段
            self.current_book.setdefault("rating", "暂无评分")
            self.current_book.setdefault("rating_count", "0")
            self.current_book.setdefault("summary", "暂无简介")
            self.books.append(self.current_book.copy())

        elif tag == "a" and self.in_title:
            self.in_title = False
        elif tag == "div" and self.in_pub:
            self.in_pub = False
        elif tag == "span" and (self.in_rating or self.in_rating_count):
            self.in_rating = False
            self.in_rating_count = False
        elif tag == "p" and self.in_detail:
            self.in_detail = False


class DoubanBookCrawler:
    """豆瓣读书爬虫类"""

    def __init__(self):
        # 1. 初始化Cookie管理器，模拟浏览器会话
        self.cookie_jar = CookieJar()
        self.cookie_handler = urllib.request.HTTPCookieProcessor(self.cookie_jar)
        self.opener = urllib.request.build_opener(self.cookie_handler)

        # 2. 设置请求头，模拟真实浏览器（关键反爬措施）
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://book.douban.com/",
        }

        # 3. 初始化HTML解析器
        self.parser = BookHTMLParser()

    def get_page(self, url):
        """获取单个页面的HTML内容"""
        try:
            # 构造请求对象
            req = urllib.request.Request(url, headers=self.headers)
            # 发送请求，设置超时时间
            with self.opener.open(req, timeout=15) as response:
                # 处理gzip压缩的响应（豆瓣会返回压缩内容）
                if response.headers.get("Content-Encoding") == "gzip":
                    import gzip

                    html = gzip.decompress(response.read()).decode("utf-8")
                else:
                    html = response.read().decode("utf-8")
                return html

        except urllib.error.HTTPError as e:
            print(f"HTTP错误: 状态码 {e.code} - {e.reason}")
            if e.code == 403:
                print("⚠️  被豆瓣反爬机制拦截，请降低爬取频率或稍后再试")
            return None
        except urllib.error.URLError as e:
            print(f"URL错误: {e.reason}")
            return None
        except Exception as e:
            print(f"未知错误: {str(e)}")
            return None

    def crawl_by_tag(self, tag, max_pages=5):
        """
        根据标签爬取书籍
        :param tag: 书籍标签，如"编程"、"文学"、"历史"
        :param max_pages: 最大爬取页数（每页20条）
        :return: 所有爬取到的书籍列表
        """
        all_books = []
        base_url = f"https://book.douban.com/tag/{urllib.parse.quote(tag)}"

        print(f"开始爬取豆瓣读书【{tag}】标签下的书籍，最多爬取{max_pages}页...")

        for page in range(max_pages):
            # 构造分页URL（豆瓣每页20条，start参数从0开始）
            start = page * 20
            url = f"{base_url}?start={start}&type=T"

            print(f"\n正在爬取第{page + 1}页: {url}")

            # 获取页面内容
            html = self.get_page(url)
            if not html:
                print(f"第{page + 1}页爬取失败，跳过")
                continue

            # 解析HTML
            self.parser.books.clear()
            self.parser.feed(html)

            # 如果当前页没有书籍，说明已经爬完所有内容
            if not self.parser.books:
                print("没有更多书籍了，爬取结束")
                break

            # 收集当前页书籍
            all_books.extend(self.parser.books)
            print(f"第{page + 1}页爬取成功，获取{len(self.parser.books)}本书籍")

            # 关键反爬措施：随机延时2-4秒，避免请求过快被封IP
            time.sleep(2)

        print(f"\n爬取完成！共获取{len(all_books)}本书籍信息")
        return all_books

    def save_to_csv(self, books, filename):
        """将书籍信息保存到CSV文件"""
        if not books:
            print("没有数据可保存")
            return

        # 定义CSV表头
        fieldnames = [
            "书名",
            "作者",
            "出版社",
            "出版日期",
            "价格",
            "评分",
            "评价人数",
            "简介",
            "链接",
        ]

        try:
            with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for book in books:
                    writer.writerow(
                        {
                            "书名": book["title"],
                            "作者": book["author"],
                            "出版社": book["publisher"],
                            "出版日期": book["pub_date"],
                            "价格": book["price"],
                            "评分": book["rating"],
                            "评价人数": book["rating_count"],
                            "简介": book["summary"],
                            "链接": book["url"],
                        }
                    )

            print(f"数据已成功保存到 {filename}")
        except Exception as e:
            print(f"保存文件失败: {str(e)}")


if __name__ == "__main__":
    # 实例化爬虫
    crawler = DoubanBookCrawler()

    # 爬取"编程"标签下的书籍，最多爬取3页
    books = crawler.crawl_by_tag(tag="编程", max_pages=3)

    # 保存数据到CSV文件
    if books:
        crawler.save_to_csv(books, "豆瓣读书_编程类书籍.csv")
