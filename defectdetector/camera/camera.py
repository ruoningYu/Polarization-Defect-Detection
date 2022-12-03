import PySpin
import numpy as np

from PySide6.QtCore import Slot
from defectdetector.controller import Controller
from .nodemap import get_whole_nodemap


class TriggerType:
    SOFTWARE = 1
    HARDWARE = 2


CHOSEN_TRIGGER = TriggerType.SOFTWARE


class Camera(Controller):
    """
    Camera 中应当包含的
    属性：
        相机参数
    方法：
        获取图像
        设置图像格式
        其他参数设置
    """

    def __init__(self):
        super(Camera, self).__init__()

    def get_node_map(self):
        return get_whole_nodemap(self.current_cam)

    def init_camera(self):
        """
        初始化相机
        Returns
        -------

        """

        try:
            self.nodemap = self.current_cam.GetNodeMap()

            self.set_pixel_format()
            self.set_buffer()
            self.configure_trigger()
            node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
            if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
                print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
                return False

            node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
            if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                    node_acquisition_mode_continuous):
                print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
                return False

            acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
            node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
            self.current_cam.BeginAcquisition()

        except PySpin.SpinnakerException as ex:
            print("相加初始化失败！", ex)

    def configure_trigger(self):

        result = True

        try:
            # Ensure trigger mode off
            # The trigger must be disabled in order to configure whether the source
            # is software or hardware.
            node_trigger_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerMode'))
            if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
                print('Unable to disable trigger mode (node retrieval). Aborting...')
                return False

            node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
            if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
                print('Unable to disable trigger mode (enum entry retrieval). Aborting...')
                return False

            node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())

            print('Trigger mode disabled...')

            # Set TriggerSelector to FrameStart
            # For this example, the trigger selector should be set to frame start.
            # This is the default for most cameras.
            node_trigger_selector = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerSelector'))
            if not PySpin.IsAvailable(node_trigger_selector) or not PySpin.IsWritable(node_trigger_selector):
                print('Unable to get trigger selector (node retrieval). Aborting...')
                return False

            node_trigger_selector_framestart = node_trigger_selector.GetEntryByName('FrameStart')
            if not PySpin.IsAvailable(node_trigger_selector_framestart) or not PySpin.IsReadable(
                    node_trigger_selector_framestart):
                print('Unable to set trigger selector (enum entry retrieval). Aborting...')
                return False
            node_trigger_selector.SetIntValue(node_trigger_selector_framestart.GetValue())

            print('Trigger selector set to frame start...')

            # Select trigger source
            # The trigger source must be set to hardware or software while trigger
            # mode is off.
            node_trigger_source = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerSource'))
            if not PySpin.IsAvailable(node_trigger_source) or not PySpin.IsWritable(node_trigger_source):
                print('Unable to get trigger source (node retrieval). Aborting...')
                return False

            if CHOSEN_TRIGGER == TriggerType.SOFTWARE:
                node_trigger_source_software = node_trigger_source.GetEntryByName('Software')
                if not PySpin.IsAvailable(node_trigger_source_software) or not PySpin.IsReadable(
                        node_trigger_source_software):
                    print('Unable to set trigger source (enum entry retrieval). Aborting...')
                    return False
                node_trigger_source.SetIntValue(node_trigger_source_software.GetValue())
                print('Trigger source set to software...')

            elif CHOSEN_TRIGGER == TriggerType.HARDWARE:
                node_trigger_source_hardware = node_trigger_source.GetEntryByName('Line0')
                if not PySpin.IsAvailable(node_trigger_source_hardware) or not PySpin.IsReadable(
                        node_trigger_source_hardware):
                    print('Unable to set trigger source (enum entry retrieval). Aborting...')
                    return False
                node_trigger_source.SetIntValue(node_trigger_source_hardware.GetValue())
                print('Trigger source set to hardware...')

            # Turn trigger mode on
            # Once the appropriate trigger source has been set, turn trigger mode
            # on in order to retrieve images using the trigger.
            node_trigger_mode_on = node_trigger_mode.GetEntryByName('On')
            if not PySpin.IsAvailable(node_trigger_mode_on) or not PySpin.IsReadable(node_trigger_mode_on):
                print('Unable to enable trigger mode (enum entry retrieval). Aborting...')
                return False

            node_trigger_mode.SetIntValue(node_trigger_mode_on.GetValue())
            print('Trigger mode turned back on...')

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return result

    def grab_next_image_by_trigger(self):

        try:
            # Use trigger to capture image
            # The software trigger only feigns being executed by the Enter key;
            # what might not be immediately apparent is that there is not a
            # continuous stream of images being captured; in other examples that
            # acquire images, the camera captures a continuous stream of images.
            # When an image is retrieved, it is plucked from the stream.

            if CHOSEN_TRIGGER == TriggerType.SOFTWARE:
                # Execute software trigger
                node_softwaretrigger_cmd = PySpin.CCommandPtr(self.nodemap.GetNode('TriggerSoftware'))
                if not PySpin.IsAvailable(node_softwaretrigger_cmd) or not PySpin.IsWritable(node_softwaretrigger_cmd):
                    print('Unable to execute trigger. Aborting...')
                    return False

                node_softwaretrigger_cmd.Execute()

            elif CHOSEN_TRIGGER == TriggerType.HARDWARE:
                print('Use the hardware to trigger image acquisition.')

            img = self.capture()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return img

    def capture(self):
        """
        这里应该判断一下触发形式：连续或者触发器模式
        Returns
        -------

        """

        frame = self.current_cam.GetNextImage(1000)
        if frame.IsIncomplete():
            raise print('Image incomplete with image status %d ...' % frame.GetImageStatus())
        else:
            _data = frame.GetData()
            _height = frame.GetHeight()
            _width = frame.GetWidth()
            _channels = frame.GetNumChannels()
            image = np.reshape(_data, (_height, _width, _channels))
        frame.Release()
        return image

    def stop(self):
        self.current_cam.EndAcquisition()
        self.reset_trigger()

    def set_pixel_format(self):
        node_pixel_format = PySpin.CEnumerationPtr(self.nodemap.GetNode('PixelFormat'))
        if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):

            # Retrieve the desired entry node from the enumeration node
            node_pixel_format_current = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('Polarized8'))
            if PySpin.IsAvailable(node_pixel_format_current) and PySpin.IsReadable(node_pixel_format_current):

                # Retrieve the integer value from the entry node
                pixel_format_current = node_pixel_format_current.GetValue()

                # Set integer as new value for enumeration node
                node_pixel_format.SetIntValue(pixel_format_current)

                print('当前像素格式设置为 %s...' % node_pixel_format.GetCurrentEntry().GetSymbolic())

            else:
                print('不支持当前格式！')

        else:
            print('像素格式不可用')

    def set_buffer(self):

        s_node_map = self.current_cam.GetTLStreamNodeMap()
        handling_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferHandlingMode'))
        if not PySpin.IsAvailable(handling_mode) or not PySpin.IsWritable(handling_mode):
            return False

        handling_mode_entry = PySpin.CEnumEntryPtr(handling_mode.GetCurrentEntry())
        if not PySpin.IsAvailable(handling_mode_entry) or not PySpin.IsReadable(handling_mode_entry):
            return False

        stream_buffer_count_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferCountMode'))
        if not PySpin.IsAvailable(stream_buffer_count_mode) or not PySpin.IsWritable(stream_buffer_count_mode):
            return False

        stream_buffer_count_mode_manual = PySpin.CEnumEntryPtr(stream_buffer_count_mode.GetEntryByName('Manual'))
        if not PySpin.IsAvailable(stream_buffer_count_mode_manual) or not PySpin.IsReadable(
                stream_buffer_count_mode_manual):
            return False

        stream_buffer_count_mode.SetIntValue(stream_buffer_count_mode_manual.GetValue())

        buffer_count = PySpin.CIntegerPtr(s_node_map.GetNode('StreamBufferCountManual'))
        if not PySpin.IsAvailable(buffer_count) or not PySpin.IsWritable(buffer_count):
            return False
        try:
            buffer_count.SetValue(10)
            handling_mode_entry = handling_mode.GetEntryByName('NewestFirst')
            handling_mode.SetIntValue(handling_mode_entry.GetValue())
            return True
        except:
            return False

    def reset_trigger(self):
        """
        This function returns the camera to a normal state by turning off trigger mode.

        :param nodemap: Transport layer device nodemap.
        :type nodemap: INodeMap
        :returns: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True
            node_trigger_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerMode'))
            if not PySpin.IsAvailable(node_trigger_mode) or not PySpin.IsReadable(node_trigger_mode):
                print('Unable to disable trigger mode (node retrieval). Aborting...')
                return False

            node_trigger_mode_off = node_trigger_mode.GetEntryByName('Off')
            if not PySpin.IsAvailable(node_trigger_mode_off) or not PySpin.IsReadable(node_trigger_mode_off):
                print('Unable to disable trigger mode (enum entry retrieval). Aborting...')
                return False

            node_trigger_mode.SetIntValue(node_trigger_mode_off.GetValue())

            print('Trigger mode disabled...')

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result