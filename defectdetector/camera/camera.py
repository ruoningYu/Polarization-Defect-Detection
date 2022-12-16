from typing import Dict, Union, Sequence

import PySpin
import numpy as np

from defectdetector.controller import Controller
from defectdetector.utils import load_config, save_config
from .nodemap import get_whole_nodemap


class Camera(Controller):
    """Classes for configuring camera parameters and getting images.

    Args:
        config (dict): Configuration files for camera.
        save (bool): Whether to save the current configuration information as a file.
        trigger (int): Trigger method. default: 0.
    """

    TriggerType = ['SOFTWARE', 'HARDWARE']

    def __init__(self,
                 config: str,
                 save=False,
                 trigger: int = 0
                 ):
        super(Camera, self).__init__()

        self.Config = load_config(config)
        self.save = save
        self.camera_feature_config = self.Config['property']['Camera Feature']['Root']
        self.transport_layer_config = self.Config['property']['Transport Layer']['Root']
        self.stream_parameters = self.Config['property']['Stream Parameters']['Root']

        self.trigger_type = self.TriggerType[trigger]

    def setup_cap(self):
        """Initialize the camera before acquiring images.

        The default initialization process includes:
            - Init Camera instance of PySpin.
            - Get nodemap of current Camera instance.
            - Get whole nodemap dict of current Camera instance.
            - Setup pixel format.
            - Setup buffer.
            - Setup trigger.
            - Setup acquisition mode.
            - Begin acquisition。
        """
        self.current_cam.Init()
        self.nodemap = self.current_cam.GetNodeMap()
        self.get_node_map()
        self.set_pixel_format()
        self.set_buffer()
        self.set_trigger()
        self.set_acquisition()
        self.current_cam.BeginAcquisition()

    def get_node_map(self):
        """Get all node information of the camera.

        Returns:
            Dict: all node information of the camera.
        """
        node_map = get_whole_nodemap(self.current_cam)
        if self.save:
            save_config(node_map)

        return node_map

    def set_node(self,
                 node: Union[Dict, Sequence],
                 node_name: str,
                 symbolic: str = None):
        """Set the node value based on the node name.

        Args:
            node (Dict): Current node information.
            node_name (str): Name of current node.
            symbolic (str): The name of the target entry. default: None.

        Returns:
            Boolean: Whether the configuration was successful.
        """
        result = True
        if not symbolic:
            symbolic = node['entry_symbolic'] if 'entry_symbolic' in node.keys() else node['value']
        else:
            symbolic = symbolic

        try:
            node_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode(node_name))

            # *** NOTES ***
            # Readability/writability should be checked prior to interacting with
            # nodes. Readability and writability are ensured by checking the
            # access mode or by using the methods
            if not PySpin.IsAvailable(node_mode) or not PySpin.IsWritable(node_mode):
                print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
                return False

            node_entry = node_mode.GetEntryByName(symbolic)
            if not PySpin.IsAvailable(node_entry) or not PySpin.IsReadable(node_entry):
                print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
                return False

            node_value = node_entry.GetValue()
            node_mode.SetIntValue(node_value)
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return result

    def set_acquisition(self, acquisition_config: Dict = None):
        """Configure the acquisition.

        Args:
            acquisition_config (Dict): Configuration parameters for trigger. default: None.

        Returns:
            Boolean: Whether the configuration was successful.
        """
        if not acquisition_config:
            acquisition_config = self.camera_feature_config['Acquisition Control']['Acquisition Mode']

        result = self.set_node(acquisition_config, 'AcquisitionMode')
        return result

    def set_pixel_format(self, pixel_format_config: Dict = None) -> bool:
        """Configure the pixel format.

        Args:
            pixel_format_config (Dict): Configuration parameters for pixel_format. default: None.

        Returns:
            Boolean: Whether the configuration was successful
        """

        if not pixel_format_config:
            pixel_format_config = self.camera_feature_config['Image Format Control']

        result = self.set_node(pixel_format_config['Pixel Format'], 'PixelFormat', 'Polarized8')
        return result

    def set_buffer(self, buffer_config: Dict = None) -> bool:
        """Configure the buffer.

        Args:
            buffer_config (Dict): Configuration parameters for buffer. default: None.

        Returns:
            Boolean: Whether the configuration was successful.
        """

        if not buffer_config:
            buffer_config = self.stream_parameters['Buffer Handling Control']

        s_node_map = self.current_cam.GetTLStreamNodeMap()
        handling_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferHandlingMode'))
        if not PySpin.IsAvailable(handling_mode) or not PySpin.IsWritable(handling_mode):
            return False

        handling_mode_entry = PySpin.CEnumEntryPtr(handling_mode.GetCurrentEntry())
        if not PySpin.IsAvailable(handling_mode_entry) or not PySpin.IsReadable(handling_mode_entry):
            return False

        self.set_node(buffer_config['Stream Buffer Count Mode'], 'StreamBufferCountMode', 'Manual')

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

    def set_trigger(self, trigger_config: Dict = None):
        """This function configures the camera to use a trigger.
        First, trigger mode is set to off in order to select the trigger source. Once the
        trigger source has been selected, trigger mode is then enabled, which has the camera
        capture only a single image upon the execution of the trigger.

        Args:
            trigger_config (Dict): Configuration parameters for trigger. default: None.

        Returns:
            Boolean: Whether the configuration was successful.
        """

        if not trigger_config:
            trigger_config = self.camera_feature_config['Acquisition Control']
        try:
            trigger_mode = trigger_config['Trigger Mode']
            trigger_mode['entry_symbolic'] = 'Off'
            self.set_node(trigger_mode, 'TriggerMode')

            # Set TriggerSelector to FrameStart
            # For this example, the trigger selector should be set to frame start.
            # This is the default for most cameras.
            self.set_node(trigger_config['Trigger Selector'], 'TriggerSelector')

            # Select trigger source
            # The trigger source must be set to hardware or software while trigger
            # mode is off.
            node_trigger_source = PySpin.CEnumerationPtr(self.nodemap.GetNode('TriggerSource'))
            if not PySpin.IsAvailable(node_trigger_source) or not PySpin.IsWritable(node_trigger_source):
                print('Unable to get trigger source (node retrieval). Aborting...')
                return False

            if self.trigger_type == 'SOFTWARE':
                self.set_node(trigger_config['Trigger Source'], 'TriggerSource', 'Software')
                print('Trigger source set to software...')

            elif self.trigger_type == 'HARDWARE':
                self.set_node(trigger_config['Trigger Source'], 'TriggerSource', 'Line0')
                print('Trigger source set to hardware...')

            # Turn trigger mode on
            # Once the appropriate trigger source has been set, turn trigger mode
            # on in order to retrieve images using the trigger.
            trigger_mode['entry_symbolic'] = 'On'
            self.set_node(trigger_mode, 'TriggerMode')

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return True

    def reset_trigger(self, trigger_config: Dict = None) -> bool:
        """This function returns the camera to a normal state by turning off trigger mode.

        Args:
            trigger_config (Dict): Configuration parameters for trigger. default: None.

        Returns:
            Boolean: Whether the configuration was successful.
        """

        if not trigger_config:
            trigger_config = self.camera_feature_config['Acquisition Control']['Trigger Mode']

        result = self.set_node(trigger_config, 'TriggerMode')
        return result

    def grab_next_image_by_trigger(self):
        """Use trigger to capture image.
        The software trigger only feigns being executed by the Enter key;
        what might not be immediately apparent is that there is not a
        continuous stream of images being captured; in other examples that
        acquire images, the camera captures a continuous stream of images.
        When an image is retrieved, it is plucked from the stream.

        Returns:
            img (ndarray): Captured image.
        """
        try:
            if self.trigger_type == 'SOFTWARE':
                # Execute software trigger
                node_softwaretrigger_cmd = PySpin.CCommandPtr(self.nodemap.GetNode('TriggerSoftware'))
                if not PySpin.IsAvailable(node_softwaretrigger_cmd) or not PySpin.IsWritable(node_softwaretrigger_cmd):
                    print('Unable to execute trigger. Aborting...')
                    return False
                node_softwaretrigger_cmd.Execute()

            elif self.trigger_type == 'HARDWARE':
                print('Use the hardware to trigger image acquisition.')

            img = self.capture()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return img

    def capture(self):
        """Get an image from your current camera and convert it to ndarray format.

        Returns:
            image (ndarray): The image captured.
        """
        frame = self.current_cam.GetNextImage(1000)
        if frame.IsIncomplete():
            raise print('Image incomplete with image status %d ...' % frame.GetImageStatus())
        else:
            data = frame.GetData()
            height, width = frame.GetHeight(), frame.GetWidth()
            channels = frame.GetNumChannels()
            image = np.reshape(data, (height, width, channels))
        frame.Release()
        return image

    # todo 完成帧率计算函数
    def get_fps(self):
        """Gets the frame rate of the currently captured image.
        """
        pass

    def stop(self):
        """Stop capturing images
        """
        self.current_cam.EndAcquisition()
        self.reset_trigger()
