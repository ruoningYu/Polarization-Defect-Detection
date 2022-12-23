import os
import time

from typing import Dict
from defectdetector.utils import singleton


@singleton
class DetectStatistic:
    """Statistic the detection information.
    """

    STATISTIC_INFO = dict()

    def __init__(self,
                 root: str = None
                 ):
        if not root:
            root = os.path.dirname(os.path.abspath(__file__))
        self.current_data = time.strftime("%Y-%m-%d", time.localtime())

        log_path = os.path.join(root, 'log', self.current_data)

        # if not os.path.exists(log_path):
        #     open(log_path, "w")
        self._log_file = open(log_path, 'a+')

    def add(self, log: Dict):
        if not isinstance(log, Dict):
            return
        if 'type' in log.keys():
            self.record(log)
        self._log_file.writelines(log + "\n")

    def record(self, log: Dict):
        """Put the defects into STATISTIC_INFO according to the type.
        """
        defect_type = log['type']
        prod_info = dict(
            prod_id=log['prod_id'],
            located=list(
                log['location']
            )
        )
        if defect_type not in self.STATISTIC_INFO.keys():
            self.STATISTIC_INFO.setdefault(defect_type, {
                'num': 0, 'prod_info': [prod_info]
            })
        else:
            self.STATISTIC_INFO[defect_type]['num'] += 1
            self.STATISTIC_INFO[defect_type]['prod_info'].append(prod_info)

    def stop(self):
        self._log_file.close()
