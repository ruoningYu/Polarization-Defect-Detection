import PySpin


class Enumeration:

    def __init__(self):
        self.interface_tree_model = dict()
        self.cam_dict = dict()

    def query_interface(self, interface):
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
            self.interface_tree_model[interface_display_name] = []

            interface.UpdateCameras()
            cam_list = interface.GetCameras()
            num_cams = cam_list.GetSize()

            if num_cams == 0:
                # 当前接口没有相机
                return result

            for i, cam in enumerate(cam_list):

                nodemap_tldevice = cam.GetTLDeviceNodeMap()
                node_device_vendor_name = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceVendorName'))
                if PySpin.IsAvailable(node_device_vendor_name) and PySpin.IsReadable(node_device_vendor_name):
                    device_vendor_name = node_device_vendor_name.ToString()

                node_device_model_name = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceModelName'))
                if PySpin.IsAvailable(node_device_model_name) and PySpin.IsReadable(node_device_model_name):
                    device_model_name = node_device_model_name.ToString()

                self.interface_tree_model[interface_display_name].append(
                    ["Device {}".format(i), device_vendor_name, device_model_name])
                # print('\tDevice %i %s %s \n' % (i, device_vendor_name, device_model_name))
                self.cam_dict[device_vendor_name + " " + device_model_name] = cam

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result

    def call_interface(self, system):
        result = True

        self.iface_list = system.GetInterfaces()
        # 当前设备的接口数量
        num_interfaces = self.iface_list.GetSize()

        # 获取已连接的相机数量
        self.cam_list = system.GetCameras()
        num_cams = self.cam_list.GetSize()

        # 没有相机返回False
        if num_cams == 0 or num_interfaces == 0:
            return False

        print('\n*** 扫描设备串口中··· ***\n')

        for iface in self.iface_list:
            result &= self.query_interface(iface)

        return result

    def get_interface_model(self, system):
        result = self.call_interface(system)
        if result:
            return self.interface_tree_model
        else:
            print("找不到相机")
            return {'none': [["none", "none", "none"]]}

    def create_camera_instance(self, cam_name):
        cam = self.cam_dict[cam_name]
        cam.Init()
        return cam

    def __del__(self):
        self.cam_list.Clear()
        self.iface_list.Clear()

