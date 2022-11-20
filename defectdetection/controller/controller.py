
import PySpin

from PySide6.QtCore import Slot

from .enumration import Enumeration
from .pipeline import Pipeline


class Controller:
    """
    用于控制相机和检测器
    """

    def __init__(self):
        self.system = PySpin.System.GetInstance()
        self.device_enum = Enumeration()
        self.current_cam = None
        self.pipeline = Pipeline()

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

    def capture_img(self):
        pass

    def run(self):
        frame = self.capture_img()
        self.pipeline.run(frame)