
from defectdetector.utils import singleton
from PySide6.QtCore import Slot

MAX_LENGTH = 10000


@singleton
class RecordBuffer:
    """
    此函数用于记录系统的操作信息及系统报错
    """

    def __init__(self):
        self.buffer = []

    def add(self, log: str):
        if len(self.buffer) < MAX_LENGTH:
            self.buffer.append(log)
        else:
            self.buffer.pop()
            self.buffer.append(log)

    def buffer_info(self):
        return self.buffer

    def __len__(self):
        return len(self.buffer)
