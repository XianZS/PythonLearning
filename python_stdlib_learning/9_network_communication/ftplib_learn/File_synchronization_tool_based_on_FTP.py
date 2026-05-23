# === 实战案例 ===
# 基于 FTP 的文件传输工具
# 我们将开发一个完整的FTP文件同步工具，它具备以下功能：
# 1. 连接到FTP服务器并自动重连
# 2. 同步本地目录到远程FTP服务器
# 3. 支持增量同步（只上传修改过的文件）
# 4. 支持断点续传大文件
# 5. 支持大文件传输优化
# 6. 详细的日志记录（同时输出到文件和控制台）
# 7. 完善的错误处理和重试机制
# 8. 支持多级目录同步
from ftplib import FTP, error_perm, error_temp
import os
import time
import hashlib
import logging
from datetime import datetime
import socket

# 日志系统配置
logging.basicConfig(
    # 日志级别
    level=logging.INFO,
    # 日志格式
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        # 文件处理器
        logging.FileHandler("ftp_sync.log", encoding="utf-8"),
        # 流处理器:将日志输出到控制台之中
        logging.StreamHandler(),
    ],
)
# 获取当前的日志记录器
logger = logging.getLogger(__name__)


# === FTP 文件同步器类 ===
class FTPFileSync:
    """
    实现本地目录到远程FTP服务器的单向同步
    核心特性:增量同步,断点续传,自动重试,多级目录支持,详细日志
    """

    def __init__(
        self,
        host,
        port=21,
        username="anonymous",
        password="",
        local_dir="./",
        remote_dir="/",
        block_size=262144,
        max_retries=3,
    ):
        # 保存FTP服务器的连接信息
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        # 处理本地目录路径,转换为绝对路径
        self.local_dir = os.path.abspath(local_dir)
        # 处理远程目录
        self.remote_dir = remote_dir.rstrip("/")
        # 传输和重试的配置
        self.block_size = block_size
        self.max_retries = max_retries
        # 初始化FTP连接对象
        self.ftp = None
        # 确保本地的目录存在
        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)
            logger.info(f"创建本地同步目录:{self.local_dir}")

    def connect(self):
        # 连接到FTP服务器,支持自动重试和指数退避
        for attempt in range(self.max_retries):
            try:
                # === 确保本地操作无误 ===
                # 创建FTP客户端实例对象
                self.ftp = FTP()
                self.ftp.connect(self.host, self.port, timeout=30)
                self.ftp.login(self.username, self.password)
                self.ftp.set_pasv(True)  # 被动启动方式
                logger.info(f"成功连接到FTP服务器:{self.host}:{self.port}")
                # === 确保远程操作无误 ===
                self._ensure_remote_dir(self.remote_dir)
                # ftp
                # 根目录 /
                # jom kom lom
                # /-
                # --kom
                # --jom
                # --lom
                # /lom/ /kom/ /jom/
                self.ftp.cwd(self.remote_dir)
                logger.info(f"已经成功切换到远程同步目录:{self.remote_dir}")
                # 连接成功
                return True
            except (error_temp, socket.error) as e:
                # 捕捉临时错误 (人话:捕捉具有偶然性的错误)
                # 1/3 2/3 3/3
                logger.info(
                    f"捕捉到临时错误,连接FTP服务器失败(尝试:{attempt + 1}/{self.max_retries}):{e}"
                )
                if self.ftp:
                    self.ftp.close()
                else:
                    pass
                # 指数退避算法
                time.sleep(2**attempt)
            except Exception as e:
                print(f"[Error]:{e}")
                logger.info(f"连接FTP服务器发生未知错误:{e}")
                if self.ftp:
                    self.ftp.close()
                return False
        logger.error("连接FTP服务器失败,已经达到最大重试次数")
        return False

    def disconnect(self):
        # 安全断开与FTP服务器的连接
        # 首先检查FTP对象是否存在 并且 socket套接字是否有效
        if self.ftp and self.ftp.sock:
            try:
                self.ftp.quit()
                logger.info("已经断开与FTP服务器的连接")
            except Exception as e:
                self.ftp.close()
                logger.error(f"强制关闭:{e}")
        else:
            pass
        self.ftp = None

    def _ensure_remote_dir(self, remote_path):
        # 确保远程目录存在,不存在的话,就需要递归创建
        # 不改变远程指针所指向的远程目录,在操作完成之后自动回退
        # p->/root/docs/
        # remote_path:/root/some/
        # p_temp=p
        # ...
        # p=p_temp
        original_dir = self.ftp.pwd()  # type: ignore
        try:
            # 拆分路径
            dirs = remote_path.strip("/").split("/")
            # 记录当前正在处理的工作目录
            current_dir = ""
            # 逐级检查并且创建目录
            for dir_name in dirs:
                if not dir_name:
                    continue
                # 不存在的情况,需要拼接路径
                current_dir += "/" + dir_name
                try:
                    # 尝试进入目录
                    self.ftp.cwd(current_dir)  # type: ignore
                except error_perm:
                    # 进入目录失败,意味着目录不存在,则需要创建这个目录
                    self.ftp.mkd(current_dir)  # type: ignore
                    logger.info(f"创建远程目录:{current_dir}")
                    # 创建成功之后进入到该目录之中
                    self.ftp.cwd(current_dir)  # type: ignore
        except Exception as e:
            logger.error(f"远程报错:{e}")
        finally:
            # 回退到之前的工作目录之中
            self.ftp.cwd(original_dir)  # type: ignore

    def _get_file_md5(self, file_path):
        # 计算文件的md5哈希值
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            # 分块读取,每次读取4096个字节
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    def _get_remote_file_list(self):
        # 获取远程ftp服务器之中的所有文件及其详细信息
        # 存储信息字典
        remote_files = {}

        def parse_dir_line(line):
            # 将FTP的list命令进行单行输出
            parts = line.split()
            if len(parts) < 9:
                return None
            # 提取权限字符串
            permissions = parts[0]
            # 提取文件的大小
            size = int(parts[4])
            # 提取文件的文件名
            filename = " ".join(parts[8:])
            # 跳过目录
            if permissions.startswith("d"):
                return None
            return filename, size

        # 执行list命令,将所有的输出行添加到list列表
        lines = []
        self.ftp.retrlines("LIST", lines.append)  # type: ignore
        for line in lines:
            result = parse_dir_line(line)
            if result:
                filename, size = result
                remote_files[filename] = {"size": size}
        # 返回远程FTP服务器文件信息字典
        return remote_files

    def _upload_file_with_resume(self, local_path, remote_filename):
        # 上传单个文件,支持断点上传
        # 获取本地文件的大小
        file_size = os.path.getsize(local_path)
        # 循环重试上传
        for attempt in range(self.max_retries):
            try:
                # 检查远程文件是否存在,并且获取其大小
                try:
                    remote_size = self.ftp.size(remote_filename)  # type: ignore
                except error_perm:
                    remote_size = 0
                if remote_size == 0:
                    logger.info(
                        f"开始上传文件:{remote_filename}({file_size / 1024 / 1024:.2f}MB)"
                    )
                    with open(local_path, "rb") as f:
                        # 以二进制形式上传文件,使用配置块的大小
                        self.ftp.storbinary(  # type: ignore
                            f"STOR {remote_filename}", f, blocksize=self.block_size
                        )  # type: ignore
                elif remote_size < file_size:  # type: ignore
                    # 远程文件存在,但是不完整
                    logger.info(
                        f"断点续传文件:{remote_filename}(已上传{remote_size / 1024 / 1024:.2f}MB / {file_size / 1024 / 1024:.2f}MB)"  # type: ignore
                    )  # type: ignore
                    with open(local_path, "rb") as f:
                        f.seek(remote_size)  # type: ignore
                        self.ftp.storbinary(  # type: ignore
                            f"STOR {remote_filename}",
                            f,
                            blocksize=self.block_size,
                            rest=remote_size,
                        )  # type: ignore
                else:
                    # 远程文件存在,并且远程文件完整
                    logger.debug(f"文件存在且完整:{remote_filename}")
                # 上传完成之后验证文件的大小
                uploaded_size = self.ftp.size(remote_filename)  # type: ignore
                if uploaded_size == file_size:
                    logger.info(f"文件上传成功:{remote_filename}")
                    return True
                else:
                    raise Exception(
                        f"文件大小不匹配:本地{file_size}字节,远程{uploaded_size}字节"
                    )
            except (error_temp, socket.error) as e:
                logger.error(
                    f"上传文件失败(尝试{attempt + 1}/{self.max_retries}):{remote_filename} - {e}"
                )
                self.disconnect()
                if not self.connect():
                    return False
                # 使用指数退避算法重试
                time.sleep(2**attempt)
            except Exception as e:
                logger.error(f"上传文件发生未知错误:{remote_filename} - {e}")
                return False
        logger.error(f"三次上传都失败,已经达到最大重试次数:{remote_filename}")
        return False

    def sync(self):
        # 执行完整的文件同步流程
        # 流程:
        #   > 连接服务器>>>获取远程文件列表>>>获取本地文件列表>>>增量同步
        # 返回:
        #   > 所有文件同步成功返回True,失败返回False
        logger.info("=" * 60)
        logger.info("开始执行FTP文件同步")
        logger.info(f"本地目录:{self.local_dir}")
        logger.info(f"远程目录:{self.remote_dir}")
        logger.info("=" * 60)
        if not self.connect():
            return False
        try:
            # 获取远程的所有文件列表
            remote_files = self._get_remote_file_list()
            logger.info(f"远程目录共有{len(remote_files)}个文件")
            # 获取远程文件和本地文件的映射关系
            local_files = []
            for root, dirs, files in os.walk(self.local_dir):
                for file in files:
                    local_path = os.path.join(root, file)
                    # 计算本地文件在FTP服务器之中的相对路径
                    rel_path = os.path.relpath(local_path, self.local_dir)
                    remote_path = rel_path.replace(os.path.sep, "/")
                    # 添加到本地文件列表
                    local_files.append((local_path, remote_path))
            logger.info(f"本地目录共有{len(local_files)}个文件")
            # 初始化统计计数器
            uploaded_count = 0  # 成功上传的文件数
            skipped_count = 0  # 跳过的文件数
            failed_count = 0  # 上传失败的文件数
            for local_path, remote_path in local_files:
                # 获取文件所对应的远程子目录
                remote_dir = os.path.dirname(remote_path)
                if remote_dir:
                    self._ensure_remote_dir(f"{self.remote_dir}/{remote_dir}")
                # 获取本地文件的大小
                file_size = os.path.getsize(local_path)
                # 增量同步判断:如果远程存在同名文件且大小相同,则任务未修改,就跳过该文件
                if remote_path in remote_files:
                    remote_size = remote_files[remote_path]["size"]
                    if remote_size == file_size:
                        logger.info(f"文件未变化,跳过:{remote_path}")
                        skipped_count += 1
                        continue
                # 文件还需要上传的逻辑
                if self._upload_file_with_resume(local_path, remote_path):
                    uploaded_count += 1
                else:
                    failed_count += 1
            # 打印同步完整信息
            logger.info("=" * 60)
            logger.info(f"上传文件:{uploaded_count}个文件")
            logger.info(f"跳过了:{skipped_count}个文件")
            logger.info(f"失败了:{failed_count}个文件")
            logger.info("=" * 60)
            return failed_count == 0
        except Exception as e:
            logger.error(f"同步过程之中发生严重错误:{e}", exc_info=True)
            return False
        finally:
            self.disconnect()


