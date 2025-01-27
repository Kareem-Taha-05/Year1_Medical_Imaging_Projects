import sys, os, pydicom, numpy as np , nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import(QApplication,QWidget,QPushButton,QVBoxLayout,QFileDialog,QLabel,QGridLayout,QSlider,QMessageBox,QToolBar,QProgressDialog)
from PyQt5.QtCore import Qt 
from PyQt5 import QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MedicalImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Medical Image Viewer")
        self.setGeometry(100, 100, 1600, 800)
        self.setStyleSheet("""
        QWidget{
                background-color:#257180}
        QSlider {
            background: #FFFFFF; /* Background color of the slider */
        }
        QSlider::groove:horizontal {
            background: #FD8B51; /* Color of the groove */
            height: 20px; /* Height of the groove */
        }   
        QSlider::handle:horizontal {
            background: #F2E5BF; /* Handle color */
            width: 15px; /* Width of the handle */
            margin: -2px 0; /* Positioning */
        }
        QGridLayout{
                    background-color:#629584;}
        QPushButton{
                    margin:10px;
                    padding:5px;
                    color:white;
                    background-color: #FD8B51;
                    border: 1px solid #CB6040;
                    font-family: Arial;}
        QPushButton:disabled{
                    margin:10px;
                    padding:5px;
                    background-color: #c0c0c0; /* Gray background for disabled button */
        color: #808080; /* Gray text */}
        QToolBar{
                background-color:#387478}
        QLabel{
                color:#FFFFFF}
        """)
        self.layout = QVBoxLayout()                     #creating the whole UI layout
        self.toolbar = QToolBar()                       #creating a bar that will contail each button later
        self.layout.addWidget(self.toolbar)             #adding the bar that has the buttons to the Full UI layout
        self.grid_layout = QGridLayout()                #creating the grid that will contain the 2D views, 3D volume, and sliders later
        self.layout.addLayout(self.grid_layout)         #adding this grid to the Full UI layout

        #Creating each button, connecting it to its relative method and adding it to the Widget (the widget is already added to the whole UI layout)
        # THE "DICOM DICOM FOLDER" BUTTON
        dicom_button = QPushButton('Upload DICOM Folder', self)          #create
        dicom_button.setObjectName("dicom")                              #set name to use in css coloring
        self.toolbar.addWidget(dicom_button)                             #adding it to the Layout
        dicom_button.clicked.connect(self.upload_folder)                 #connecting to relative method 
        # THE "Upload NIfTI File" BUTTON
        nifti_button = QPushButton('Upload NIfTI File', self)            #create
        nifti_button.setObjectName("nifti")                              #set name to use in css coloring
        self.toolbar.addWidget(nifti_button)                             #adding it to the Layout
        nifti_button.clicked.connect(self.upload_nifti_folder)           #connecting to relative method
        # THE "Switch to zoom"" BUTTON
        self.mode_button = QPushButton('Switch to Zoom Mode', self)      #create
        self.toolbar.addWidget(self.mode_button)                         #adding it to the Layout
        self.mode_button.clicked.connect(self.toggle_mode)               #connecting to relative method
        # THE "Zoom in" BUTTON
        self.zoom_in_button = QPushButton('Zoom In', self)               #create
        self.zoom_in_button.setObjectName("zoom_in")                     #set name to use in css coloring
        self.toolbar.addWidget(self.zoom_in_button)                      #adding it to the Layout
        self.zoom_in_button.clicked.connect(self.zoom_in)                #connecting to relative method
        self.zoom_in_button.setEnabled(False)                            #Initializing it to disabled until we switch to the zoom mode later
        # THE "Zoom Out" Button
        self.zoom_out_button = QPushButton('Zoom Out', self)             #create
        self.zoom_out_button.setObjectName("zoom_out")                   #set name to use in css coloring
        self.toolbar.addWidget(self.zoom_out_button)                     #adding it to the Layout
        self.zoom_out_button.clicked.connect(self.zoom_out)              #connecting to relative method
        self.zoom_out_button.setEnabled(False)                           #Initializing it to disabled until we switch to the zoom mode later

        #Creating the places that will contain the 2D Images with their labels and sliders then adding them to the grid
        #Axial
        self.axial_canvas = FigureCanvas(plt.Figure())                     #creating the empty space for the 2D Axial view using Matplotlib  
        self.axial_canvas.setMinimumSize(300, 300)                         #setting the size of the picture area to 300x300              
        self.axial_view_label = QLabel("Axial View")                       #creating the label
        self.axial_slider = QSlider()                                      #creating the slider
        self.axial_slider.setOrientation(1)                                #setting the slider's orientation to vertical
        self.axial_slider.setRange(0, 0)                                   # Setting the initial range of the slider (0 bec no data is loaded yet)
        self.axial_slider.valueChanged.connect(self.update_axial_index)    #connecting with a method to update the view when moving the slider

        self.grid_layout.addWidget(self.axial_view_label, 0, 0)            #adding label to grid
        self.grid_layout.addWidget(self.axial_canvas, 1, 0)                #adding pic area to grid
        self.grid_layout.addWidget(self.axial_slider, 2, 0)                #adding slider to grid

        self.axial_canvas.mpl_connect('button_press_event', self.on_mouse_press)               #triggers a method when the mouse is pressed
        self.axial_canvas.mpl_connect('button_release_event', self.on_mouse_release)           #triggers a method when the mouse is releases
        self.axial_canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)             #triggers a method when the mouse is moved

        #Saggital
        self.sagittal_canvas = FigureCanvas(plt.Figure())
        self.sagittal_canvas.setMinimumSize(300, 300)
        self.sagittal_view_label = QLabel("Sagittal View")
        self.sagittal_slider = QSlider()
        self.sagittal_slider.setOrientation(1)
        self.sagittal_slider.setRange(0, 0)
        self.sagittal_slider.valueChanged.connect(self.update_sagittal_index)

        self.grid_layout.addWidget(self.sagittal_view_label, 0, 1)
        self.grid_layout.addWidget(self.sagittal_canvas, 1, 1)
        self.grid_layout.addWidget(self.sagittal_slider, 2, 1)

        self.sagittal_canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.sagittal_canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.sagittal_canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        #Coronal
        self.coronal_canvas = FigureCanvas(plt.Figure())
        self.coronal_canvas.setMinimumSize(300, 300)
        self.coronal_view_label = QLabel("Coronal View")
        self.coronal_slider = QSlider()
        self.coronal_slider.setOrientation(1)
        self.coronal_slider.setRange(0, 0)
        self.coronal_slider.valueChanged.connect(self.update_coronal_index)
        
        self.grid_layout.addWidget(self.coronal_view_label, 0, 2)
        self.grid_layout.addWidget(self.coronal_canvas, 1, 2)
        self.grid_layout.addWidget(self.coronal_slider, 2, 2)

        self.coronal_canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.coronal_canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.coronal_canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        #create sliders for brightness and contrast with labels then adding them to the Full UI layout directly 
        #Brightness
        self.brightness_slider = QSlider()                                 #creates a slider
        self.layout.addWidget(QLabel("Brightness"))                        #creates a label for the slider and adding it to the layout
        self.brightness_slider.setOrientation(1)                           #making the slider vertical 
        self.brightness_slider.setRange(-255, 255)                         #setting the range of values for the slider
        self.brightness_slider.setValue(0)                                 #setting the initial value
        self.brightness_slider.valueChanged.connect(self.update_views)     #when the value changes call a method to update the views
        self.layout.addWidget(self.brightness_slider)                      #add the slider to the layout

        #Contrast
        self.contrast_slider = QSlider()
        self.layout.addWidget(QLabel("Contrast"))
        self.contrast_slider.setOrientation(1)
        self.contrast_slider.setRange(-255, 255)
        self.contrast_slider.setValue(0)
        self.contrast_slider.valueChanged.connect(self.update_views)        
        self.layout.addWidget(self.contrast_slider) 

        #Creating the custom mouse shapes for the zoom in and zoom out modes
        #Zoom in
        pm = QtGui.QPixmap(32, 32)                                    #create a 32x32 grid
        pm.fill(QtCore.Qt.transparent)                                #make it transparent
        painter = QtGui.QPainter(pm)                                  #take this grid to a painter
        painter.drawText(0, 0, 32, 32, QtCore.Qt.AlignCenter, "+")    #add the wanted shape in the center
        painter.end()                                                 #save the shape
        self.zoom_in_cursor = QtGui.QCursor(pm)                       #save the shape in a variable called zoom_in_cursor
        #Zoom out       
        pm = QtGui.QPixmap(32, 32)                                    #create a 32x32 grid
        pm.fill(QtCore.Qt.transparent)                                #make it transparent
        painter = QtGui.QPainter(pm)                                  #take this grid to a painter
        painter.drawText(0, 0, 32, 32, QtCore.Qt.AlignCenter, "-")    #add the wanted shape in the center
        painter.end()                                                 #save the shape
        self.zoom_out_cursor = QtGui.QCursor(pm)                      #save the shape in a variable called zoom_out_cursor
        


        #Initializing Attributes
        self.CURSOR_MODE = "cursor"
        self.ZOOM_MODE = "zoom"
        self.current_mode = self.CURSOR_MODE
        self.is_mouse_pressed = False
        self.zoom_mode = False
        self.zoom_in_mode = False
        self.zoom_out_mode = False
        self.zoom_factor = 1.0

        self.image_volume = None
        self.axial_index = None
        self.sagittal_index = None
        self.coronal_index = None
        self.axial_crosshair = None
        self.sagittal_crosshair = None
        self.coronal_crosshair = None

        #Finalizing UI
        self.image_label = QLabel(self)
        self.crosshair_cursor = QtGui.QCursor(QtCore.Qt.CrossCursor)
        self.setLayout(self.layout)
        self.set_cursor_mode()

    #this method takes the file path and reads it
    def load_dicom_slice(self, filepath):
        """Load a single DICOM slice with enhanced compression handling."""
        try:
            dataset = pydicom.dcmread(filepath)                       #reading the dicom data stored in the file    
            pixel_array = dataset.pixel_array                         #convert the data to a pixel array

            # Apply rescale slope and intercept
            if hasattr(dataset, 'RescaleSlope') and hasattr(dataset, 'RescaleIntercept'):            #checks if the file has slope and intercept
                pixel_array = pixel_array * float(dataset.RescaleSlope) + float(dataset.RescaleIntercept)    # apply y=mx+c

            # Normalize to 8-bit range for consistency
            if pixel_array.max() != pixel_array.min():                 #checks that there is variation in pixel values (thus there is an image)
                pixel_array = ((pixel_array - pixel_array.min()) * 255 /                #normalizing then making it in 8 bit range
                             (pixel_array.max() - pixel_array.min())).astype(np.uint8)
            else:
                pixel_array = np.zeros_like(pixel_array, dtype=np.uint8)    #the image is blank so we create an empty array of zeros

            return pixel_array, dataset
        except Exception as e:
            raise Exception(f"Error reading DICOM file {filepath}: {str(e)}")
            
    
    def load_dicom_folder(self, folder_path):
        """Load all DICOM files from a folder with compression handling."""
        try:
            # Get all DICOM files
            dicom_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                          if f.endswith(('.dcm', '.DCM'))]
            
            if not dicom_files:
                raise Exception("No DICOM files found in the selected folder.")

            # Sort files
            dicom_files.sort()

            # Create progress dialog
            progress = QProgressDialog("Loading DICOM files...", "Cancel", 0, len(dicom_files), self)
            progress.setWindowModality(Qt.WindowModal)
                         
            for i, file in enumerate(dicom_files):
                try:
                    dataset = pydicom.dcmread(file)
                except Exception as e:
                    QMessageBox.warning(self, "Warning", f"Error reading file {file}: {str(e)}")
                    continue
                progress.setValue(i)
                if progress.wasCanceled():
                    return

            # Second pass: load and process slices
            slices = []
            progress.setLabelText("Processing DICOM files...")
            progress.setValue(0)

            for i, file in enumerate(dicom_files):
                try:
                    pixel_array, _ = self.load_dicom_slice(file)                    
                    slices.append(pixel_array)
                    progress.setValue(i)
                    if progress.wasCanceled():
                        return
                        
                except Exception as e:
                    QMessageBox.warning(self, "Warning", f"Skipping file {file}: {str(e)}")
                    continue

            progress.setValue(len(dicom_files))

            if not slices:
                raise Exception("No valid DICOM slices could be loaded.")

            # Convert to volume
            self.image_volume = np.array(slices)

            # Initialize indices
            self.axial_index = self.image_volume.shape[0] // 2
            self.sagittal_index = self.image_volume.shape[1] // 2
            self.coronal_index = self.image_volume.shape[2] // 2
            # Update sliders
            self.axial_slider.setRange(0, self.image_volume.shape[0] - 1)
            self.sagittal_slider.setRange(0, self.image_volume.shape[1] - 1)
            self.coronal_slider.setRange(0, self.image_volume.shape[2] - 1)
            
            self.axial_slider.setValue(self.axial_index)
            self.sagittal_slider.setValue(self.sagittal_index)
            self.coronal_slider.setValue(self.coronal_index)

            # Create volume rendering and show views
            self.show_views()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            print(f"Error details: {str(e)}")  # For debugging


    def show_views(self):
        """Display the axial, sagittal, and coronal views."""
        if self.image_volume is None:
            return
        
        views = {
            "Axial": (self.axial_canvas, self.image_volume[self.axial_index, :, :], f"Axial View: Slice {self.axial_index}"),
            "Sagittal": (self.sagittal_canvas, np.rot90(self.image_volume[:, self.sagittal_index, :], k=2), f"Sagittal View: Slice {self.sagittal_index}"),
            "Coronal": (self.coronal_canvas, np.flip(self.image_volume[:, :, self.coronal_index], axis=0), f"Coronal View: Slice {self.coronal_index}"),
        }
        
        for key, (canvas, view, title) in views.items():
            self.prepare_canvas(canvas, view, title)
        
        # Force update after loading
        self.update_views()


    def prepare_canvas(self, canvas, image, title):
        """Helper method to prepare a canvas with the given image and title."""
        canvas.figure.clear()
        ax = canvas.figure.add_subplot(111)
        ax.imshow(image, cmap='gray', origin='lower' if "Sagittal" in title or "Coronal" in title else 'upper')
        ax.axis('off')
        ax.set_title(title)
        canvas.draw()


    def upload_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select DICOM Folder")
        if folder_path:
            self.load_dicom_folder(folder_path)

    def plot_view(self, view, canvas, index, crosshair_position=None):
        canvas.figure.clear()
        ax = canvas.figure.add_subplot(111)
        ax.imshow(view, cmap="gray", aspect='equal')
        ax.axis('off')
        ax.set_title(f'Slice: {index}')

        if crosshair_position is not None:
            ax.axvline(crosshair_position[0], color='red', linestyle='--')
            ax.axhline(crosshair_position[1], color='red', linestyle='--')

        canvas.draw()

    def update_views(self):
        """Update the axial, sagittal, and coronal views with brightness/contrast adjustments."""
        views = {
            "Axial": (self.axial_canvas, self.image_volume[self.axial_index, :, :], self.axial_crosshair),
            "Sagittal": (self.sagittal_canvas, np.rot90(self.image_volume[:, self.sagittal_index, :], k=2), self.sagittal_crosshair),
            "Coronal": (self.coronal_canvas, np.flip(self.image_volume[:, :, self.coronal_index], axis=0), self.coronal_crosshair),
        }
        
        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value()
        
        for key, (canvas, view, crosshair_position) in views.items():
            adjusted_view = self.adjust_brightness_contrast(view, brightness, contrast)
            self.plot_view(adjusted_view, canvas, getattr(self, f"{key.lower()}_index"), crosshair_position)


    def adjust_brightness_contrast(self, image, brightness, contrast):
        image = image.astype(np.float32)
        image += brightness

        image = (image - 0) / (255 - 0)

        if contrast != 0:
            factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
            image = factor * (image - 0.5) + 0.5

        image = np.clip(image, 0, 1)
        image = (image * 255).astype(np.uint8)
        return image

    def update_axial_index(self, value):
        self.axial_index = value
        self.update_views()

    def update_sagittal_index(self, value):
        self.sagittal_index = value
        self.update_views()

    def update_coronal_index(self, value):
        self.coronal_index =  value
        self.update_views()
  

    def set_zoom_state(self, zoom_mode=False, zoom_in=False, zoom_out=False):
        """Helper method to set zoom-related states."""
        self.zoom_mode = zoom_mode
        self.zoom_in_mode = zoom_in
        self.zoom_out_mode = zoom_out

    def update_canvas_limits(self, ax, zoom_factor, x=None, y=None):
        """Update the axis limits for zooming.

        Args:
            ax: The axes object to update.
            zoom_factor: The factor by which to zoom in or out.
            x (optional): The x-coordinate for zoom centering.
            y (optional): The y-coordinate for zoom centering.
        """
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        # Calculate the new limits
        if x is not None and y is not None:
            cx = x
            cy = y
        else:
            cx = (xmin + xmax) / 2
            cy = (ymin + ymax) / 2

        new_dx = (xmax - xmin) / zoom_factor
        new_dy = (ymax - ymin) / zoom_factor

        ax.set_xlim([cx - new_dx / 2, cx + new_dx / 2])
        ax.set_ylim([cy - new_dy / 2, cy + new_dy / 2])


    def zoom_in(self):
        """Enable zoom-in mode and change cursor."""
        if self.current_mode != self.ZOOM_MODE:
            return
        self.set_zoom_state(zoom_mode=True, zoom_in=True)
        self.setCursor(self.zoom_in_cursor)

    def zoom_out(self):
        """Enable zoom-out mode and change cursor."""
        if self.current_mode != self.ZOOM_MODE:
            return
        self.set_zoom_state(zoom_mode=True, zoom_out=True)
        self.setCursor(self.zoom_out_cursor)

    def reset_zoom_mode(self):
        """Reset to default cursor mode."""
        self.zoom_in_mode = False
        self.zoom_out_mode = False
        self.zoom_mode = False
        self.setCursor(QtCore.Qt.ArrowCursor) 

    def toggle_mode(self):
        """Toggle between cursor and zoom modes."""
        if self.current_mode == self.CURSOR_MODE:
            self.set_zoom_mode()
        else:
            self.set_cursor_mode()

    def set_cursor_mode(self):
        """Switch to cursor mode."""
        self.current_mode = self.CURSOR_MODE
        self.mode_button.setText('Switch to Zoom Mode')
        self.zoom_in_button.setEnabled(False)
        self.zoom_out_button.setEnabled(False)
        self.reset_zoom_mode()
        self.setCursor(self.crosshair_cursor)

    def set_zoom_mode(self):
        """Switch to zoom mode."""
        self.current_mode = self.ZOOM_MODE
        self.mode_button.setText('Switch to Cursor Mode')
        self.zoom_in_button.setEnabled(True)
        self.zoom_out_button.setEnabled(True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def update_zoom(self, canvas):
        """Apply the zoom factor to the given canvas."""
        ax = canvas.figure.axes[0]
        zoom_factor = 1 / self.zoom_factor  # Assuming `zoom_factor` is defined elsewhere
        self.update_canvas_limits(ax, zoom_factor)
        canvas.figure.canvas.draw()
        canvas.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def perform_zoom(self, canvas, x, y):
        """Perform a zoom operation centered on a specific point."""
        if not self.zoom_mode or self.current_mode != self.ZOOM_MODE:
            return
            
        ax = canvas.figure.axes[0]  # Get the axes of the canvas
        # Correct zoom factors
        zoom_factor = 2.0 if self.zoom_in_mode else 0.5
        # Update canvas limits based on the zoom factor
        self.update_canvas_limits(ax, zoom_factor, x, y)
        # Redraw the canvas
        canvas.draw()

    def handle_cursor_motion(self, event):
        """Handle cursor motion for different views."""
        if not event.inaxes:
            return
            
        x = int(event.xdata) if event.xdata is not None else None
        y = int(event.ydata) if event.ydata is not None else None
        
        if x is None or y is None:
            return
            
        # Determine which canvas was clicked
        if event.canvas == self.axial_canvas:
            self.sagittal_index = y
            self.coronal_index = x
            self.axial_crosshair = (x, y)
            self.sagittal_slider.setValue(y)
            self.coronal_slider.setValue(x)
        elif event.canvas == self.sagittal_canvas:
            self.axial_index = y
            self.coronal_index = x
            self.sagittal_crosshair = (x, y)
            self.axial_slider.setValue(y)
            self.coronal_slider.setValue(x)
        elif event.canvas == self.coronal_canvas:
            self.sagittal_index = x
            self.axial_index = y
            self.coronal_crosshair = (x, y)
            self.sagittal_slider.setValue(x)
            self.axial_slider.setValue(y)
        self.update_views()

    def on_mouse_press(self, event):
        """Handle mouse press events."""
        if event.button == 1:  # Left mouse button
            self.is_mouse_pressed = True
            if self.current_mode == self.ZOOM_MODE and self.zoom_mode:
                self.perform_zoom(event.canvas, event.xdata, event.ydata)
            elif self.current_mode == self.CURSOR_MODE:
                self.handle_cursor_motion(event)
    def on_mouse_release(self, event):
        """Handle mouse release events."""
        if event.button == 1:  # Left mouse button
            self.is_mouse_pressed = False

    def on_mouse_motion(self, event):
        """Handle mouse motion events."""
        if self.is_mouse_pressed and self.current_mode == self.CURSOR_MODE:
            self.handle_cursor_motion(event)   

    def upload_nifti_folder(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select NIfTI File", "", "NIfTI Files (*.nii *.nii.gz)")
        if file_path:
            self.load_nifti_file(file_path)

    def load_nifti_file(self, file_path):
        nifti_img = nib.load(file_path)
        self.image_volume = nifti_img.get_fdata()
        self.image_volume = np.transpose(self.image_volume, (2, 0, 1))  # Ensure slices are in the right order

        # Set initial indices and update GUI
        self.axial_index = self.image_volume.shape[0] // 2
        self.sagittal_index = self.image_volume.shape[1] // 2
        self.coronal_index = self.image_volume.shape[2] // 2

        self.axial_slider.setRange(0, self.image_volume.shape[0] - 1)
        self.sagittal_slider.setRange(0, self.image_volume.shape[1] - 1)
        self.coronal_slider.setRange(0, self.image_volume.shape[2] - 1)

        self.axial_slider.setValue(self.axial_index)
        self.sagittal_slider.setValue(self.sagittal_index)
        self.coronal_slider.setValue(self.coronal_index)

        self.show_views() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MedicalImageViewer()
    viewer.show()
    sys.exit(app.exec_())