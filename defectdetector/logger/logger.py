import logging
import time

from .record_buffer import RecordBuffer
from .detect_statistic import DetectStatistic
from logging import Logger, LogRecord, Handler


"""
Log 整体分为两个部分：
    1、显示在前端界面中的检测信息
        将检测记录进行永久性保存，记录在文件中
    2、后端代码的操作信息
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