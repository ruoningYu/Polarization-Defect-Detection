

class RecordBuffer:
    """
    此函数用于记录系统的操作信息及系统报错
    """

    _buffer = []

    def __init__(self,
                 max_length: int = 10000
                 ):

        self.max_length = max_length

    def add(self,
            log: str):
        if len(self._buffer) < self.max_length:
            self._buffer.append(log)
        else:
            self._buffer.pop()
            self._buffer.append(log)

    def formatter(self):
        pass
