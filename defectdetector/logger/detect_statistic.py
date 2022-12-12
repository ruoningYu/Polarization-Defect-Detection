import time
import os
import json

from typing import Dict
from logging import Handler, LogRecord


class DetectStatistic:

    STATISTIC_INFO = dict()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DetectStatistic, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 root: str = None
                 ):
        if not root:
            root = os.path.dirname(os.path.abspath(__file__))
        self.current_data = time.strftime("%Y-%m-%d", time.localtime())
        log_path = os.path.join(root, 'log', self.current_data)

        if not os.path.exists(log_path):
            open(log_path, "w")
        self._log_file = open(log_path, 'a+')

    def add(self, log: Dict):

        self._log_file.writelines(log + "\n")

    def filter(self, log: Dict):
        """
        此处将缺陷按照类型放入STATISTIC_INFO中进行记录
        """
        defect_type = log['type']
        prod_info = dict(
            prod_id=log['prod_id'],
            located=list(

            )
        )
        if defect_type not in self.STATISTIC_INFO.keys():
            self.STATISTIC_INFO.setdefault(defect_type, {
                'num': 0, 'prod_info': [
                    {'prod_id': log['prod_id']}
                ]
            })

    def stop(self):
        self._log_file.close()
