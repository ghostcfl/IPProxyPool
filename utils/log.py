import sys
from loguru import logger as lg
from settings import STD_OUT_LOG_LEVER, FILE_LOG_LEVER
from os.path import dirname


def get_logger():
    LOG_CONFIG = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": "{time:YYYY-MM-DD HH:mm:ss} | ({level}){message}",
                "level": STD_OUT_LOG_LEVER,
            },
            {
                "sink": dirname(__file__) + "/log.log",
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
                "enqueue": True,
                "rotation": "500 MB",
                "level": FILE_LOG_LEVER,
                "encoding": "utf-8",
            },
        ]
    }
    lg.configure(**LOG_CONFIG)
    return lg


logger = get_logger()
