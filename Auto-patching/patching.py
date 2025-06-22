import pya

def create_grid(layout, cell, grid_layer, area_size, field_size, grid_line_width, x_left, y_bottom, datatype=0):
    """
    Create a grid of rectangles in the specified layout and layer.
    The grid is the boundary of writing fields, the whole exposure area size is area_size^2, 
    divided into writing fields of size field_size^2. The left-bottom coordinate of the area is (x_left, y_bottom).
    """
    # turn um into dbu (standard unit in KLayout)
    dbu = layout.dbu
    area_size_dbu = int(area_size / dbu)
    field_size_dbu = int(field_size / dbu)
    grid_line_width_dbu = int(grid_line_width / dbu)
    x_left_dbu = int(x_left / dbu)
    y_bottom_dbu = int(y_bottom / dbu)

    # find or create the grid layer
    grid_layer_info = pya.LayerInfo(grid_layer, datatype)
    grid_layer_index = layout.find_layer(grid_layer_info)
    if grid_layer_index is None:
        grid_layer_index = layout.create_layer(grid_layer_info)

    # calculate the number of lines needed
    num_lines = int(area_size / field_size) - 1

    for i in range(1, num_lines + 1):
        # create vertical lines
        x_pos = i * field_size_dbu + x_left_dbu
        p1 = pya.Point(x_pos - grid_line_width_dbu // 2, y_bottom_dbu)
        p2 = pya.Point(x_pos + grid_line_width_dbu // 2, area_size_dbu + y_bottom_dbu)
        cell.shapes(grid_layer_index).insert(pya.Box(p1, p2))

        # create horizontal lines
        y_pos = i * field_size_dbu + y_bottom_dbu
        p1 = pya.Point(x_left_dbu, y_pos - grid_line_width_dbu // 2)
        p2 = pya.Point(area_size_dbu + x_left_dbu, y_pos + grid_line_width_dbu // 2)
        cell.shapes(grid_layer_index).insert(pya.Box(p1, p2))

    print("Grid created on layer: ", grid_layer_info)
    
    return


def create_patch(layout, cell, electrode_layer, grid_layer, patch_layer, patch_size):
    """
    Create patches at the center of intersections between electrode and grid layers.
    Datatype for all layers must be 0.
    """
    # Get the database unit (dbu) for unit conversion
    dbu = layout.dbu
    patch_size_dbu = int(patch_size / dbu)

    # Get layer indices
    electrode_layer_index = layout.find_layer(pya.LayerInfo(electrode_layer, 0))
    grid_layer_index = layout.find_layer(pya.LayerInfo(grid_layer, 0))
    patch_layer_index = layout.find_layer(pya.LayerInfo(patch_layer, 0))
    if patch_layer_index is None:
        patch_layer_index = layout.create_layer(pya.LayerInfo(patch_layer, 0))

    # Create Regions for boolean operations
    electrode_regioin = pya.Region(cell.shapes(electrode_layer_index))
    grid_region = pya.Region(cell.shapes(grid_layer_index))

    # Find intersections
    intersection_region = electrode_regioin & grid_region

    # Create patches at the center of intersections
    if intersection_region.is_empty():
        print("Warning: No intersections found between the electrode layer and the grid layer.")
    for intersection_shape in intersection_region.each():
        center = intersection_shape.bbox().center()
        p1 = pya.Point(center.x - patch_size_dbu//2, center.y - patch_size_dbu//2)
        p2 = pya.Point(center.x + patch_size_dbu//2, center.y + patch_size_dbu//2)
        cell.shapes(patch_layer_index).insert(pya.Box(p1, p2))
        
    print(f"Patches created on layer {patch_layer_index}.")
    
    return