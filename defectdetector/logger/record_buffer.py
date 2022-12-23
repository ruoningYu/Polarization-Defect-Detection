

from typing import Dict
from defectdetector.utils import singleton
from PySide6.QtCore import Slot, Signal, QObject


MAX_LENGTH = 10000


@singleton
class RecordBuffer(QObject):
    """This function is used to record system operation information and system error.
    """
    record_signal = Signal(dict)
    buffer = []

    def add(self, log: str):
        if len(self.buffer) < MAX_LENGTH:
            self.buffer.append(log)
            self.emit_record(log)
        else:
            self.buffer.pop()
            self.buffer.append(log)
            self.emit_record(log)

    def buffer_info(self):
        return self.buffer

    def emit_record(self, log):
        self.record_signal.emit(log)

    def __len__(self):
        return len(self.buffer)
