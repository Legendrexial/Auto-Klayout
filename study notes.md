# Errors encountered during development

## pya.Region()

#### What can be "Region"ed?

```python
for shape in cell.shapes(box_layer_index):
    pya.Region(shape) # wrong! "shape" cannot be converted to "Region"
    pya.Region(shape.box()) # wrong! "box" is no callable.
    pya.Region(shape.box) # correct
```

1. shape cannot be Regioned
2. only box/polygon etc. objects can be Regioned.



## How to extract Edges?

```python
all_edges = pya.Edges() # empty object
for shape in cell.shapes(box_layer_index):
    all_edges.insert(shape.edges()) # wrong! shape has no attribute .edges()
    all_edges.insert(shape.edge) # wrong! shape.edge cannot be inserted into pya.Edges()
    
```

#### correct way:

```python
all_edges = pya.Edges() # empty object
for shape in cell.shapes(box_layer_index):
    temp_polygon = shape.polygon # turn any shapes to polygon
    shape_region = pya.Region(temp_polygon) # turn polygon into Region
    all_edges.insert(shape_region.edges()) # get edges from Region.edges()
```

