import PySpin
import logging

from PySide6.QtCore import Slot, Signal, QObject
from PySide6.QtGui import QImage

from .enumration import Enumeration
from .pipeline import Pipeline

from defectdetector.logger import BaseLogHandler
from defectdetector.transforms import Transforms
from defectdetector.detector import YoloxDetector


class Buffer:
    """Used to save images obtained from the camera
    """
    data_list = []

    def push(self, image):
        """Push the image in the buffer

        Args:
            image (ndarray):  Image to be pushed
        """
        if len(self.data_list) != 0:
            self.data_list.pop()
        self.data_list.append(image)

    def pop(self):
        """Pop the image in the buffer

        Returns:
            image (ndarray): Image to be popped
        """
        return self.data_list.pop()


class Controller(QObject):
    """Main control component of detector.

    include:
        system (PySpin.System):
            Retrieve singleton reference to system object
            Everything originates with the system object. It is important to notice
            that it has a singleton implementation, so it is impossible to have
            multiple system objects at the same time. Users can only get a smart
            pointer (SystemPtr) to the system instance.

        Camera (detector.camera.Camera):
            Class used to represent the camera itself.

        Pipeline (detector.pipeline.Pipeline):
            Manager of image processing or defect detection methods.

        Detector (detector.detector.Detector):
            Inspection components to detect defects in target objects.

        Logger (detector.logger.Logger):
            Log manager for recording operational and detection information
    """
    update_frame = Signal(QImage)

    def __init__(self):
        super(Controller, self).__init__()

        self.system = PySpin.System.GetInstance()
        self.device_enum = Enumeration()
        self.current_cam = None
        self.buffer = Buffer()

        self.log = logging.getLogger("test")
        self.log.setLevel(logging.INFO)
        self.log.addHandler(BaseLogHandler())

        self.pipeline = Pipeline(self.log, Transforms.METHOD)
        self.pipeline.add(YoloxDetector)

    def get_interface_model(self):
        """Scan the serial port on the host

        Returns:
            interface_model (Dict): serial port on the host
        """
        return self.device_enum.get_interface_info(self.system)

    @Slot()
    def select_camera(self, current):
        """Select the camera to be used and assign it to self.current_cam

        Args:
            current :Selected camera.

        """
        self.current_cam = self.device_enum.create_camera_instance(current.data())

    def get_cam(self):
        """Returns an instance of the current camera

        Returns:
            current_cam (PySpin.Camera): instance of the current camera.
        """
        return self.current_cam if self.current_cam else None

    def grab_next_image_by_trigger(self):
        """Get the next image by trigger

        Returns:
            img (ndarray): The next image from camera
        """
        pass

    def get_frame(self):
        """Acquire the processed image and push it to the buffer
        """
        frame = self.grab_next_image_by_trigger()
        res = self.pipeline.run(frame)
        self.buffer.push(res)

    def stop(self):
        """Stop acquiring images and turn off the camera
        """
        pass
