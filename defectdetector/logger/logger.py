import logging
import time

from .record_buffer import RecordBuffer
from .detect_statistic import DetectStatistic

from logging import Logger, LogRecord, Handler, Formatter


"""
Log 整体分为两个部分：
    1、显示在前端界面中的检测信息
        将检测记录进行永久性保存，记录在文件中
    2、后端代码的操作信息
        将操作信息进行短期保存，不在前端界面直接显示，但是可以调用显示
        
    从log中获取的信息统一转换为json格式
    然后由BaseLogHandler进行统一分发
    前端直接从相应的类中提取相应日志信息，不在经过日志记录类
    相应类均为单例，实时记录相应信息
        
"""

SAVE_ATTR = ["module", "msg"]


class DetectFormatter(Formatter):

    def __init__(self):
        super(DetectFormatter, self).__init__()

    def format(self, record: LogRecord) -> str:
        msg = self.translate(record)
        return self.time_format(msg)

    @staticmethod
    def translate(record: LogRecord):
        s = {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__ if attr_name in SAVE_ATTR
        }

        return s

    @staticmethod
    def time_format(msg):
        _time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        msg["tm"] = _time
        return msg


class BaseLogHandler(Handler):

    def __init__(self, name=""):
        super(BaseLogHandler, self).__init__()
        self.name = name

        self.det_formatter = DetectFormatter()
        self.setFormatter(self.det_formatter)

        self.record_buffer = RecordBuffer()
        self.detect_statistic = DetectStatistic()

    def emit(self, record: LogRecord) -> None:
        _log_info = self.format(record)
        for attr in record.__dict__:
            if attr == 'detector':
                self.detect_statistic.add(_log_info)
            else:
                self.record_buffer.add(_log_info)

        将操作信息进行短期保存，不在前短界面直接显示，但是可以读取
"""


class ViewLogHandler(Handler):

    def __new__(cls, *args, **kwargs):
        pass

    def __init__(self):
        super(ViewLogHandler, self).__init__()
        self.record_buffer = RecordBuffer()
        self.detect_statistic = DetectStatistic()

    def emit(self, record: LogRecord) -> None:
        value = self.format(record)
        self.record_buffer.add(value)
        self.detect_statistic.add(value)