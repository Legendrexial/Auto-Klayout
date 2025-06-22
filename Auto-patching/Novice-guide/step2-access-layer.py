# -----------------------------------------------------------------------------
# 步骤二：访问版图 - 获取目标图层
# -----------------------------------------------------------------------------

# 导入Klayout的核心库，所有脚本都必须有这一行
import pya

print("--- Step 2 Script Started ---")

# 1. 获取当前活动的版图对象
# 这是标准的“样板代码”，用于获取程序、主窗口、当前视图等核心对象。
app = pya.Application.instance()
mw = app.main_window()
lv = mw.current_view()

# 一个好的习惯是检查当前是否有视图，如果没有则报错退出。
if lv is None:
  raise Exception("No layout view found. Please open a layout first.")

# 从当前视图中，获取版图(layout)和它所在的单元(cell)
# layout 对象就是您整个GDS文件的数据库。
layout = lv.active_cellview().layout()
cell = lv.active_cellview().cell

print(f"Successfully accessed layout for cell: '{cell.name}'")

# 2. 定义您想要访问的目标图层
# 在GDSII格式中，一个图层由 Layer Number 和 Datatype Number 共同确定。
# !!!【请修改这里】!!!
# 请将下面的数字修改为您GDS文件中存放电极的实际层号。
ELECTRODE_LAYER = 6
ELECTRODE_DATATYPE = 0

# 使用pya.LayerInfo来创建一个图层信息的对象
electrode_layer_info = pya.LayerInfo(ELECTRODE_LAYER, ELECTRODE_DATATYPE)
# electrode_layer_info = pya.LayerInfo.from_string("6/0")


# Klayout内部使用一个整数索引来管理图层，我们需要用LayerInfo来查找这个索引。
electrode_layer_index = layout.layer(electrode_layer_info)

# 再次检查，确保这个图层在您的版图中真实存在。
if electrode_layer_index is None:
  raise Exception(f"Layer {ELECTRODE_LAYER}/{ELECTRODE_DATATYPE} not found in the layout.")

print(f"Target layer {ELECTRODE_LAYER}/{ELECTRODE_DATATYPE} found with internal index: {electrode_layer_index}")

# 3. 遍历图层上的所有形状 (Shapes)
# .shapes() 方法可以获取一个图层上所有的几何图形。
shapes = cell.shapes(electrode_layer_index)

shape_count = 0
# 使用 for 循环来逐个访问每个图形
for shape in shapes:
  # shape 对象包含了图形的所有信息。
  # 我们可以打印出它的基本信息，或者获取它的边界框(Bounding Box)。
  print(f"  - Found a shape: {shape}, Area: {shape.area()} µm²")
  shape_count += 1

print(f"\n--- Script Finished ---")
print(f"Total shapes found on layer {ELECTRODE_LAYER}/{ELECTRODE_DATATYPE}: {shape_count}")
