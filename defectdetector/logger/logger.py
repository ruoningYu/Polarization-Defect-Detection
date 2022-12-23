import time
from logging import LogRecord, Handler, Formatter
from typing import Dict

from .detect_statistic import DetectStatistic
from .record_buffer import RecordBuffer

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

    def __init__(self, name=""):
        super(BaseLogHandler, self).__init__()
        self.name = name

        self.setFormatter(DetectFormatter())

        self.record_buffer = RecordBuffer()
        self.detect_statistic = DetectStatistic()

    def emit(self, record: LogRecord) -> None:
        _log_info = self.format(record)

        self.record_buffer.add(_log_info)
