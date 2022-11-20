
import PySpin

MAX_CHARS = 100


def get_string_node(node):
    node_type = "string"
    node_string = PySpin.CStringPtr(node)

    display_name = node_string.GetDisplayName()
    value = node_string.GetValue()
    value = value[:MAX_CHARS] + '...' if len(value) > MAX_CHARS else value

    node_info = {
        display_name:
            {
                "value": value,
                "type": node_type
            },
    }

    return node_info


def get_integer_node(node):
    node_type = "integer"
    node_integer = PySpin.CIntegerPtr(node)

    display_name = node_integer.GetDisplayName()
    value = node_integer.GetValue()

    node_info = {
        display_name:
            {
                "value": value,
                "type": node_type
            },
    }

    return node_info


def get_float_node(node):
    node_type = "float"
    node_float = PySpin.CFloatPtr(node)

    display_name = node_float.GetDisplayName()
    value = node_float.GetValue()

    node_info = {
        display_name:
            {
                "value": value,
                "type": node_type
            },
    }

    return node_info


def get_boolean_node(node):
    node_type = "boolean"
    node_boolean = PySpin.CBooleanPtr(node)

    display_name = node_boolean.GetDisplayName()
    value = node_boolean.GetValue()

    node_info = {
        display_name:
            {
                "value": value,
                "type": node_type
            },
    }

    return node_info


def get_commend_node(node):
    node_type = "command"
    node_commend = PySpin.CCommandPtr(node)

    display_name = node_commend.GetDisplayName()
    tooltip = node_commend.GetToolTip()
    tooltip = tooltip[:MAX_CHARS] + '...' if len(tooltip) > MAX_CHARS else tooltip

    node_info = {
        display_name:
            {
                "tooltip": tooltip,
                "type": node_type
            },
    }

    return node_info


def get_enumeration_node_and_current_entry(node):
    """

    Parameters
    ----------
    node

    Returns
    -------

    """
    node_type = "enumeration"
    node_enumeration = PySpin.CEnumerationPtr(node)
    node_enum_entry = PySpin.CEnumEntryPtr(node_enumeration.GetCurrentEntry())

    display_name = node_enumeration.GetDisplayName()
    entry_symbolic = node_enum_entry.GetSymbolic()

    node_info = {
        display_name:
            {
                "entry_symbolic": entry_symbolic,
                "type": node_type
            },
    }

    return node_info


def get_category_node_and_all_feature(node, level, layer):
    """

    Parameters
    ----------
    node (str): node节点
    level (str): 层的等级
    layer (int): 层的名称

    Returns (dict): 一个层下的所有节点
    -------

    """
    node_category = PySpin.CCategoryPtr(node)
    display_name = node_category.GetDisplayName()

    temp_node_info_dict = {
        display_name: dict()
    }

    for node_feature in node_category.GetFeatures():

        if not PySpin.IsAvailable(node_feature) or not PySpin.IsReadable(node_feature):
            continue

        if node_feature.GetPrincipalInterfaceType() == PySpin.intfICategory:
            _temp_node_info_dict = get_category_node_and_all_feature(node_feature, level + 1, layer)
            node_info = None

        if node_feature.GetPrincipalInterfaceType() == PySpin.intfIString:

            node_info = get_string_node(node_feature)
        elif node_feature.GetPrincipalInterfaceType() == PySpin.intfIInteger:

            node_info = get_integer_node(node_feature)
        elif node_feature.GetPrincipalInterfaceType() == PySpin.intfIFloat:

            node_info = get_float_node(node_feature)
        elif node_feature.GetPrincipalInterfaceType() == PySpin.intfIBoolean:

            node_info = get_boolean_node(node_feature)
        elif node_feature.GetPrincipalInterfaceType() == PySpin.intfICommand:

            node_info = get_commend_node(node_feature)
        elif node_feature.GetPrincipalInterfaceType() == PySpin.intfIEnumeration:

            node_info = get_enumeration_node_and_current_entry(node_feature)

        if node_info:
            try:
                temp_node_info_dict[display_name].update(node_info)
            except KeyError:
                pass
        else:
            temp_node_info_dict[display_name].update(_temp_node_info_dict)

    return temp_node_info_dict


def get_whole_nodemap(cam):
    """

    Parameters
    ----------
    cam (Camera): 一个相机实例

    Returns (dict): 返回包含所有node的字典
    -------

    """
    level = 0
    cam.Init()
    nodemap_dict = dict()
    nodemap_applayer = cam.GetNodeMap()
    nodemap_applayer_detail = get_category_node_and_all_feature(nodemap_applayer.GetNode('Root'), level,
                                                                     "applayer")
    nodemap_dict['Camera Feature'] = nodemap_applayer_detail

    nodemap_gentl = cam.GetTLDeviceNodeMap()
    nodemap_gentl_detail = get_category_node_and_all_feature(nodemap_gentl.GetNode('Root'), level, "gentl")
    nodemap_dict['Transport Layer'] = nodemap_gentl_detail

    nodemap_tlstream = cam.GetTLStreamNodeMap()
    nodemap_tlstream_detail = get_category_node_and_all_feature(nodemap_tlstream.GetNode('Root'), level,
                                                                     "tlstream")
    nodemap_dict['Stream Parameters'] = nodemap_tlstream_detail

    return nodemap_dict