def main():
    # 演示FTP文件同步器的作用
    local_ip = socket.gethostbyname(socket.gethostname())
    # 设置FTP同步配置参数
    config = {
        "host": local_ip,
        "port": 2121,
        "username": "testuser",
        "password": "testpass",
        "local_dir": "./local_sync_files",
        "remote_dir": "/ftp_sync_demo",
        "block_size": 262144,
        "max_retries": 3,
    }
    # 确保本地同步目录存在
    local_dir = config["local_dir"]
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    else:
        pass
    # 创建测试文件
    logger.info("正在创建测试文件")
    # # 创建5个测试文件
    # for i in range(5):
    #     test_file = os.path.join(local_dir, f"document_{i + 1}.txt")
    #     with open(test_file, "w", encoding="utf-8") as f:
    #         f.write(f"这是文档{i + 1}\n")
    #         f.write(f"创建时间:{datetime.now()}\n")
    #         f.write("这是一个FTP同步测试的文本文件")
    #         f.write("增量测试")
    # # 大文件分块测试 10*1024*1024 B = 10MB
    # large_file = os.path.join(local_dir, "large_data.bin")
    # with open(large_file, "wb") as f:
    #     f.write(os.urandom(10 * 1024 * 1024))
    # logger.info("测试文件创建成功")
    # 创建FTP文件同步实例化对象
    sync_ftp_obj = FTPFileSync(**config)
    # 执行同步操作
    make_judge = sync_ftp_obj.sync()
    # 判断输出结果
    if make_judge:
        logger.info("FTP文件同步成功")
    else:
        logger.info("FTP文件同步失败")


if __name__ == "__main__":
    main()
