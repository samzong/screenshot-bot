import logging
import sys

loggers = {}

LOG_ENABLED = True  # 是否开启日志
LOG_TO_CONSOLE = True  # 是否输出到控制台
LOG_TO_FILE = True  # 是否输出到文件

LOG_PATH = 'app.log'  # 日志文件路径
LOG_LEVEL = 'INFO'  # 日志级别

# 日志输出格式
LOG_FORMAT = '%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s'


def get_logger(name=None):
    """
    get logger by name
    :param name: name of logger
    :return: logger
    """
    global loggers

    if not name: name = __name__

    if loggers.get(name):
        return loggers.get(name)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # 输出到控制台
    if LOG_ENABLED and LOG_TO_CONSOLE:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level=LOG_LEVEL)
        formatter = logging.Formatter(LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # 输出到文件
    if LOG_ENABLED and LOG_TO_FILE:
        file_handler = logging.FileHandler(LOG_PATH, encoding='utf-8')
        file_handler.setLevel(level=LOG_LEVEL)
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # 保存到全局 loggers
    loggers[name] = logger
    return logger
