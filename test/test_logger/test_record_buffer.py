import logging

from defectdetector.logger.logger import BaseLogHandler
from defectdetector.logger.record_buffer import RecordBuffer


def test_view_log_handler():
    log = logging.getLogger("test")

    log_handler = BaseLogHandler()

    log.setLevel(logging.INFO)
    log.addHandler(log_handler)

    for i in range(50):
        log.warning(f"waring something ---- {i}")
        log.info(f'waring something ---- {i} - {i}')

    buffer_info = RecordBuffer()
    print(buffer_info.buffer_info())
