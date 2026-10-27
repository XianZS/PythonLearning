"""
logging 标准库学习
"""

# 1、logging标准库的简单解读
from logging import log


def func_1():
    import logging

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.debug("调试信息：变量x的数值是10")
    logging.info("输出信息：变量x的数值是20")


# 2、日志级别：精准控制日志的输出
def func_2():
    import logging

    """
    debug:10，调试
    info:20，输出
    warning:30，警告
    error:40，报错
    critical:50，严重报错
    >>>
        WARNING:root:【warning】：应该是输出的
        ERROR:root:【error】：应该是输出的
        CRITICAL:root:【critical】：应该是输出的
    """
    logging.basicConfig(level=30)
    logging.debug("【debug】：应该是不输出的")
    logging.info("【info】：应该是不输出的")
    logging.warning("【warning】：应该是输出的")
    logging.error("【error】：应该是输出的")
    logging.critical("【critical】：应该是输出的")


# 3、handler：将日志发送到不同的位置
def func_3():
    import logging
    from logging.handlers import RotatingFileHandler

    """
    目的地：文件、控制台、命令行
    streamhandler：输出到控制台
    filehandler：输出到文件
    没有设置：输出到命令行之中
    """
    # 创建logging对象
    logger = logging.getLogger(__name__)
    # 设置日志级别
    logger.setLevel(logging.DEBUG)
    # 是否可以传递给父logger
    logger.propagate = False
    # === 将日志输出到控制台之中 ===
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fromatter = logging.Formatter("%s(levelname)s:%(message)s")
    console_handler.setFormatter(console_fromatter)
    logger.addHandler(console_handler)
    logging.debug("【debug】：调试信息")
    logging.info("【info】：输出信息")
    logging.error("【error】：报错信息")


# 4、日志输出格式
def func_4():
    """
    %(asctime)s：获取日志输出的时间
    %(levelname)s：获取日志输出的级别
    %(message)s：获取日志输出的内容
    %(module)s：获取日志输出的模块名
    %(lineno)d：获取日志输出的行号
    %(funcName)s：获取日志输出的函数名
    """
    import logging

    formatter = logging.Formatter(
        "[%(asctime)s] [%(module)s:%(lineno)d] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)
    # logger = logging.getLogger(__name__)
    # logger.addHandler(handler)
    # logger.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(module)s:%(lineno)d] %(levelname)s - %(message)s",
    )
    logging.info("这是一条带着格式的日志输出")


# 5、简单的实战案例
def func_5():
    """
    简易任务处理系统日志
    """
    import logging
    from logging.handlers import RotatingFileHandler
    import time
    import random

    def setup_task_logger():
        """
        配置任务专用的logger对象
        """
        logger = logging.getLogger("task_processor")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        # 设置控制台
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console_format = logging.Formatter("%(levelname)s: %(message)s")
        console.setFormatter(console_format)
        logger.addHandler(console)
        # 设置文件
        file = RotatingFileHandler(
            "task_system.log",
            maxBytes=2 * 1024 * 1024,  # 2MB
            backupCount=5,
            encoding="utf-8",
        )
        file.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
        )
        file.setFormatter(file_format)
        logger.addHandler(file)
        return logger


# 6、日志设置的三种格式
def func_6():
    def func_6_1():
        """
        字典配置
        """
        import logging.config

        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": "%(levelname)s - %(asctime)s - %(lineno)d"}
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "app.log",
                    "formatter": "standard",
                    "encoding": "utf-8",
                }
            },
            "root": {"level": "INFO", "handlers": ["file"]},
        }
        logging.config.dictConfig(log_config)
        logging.info("通过字典配置记录的日志")

    def func_6_2():
        import logging.config

        logging.config.fileConfig("./logging.conf")
        logging.info("通过文件配置记录的日志")

    # func_6_1()
    # func_6_2()


if __name__ == "__main__":
    # func_1()
    # func_2()
    # func_3()
    # func_4()
    func_6()
