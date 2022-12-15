import PySpin


class Enumeration:
    """Scan the interface list and get the device information.
        interface_info (dict): All devices' information.
        cam_dict (dict): All cameras information.
    """

    def __init__(self):
        self.interface_info = dict()
        self.cam_dict = dict()

    @staticmethod
    def get_cam_name(cam):
        """Get the device name information.

        Args:
            cam : camera on the interface.

        Returns:
            device_vendor_name (str): device vendor.
            device_model_name (str): device name.
        """
        try:
            nodemap_tldevice = cam.GetTLDeviceNodeMap()
            node_device_vendor_name = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceVendorName'))
            if PySpin.IsAvailable(node_device_vendor_name) and PySpin.IsReadable(node_device_vendor_name):
                device_vendor_name = node_device_vendor_name.ToString()

            node_device_model_name = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceModelName'))
            if PySpin.IsAvailable(node_device_model_name) and PySpin.IsReadable(node_device_model_name):
                device_model_name = node_device_model_name.ToString()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)

        return device_vendor_name, device_model_name

    def query_interface(self, interface):
        """ Queries an interface for its cameras and return device information.

        Args:
            interface: InterfacePtr of PySpin.

        Returns:
            Boolean: True if successful, False otherwise.
        """
        try:
            result = True

            nodemap_interface = interface.GetTLNodeMap()
            node_interface_display_name = PySpin.CStringPtr(nodemap_interface.GetNode('InterfaceDisplayName'))

            if PySpin.IsAvailable(node_interface_display_name) and PySpin.IsReadable(node_interface_display_name):
                try:
                    interface_display_name = node_interface_display_name.GetValue()
                except UnicodeDecodeError:
                    interface_display_name = "Intel(R) USB 3.0 Scalable Host Controller"
            else:
                print('Interface display name not readable')

            self.interface_info[interface_display_name] = []

            # *** NOTES ***
            # Updating the cameras on each interface is especially important if
            # there has been any device arrivals or removals since the last time
            # that UpdateCameras() was called.
            interface.UpdateCameras()

            # *** NOTES ***
            # Camera lists can be retrieved from an interface or the system object.
            # Camera lists retrieved from an interface, such as this one, only
            # return cameras attached on that specific interface whereas camera
            # lists retrieved from the system will return all cameras on all
            # interfaces.
            self.cam_list = interface.GetCameras()

            # Retrieve number of cameras
            num_cams = self.cam_list.GetSize()

            if num_cams == 0:
                return result

            for i, cam in enumerate(self.cam_list):
                device_vendor_name, device_model_name = self.get_cam_name(cam)
                self.interface_info[interface_display_name].append(["Device {}".format(i),
                                                                    device_vendor_name, device_model_name])
                self.cam_dict[device_vendor_name + " " + device_model_name] = cam

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result

    def call_interface(self, system):
        """Scan the host interface and access it.

        Args:
            system : smart pointer (SystemPtr) to the system instance.

        Returns:
            Boolean: True if successful, False otherwise.
        """
        result = True
        self.iface_list = system.GetInterfaces()
        num_interfaces = self.iface_list.GetSize()

        if num_interfaces == 0:
            return False

        for iface in self.iface_list:
            result &= self.query_interface(iface)

        return result

    def get_interface_info(self, system):
        """Get information about all interfaces as well as the camera name.

        Args:
            system: smart pointer (SystemPtr) to the system instance.

        Returns:
            Dict: All interfaces information.
        """
        if self.call_interface(system):
            return self.interface_info
        else:
            return {'none': [["none", "none", "none"]]}

    def create_camera_instance(self, cam_name):
        """Instantiates the camera selected in the list.

        Args:
            cam_name (str): The camera name of the choice.

        Returns:
            Camera Instance.
        """
        return self.cam_dict[cam_name]

    def __del__(self):
        """Interface and Cam lists must be cleared manually prior to a system release call.
        """
        self.cam_list.Clear()
        self.iface_list.Clear()

