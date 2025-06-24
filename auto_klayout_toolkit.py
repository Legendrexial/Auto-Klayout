def find_or_create_layer(layout, layer_info):
    """
    尝试查找指定的图层，如果不存在则创建它。
    :param layout: 当前版图对象
    :param layer_info: pya.LayerInfo 对象，包含图层号和数据类型
    :return: 图层的索引
    """
    layer_index = layout.find_layer(layer_info)
    if layer_index is None:
        print(f"Layer {layer_info} is created.")
        layer_index = layout.insert_layer(layer_info)
    else:
        print(f"Layer {layer_info} already exists.")
    return layer_index