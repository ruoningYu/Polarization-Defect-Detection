import logging

from defectdetector.logger.logger import BaseLogHandler


def test_view_log_handler():
    log = logging.getLogger("test")

    log_handler = BaseLogHandler()

    log.setLevel(logging.INFO)
    log.addHandler(log_handler)

    for i in range(500):
        log.warning(f"test log info {i}")

