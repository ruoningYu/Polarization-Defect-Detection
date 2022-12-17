import logging

from typing import Dict
from defectdetector.logger import BaseLogHandler
from defectdetector.logger import DetectStatistic


class Detector:

    def __init__(self):

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(BaseLogHandler())

        self.detect_statistic = DetectStatistic()

    def detect(self, frame_info: Dict):
        pass

    def __call__(self, frame_info: Dict):
        return self.detect(frame_info)
