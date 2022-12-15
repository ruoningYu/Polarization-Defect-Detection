import PySpin

MAX_CHARS = 100

NODES_TYPE = {
    6: 'string',
    2: 'integer',
    5: 'float',
    3: 'boolean',
    4: 'command',
}


def get_node_info(node):
    """Gets information about a single node, including the node name
    and corresponding value.

    Args:
        node (IValue): A node object.

    Returns:
        node_info (Dict): Information for a node.
    """
    node_type = NODES_TYPE[node.GetPrincipalInterfaceType()]
    _node = getattr(PySpin, f'C{node_type.title()}Ptr')(node)
    display_name = _node.GetDisplayName()

    if node_type == 'command':
        value = _node.GetToolTip()
    else:
        value = _node.GetValue()

    if node_type == 'string' or node_type == 'command':
        value = value[:MAX_CHARS] + '...' if len(value) > MAX_CHARS else value

    node_info = {
        display_name:
            {
                "value": value,
                "type": node_type
            },
    }

    return node_info


def get_enumeration_node_and_current_entry(node):
    """Gets information about enumerating class nodes.

    Args:
        node (IValue): A node object.

    Returns:
        node_info (Dict): Information for a node.

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
    """Gets information about all nodes under a category node
    based on the name and rank of that category.

    Args:
        node (IValue): A node object.
        level (int):  The level of the layer.
        layer (str): The name of the layer.

    Returns:
        nodes_info_dict (Dict): Information about all nodes under the category node.
    """
    node_category = PySpin.CCategoryPtr(node)
    display_name = node_category.GetDisplayName()

    nodes_info_dict = {
        display_name: dict()
    }

    for node_feature in node_category.GetFeatures():

        if not PySpin.IsAvailable(node_feature) or not PySpin.IsReadable(node_feature):
            continue

        if node_feature.GetPrincipalInterfaceType() == PySpin.intfICategory:
            _temp_node_info_dict = get_category_node_and_all_feature(node_feature, level + 1, layer)
            node_info = None

        try:
            node_info = get_node_info(node_feature)
        except KeyError:
            pass

        if node_feature.GetPrincipalInterfaceType() == PySpin.intfIEnumeration:
            node_info = get_enumeration_node_and_current_entry(node_feature)

        if node_info:
            try:
                nodes_info_dict[display_name].update(node_info)
            except KeyError:
                pass
        else:
            nodes_info_dict[display_name].update(_temp_node_info_dict)

    return nodes_info_dict


def get_whole_nodemap(cam):
    """Get a dictionary containing information about all the parameters
    of the camera.

    Args:
        cam (Camera): A camera instance.

    Returns:
        nodemap_dict (Dict): A dict of all nodes and node information.
        Used to display and manipulate all parameters of the camera.
    """
    level = 0
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
