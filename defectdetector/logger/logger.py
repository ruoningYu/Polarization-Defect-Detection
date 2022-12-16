import time
from logging import LogRecord, Handler, Formatter
from typing import Dict

from .detect_statistic import DetectStatistic
from .record_buffer import RecordBuffer

"""
Log 整体分为两个部分：
    **
        检测信息不在经由log模块进行记录与统计，转为直接记录
    **
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

    def format(self, record: LogRecord) -> Dict:
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
    """
    所有的信息预处理在该类中完成：
        包括：时间、记录类型、所属模块、记录级别、记录关键词
    """

    def __init__(self, name=""):
        super(BaseLogHandler, self).__init__()
        self.name = name

        self.setFormatter(DetectFormatter())

        self.record_buffer = RecordBuffer()
        self.detect_statistic = DetectStatistic()

    def emit(self, record: LogRecord) -> None:
        _log_info = self.format(record)

        self.record_buffer.add(_log_info)
