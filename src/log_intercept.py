from logging import Handler, LogRecord, __file__
from sys import _getframe

from loguru import logger


class InterceptHandler(Handler):
    """Handler intercepting standard logs and passing them into loguru logger"""

    def emit(self, record: LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = _getframe(6), 6
        while frame and frame.f_code.co_filename == __file__:
            frame = frame.f_back
            depth += 1
        intercepting_logger = logger.opt(depth=depth, exception=record.exc_info)
        intercepting_logger.log(level, record.getMessage())
