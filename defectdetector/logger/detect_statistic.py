import time
import os
import inspect


class DetectStatistic:

    def __init__(self,
                 root: str = None
                 ):
        if not root:
            root = os.path.dirname(os.path.abspath(__file__))
        self.current_data = time.strftime("%Y-%m-%d", time.localtime())
        log_path = os.path.join(root, 'log',  self.current_data)

        if not os.path.exists(log_path):
            open(log_path, "w")
        self._log_file = open(log_path, 'a+')

    def add(self, log: str):
        self._log_file.writelines(log + "\n")

    def stop(self):
        self._log_file.close()

