# due to the way KLayout handles Python imports, to import module patching.py
# we firstly have to add the absolute current working directory to sys.path
import os
import sys
import pya

# Ensure the current directory is in sys.path for module imports
script_path = os.path.abspath(__file__)
current_dir = os.path.dirname(script_path)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- Define the GUI Dialog Class ---

class PatchingDialog(pya.QDialog):
    """
    This class defines the GUI dialog for the auto-patching tool.
    It inherits from pya.QDialog, which is KLayout's wrapper for Qt's QDialog.
    """
    
    def __init__(self, parent=None):
        # Call the constructor of the parent class (QDialog)
        super(PatchingDialog, self).__init__(parent)
        
        # Set the window title
        self.setWindowTitle("Auto-Patching")
        
        # ----------------------- Create Widgets (UI elements) ---------------------
        # set grid layout for the dialog
        layout = pya.QGridLayout(self)

        # Input Shapes
        layout.addWidget(pya.QLabel("Layer of Input Shapes", self), 0, 0, 1, 2) # Spanning 2 columns
        
        layout.addWidget(pya.QLabel("Electrode Layer:", self), 1, 0)
        self.electrode_layer_input = pya.QLineEdit("1", self)
        layout.addWidget(self.electrode_layer_input, 1, 1)

        layout.addWidget(pya.QLabel("Writing Field Layer:", self), 2, 0)
        self.writing_field_layer_input = pya.QLineEdit("", self)
        layout.addWidget(self.writing_field_layer_input, 2, 1)

        # Separator
        line = pya.QFrame(self); line.setFrameShape(pya.QFrame.HLine); line.setFrameShadow(pya.QFrame.Sunken)
        layout.addWidget(line, 3, 0, 1, 2)


        # Output Shapes
        layout.addWidget(pya.QLabel("Layer of Output Shapes", self), 4, 0, 1, 2) # Spanning 2 columns

        layout.addWidget(pya.QLabel("Grid Layer", self), 5, 0)
        self.grid_layer_input = pya.QLineEdit("", self)
        layout.addWidget(self.grid_layer_input, 5, 1)

        layout.addWidget(pya.QLabel("Patch Layer", self), 6, 0)
        self.patch_layer_input = pya.QLineEdit("", self)
        layout.addWidget(self.patch_layer_input, 6, 1)

        # Separator
        line = pya.QFrame(self); line.setFrameShape(pya.QFrame.HLine); line.setFrameShadow(pya.QFrame.Sunken)
        layout.addWidget(line, 7, 0, 1, 2)

        # Grid and patch settings
        layout.addWidget(pya.QLabel("Grid Width (µm):", self), 8, 0)
        self.grid_width_input = pya.QLineEdit("1", self)
        layout.addWidget(self.grid_width_input, 8, 1)

        layout.addWidget(pya.QLabel("Patch Size (µm):", self), 9, 0)
        self.patch_size_input = pya.QLineEdit("8", self)
        layout.addWidget(self.patch_size_input, 9, 1)

        # --- OK Buttons ---
        self.ok_button = pya.QPushButton("Create Patches", self)
        self.ok_button.clicked(self.on_ok_clicked) # Connect button click to a method
        layout.addWidget(self.ok_button, 10, 0, 1, 2)
        
    def on_ok_clicked(self):
        """
        This method is executed when the 'Run Patching' button is clicked.
        """
        try:
            # Get layer input
            electrode_layer_info = pya.LayerInfo.from_string(self.electrode_layer_input.text + "/0")
            writing_field_layer_info = pya.LayerInfo.from_string(self.writing_field_layer_input.text + "/0")
            grid_layer_info = pya.LayerInfo.from_string(self.grid_layer_input.text + "/0")
            patch_layer_info = pya.LayerInfo.from_string(self.patch_layer_input.text + "/0")
            
            # Convert text inputs to numbers (float for sizes, int for layers)
            grid_width = float(self.grid_width_input.text)
            patch_size = float(self.patch_size_input.text)
            
            print("Starting auto-patching process...")

            # --- call functions to create patches ---
            
            # Get the main KLayout objects
            app = pya.Application.instance()
            mw = app.main_window()
            lv = mw.current_view()
            if lv is None: raise Exception("No layout view open.")
            layout = lv.active_cellview().layout()
            cell = lv.active_cellview().cell

            # Call the grid creation function
            from patching import create_grid_from_shapes, create_patch

            # Firstly create grid
            create_grid_from_shapes(layout, cell, 
                                    writing_field_layer_info.layer, 
                                    grid_layer_info.layer, 
                                    grid_width)
            
            # Then create patches at the intersection between grid and electrode
            create_patch(layout, cell,
                         electrode_layer_info.layer,
                         grid_layer_info.layer, 
                         patch_layer_info.layer, 
                         patch_size)
            
            print("Process finished successfully!")
            self.accept() # Close the dialog after success

        except Exception as e:
            # Show any errors in a message box
            pya.QMessageBox.critical(self, "Error", str(e))