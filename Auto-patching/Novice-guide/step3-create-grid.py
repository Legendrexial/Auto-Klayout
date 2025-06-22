# -----------------------------------------------------------------------------
# 步骤三：创建虚拟“写场网格”
# -----------------------------------------------------------------------------

import pya
import sys
import os

# 1. 获取当前脚本文件(e.g., my_macro.lym)的绝对路径
#    os.path.abspath(__file__) 是关键，它能确保我们得到一个完整的、不会出错的路径
script_path = os.path.abspath(__file__)

# 2. 从这个绝对路径中，获取脚本所在的目录
current_dir = os.path.dirname(script_path)

# 3. 再一次使用os.path.dirname，从当前目录获取父目录的路径
parent_dir = os.path.dirname(current_dir)

# 4. 【核心】将这个计算出的、正确的父目录绝对路径添加到Python的模块搜索列表(sys.path)中
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from auto_klayout_toolkit import *


print("--- Step 3 Script Started ---")

# --- Part 1: 获取版图并定义参数 ---
# 定义网格参数 (单位: 微米)
AREA_SIZE = 5000.0  # 整个曝光区域的边长
FIELD_SIZE = 1000.0 # 单个写场的边长
GRID_LINE_WIDTH = 1.0 # 我们画的网格辅助线的宽度 (这个值不重要，设为1即可)
X_LEFT = -810
Y_BOTTOM = -1650
GRID_LAYER = 51 # GRID_LAYER/0 is the layer where grid lines will be drawn

# 这部分代码与步骤二相同，用于获取当前版图
app = pya.Application.instance()
mw = app.main_window()
lv = mw.current_view()
if lv is None:
  raise Exception("No layout view found. Please open a layout first.")
layout = lv.active_cellview().layout()
top_cell = lv.active_cellview().cell
print(f"Accessed layout for cell: '{top_cell.name}'")

# 【重要概念】: Klayout在后台使用整数“数据库单位(dbu)”来表示所有坐标和尺寸。
# 我们必须将微米单位转换为dbu，才能精确地创建图形。
# layout.dbu 告诉我们1个dbu等于多少微米 (例如 0.001 um/dbu)。
dbu = layout.dbu
area_size_dbu = int(AREA_SIZE / dbu)
field_size_dbu = int(FIELD_SIZE / dbu)
grid_line_width_dbu = int(GRID_LINE_WIDTH / dbu)
x_left_dbu = int(X_LEFT / dbu)
y_bottom_dbu = int(Y_BOTTOM / dbu)

print(f"Layout database unit (dbu) is: {dbu} um")

# --- Part 2: 创建一个新图层用于存放网格线 ---

# 我们将把网格线画在一个新的、临时的图层上 (例如 200/0)，
# 以免与我们的原始设计混淆。
grid_layer_info = pya.LayerInfo(GRID_LAYER, 0)

# 步骤一：尝试用 find_layer() 查找这个图层
grid_layer_index = find_or_create_layer(layout, grid_layer_info)

print(f"Grid lines will be drawn on layer {grid_layer_info}.")


# --- Part 3: 使用循环创建网格线 ---

# 计算需要画多少条线 (5000/1000 = 5个写场，中间有4条分界线)
num_lines = int(AREA_SIZE / FIELD_SIZE) - 1

# 循环创建垂直的网格线
print(f"Creating {num_lines} vertical grid lines...")
for i in range(1, num_lines + 1):
  # 计算每条线的中心x坐标
  x_pos = i * field_size_dbu + x_left_dbu
  # 定义线的左下角和右上角坐标，从而创建一个细长的矩形(Box)
  p1 = pya.Point(x_pos - grid_line_width_dbu // 2, y_bottom_dbu)
  p2 = pya.Point(x_pos + grid_line_width_dbu // 2, area_size_dbu + y_bottom_dbu)
  print(p1)
  # 在指定的图层上插入这个新的Box图形
  top_cell.shapes(grid_layer_index).insert(pya.Box(p1, p2))

# 循环创建水平的网格线
print(f"Creating {num_lines} horizontal grid lines...")
for i in range(1, num_lines + 1):
  y_pos = i * field_size_dbu + y_bottom_dbu
  p1 = pya.Point(x_left_dbu, y_pos - grid_line_width_dbu // 2)
  p2 = pya.Point(area_size_dbu + x_left_dbu, y_pos + grid_line_width_dbu // 2)
  top_cell.shapes(grid_layer_index).insert(pya.Box(p1, p2))

print("--- Script Finished ---")
print(f"Grid creation complete. Check layer {GRID_LAYER}/0 in your layout.")



