import time
import PySpin
import threading
import cv2

from PySide6.QtCore import Slot, Signal, QObject, QThread
from PySide6.QtGui import QImage

from .enumration import Enumeration
from .pipeline import Pipeline
from defectdetector.transforms import Transforms
from defectdetector.detector import YoloxDetector


class Buffer:
    data_list = []

    def push(self, image):
        if len(self.data_list) != 0:
            self.data_list.pop()
        self.data_list.append(image)

    def pop(self):
        return self.data_list.pop()


class Controller(QObject):
    """
    用于控制相机和检测器
    """

    update_frame = Signal(QImage)

    def __init__(self):
        super(Controller, self).__init__()
        self.system = PySpin.System.GetInstance()
        self.device_enum = Enumeration()
        self.current_cam = None
        self.buffer = Buffer()
        self.pipeline = Pipeline(
            Transforms.METHOD
        )
        self.pipeline.add(YoloxDetector)


    def get_interface_model(self):
        """
        获取主机上的接口列表
        Returns
        -------

        """
        return self.device_enum.get_interface_model(self.system)

    @Slot()
    def select_camera(self, current):
        """

        Parameters
        ----------
        current (str): 当前被选中的相机

        Returns (dict): 当前相机的nodemap
        -------

        """
        self.current_cam = self.device_enum.create_camera_instance(current.data())

    def get_cam(self):
        """
        获取相机实例
        Returns
        -------

        """
        return self.current_cam if self.current_cam else None

    def grab_next_image_by_trigger(self):
        pass

    def get_frame(self):
        frame = self.grab_next_image_by_trigger()
        # self.buffer.push(frame)
        res = self.pipeline.run(frame)
        self.buffer.push(res)

    def stop(self):
        pass
