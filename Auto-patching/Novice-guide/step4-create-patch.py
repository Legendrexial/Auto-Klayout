# -----------------------------------------------------------------------------
# 步骤四 & 五：计算交点并生成补丁
# -----------------------------------------------------------------------------

import pya

print("--- Steps 4 & 5 Script Started ---")

# --- Part 1: 定义参数和获取对象 ---

# get current active cellview
active_cellview = pya.Application.instance().main_window().current_view().active_cellview()

# get layout and cell from the active cellview
layout = active_cellview.layout()
cell = active_cellview.cell

print(f"Accessed layout for cell: '{cell.name}'")

# --- Define layer and size parameters ---
# Datatype is always 0
ELECTRODE_LAYER = 6
GRID_LAYER = 51
PATCH_LAYER = 202

PATCH_SIZE = 8.0  # um, the side length of the square patch

# Get the database unit (dbu) for unit conversion
dbu = layout.dbu
patch_size_dbu = int(PATCH_SIZE / dbu)

# --- Part 2: Get Input Layers and Create Region Objects ---

# Define and get the layer index for the electrodes
electrode_layer_info = pya.LayerInfo(ELECTRODE_LAYER, 0)
electrode_layer_index = layout.find_layer(electrode_layer_info)
if electrode_layer_index is None:
    raise Exception(f"Electrode layer {electrode_layer_info} not found.")

# Define and get the layer index for the grid
grid_layer_info = pya.LayerInfo(GRID_LAYER, 0)
grid_layer_index = layout.find_layer(grid_layer_info)
if grid_layer_index is None:
    raise Exception(f"Grid layer {grid_layer_info} not found. Please run Step 3 script first.")

# Create Region objects. A Region can be seen as a collection of all shapes on a layer.
print("Creating Regions from layers...")
electrode_region = pya.Region(cell.shapes(electrode_layer_index))
grid_region = pya.Region(cell.shapes(grid_layer_index))

# --- Part 3: Perform Boolean Operation to Find Intersections ---

# This is the core step: use the '&' operator to perform a boolean AND on the two Regions.
# The result, 'intersection_region', will only contain the overlapping parts.
print("Performing boolean AND operation to find intersections...")
intersection_region = electrode_region & grid_region

print(dir(intersection_region))  # Debug: print available methods and attributes

# Check how many intersections were found
num_intersections = intersection_region.size()
if num_intersections == 0:
    print("Warning: No intersections found between the electrode layer and the grid layer.")
else:
     print(f"Found {num_intersections} intersection(s).")

# --- Part 4: Create Patches at the Center of Intersections ---

# Get or create the output layer for the patches
patch_layer_info = pya.LayerInfo(PATCH_LAYER, 0)
patch_layer_index = layout.find_layer(patch_layer_info)
if patch_layer_index is None:
    patch_layer_index = layout.insert_layer(patch_layer_info)
print(f"Patches will be created on layer {patch_layer_info}.")

# Iterate over each small intersection shape found
for intersection_shape in intersection_region.each():
    # Get the center point of the intersection shape's bounding box
    center_point = intersection_shape.bbox().center()
    
    # Based on the center point, calculate the lower-left and upper-right corners of the patch
    p1 = pya.Point(center_point.x - patch_size_dbu // 2, center_point.y - patch_size_dbu // 2)
    p2 = pya.Point(center_point.x + patch_size_dbu // 2, center_point.y + patch_size_dbu // 2)

    # Create a square patch (Box) and insert it into the patch layer
    cell.shapes(patch_layer_index).insert(pya.Box(p1, p2))

print(f"--- Script Finished ---")
print(f"Successfully created {num_intersections} patches on layer {patch_layer_info}.")