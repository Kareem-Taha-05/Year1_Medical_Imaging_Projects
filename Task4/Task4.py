import sys
import random
import pydicom
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QGraphicsPixmapItem, 
    QTextEdit, QLineEdit, QWidget, QTabWidget, QSplitter, QInputDialog , QTableWidget , QTableWidgetItem , QHeaderView , QScrollArea , QSizePolicy ,QGridLayout  , QGraphicsView , QGraphicsScene
)
from PyQt5.QtCore import Qt, QTimer , QEvent 
from PyQt5.QtGui import QPixmap, QImage , QPainter
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from pydicom.multival import MultiValue

class DicomViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Viewer")
        self.setGeometry(100, 100, 1200, 800)
        
        self.dicom_file = None
        self.m2d_frames = []                                                        
        self.m2d_timer = QTimer()
        self.m2d_index = 0

        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()

        # Tabs for different functionalities
        self.image_tab = QWidget()
        self.metadata_tab = QWidget()
        self.three_d_tab = QWidget()

        self.tabs.addTab(self.image_tab, "Image Viewer")
        self.tabs.addTab(self.metadata_tab, "Metadata Viewer")
        self.tabs.addTab(self.three_d_tab, "3D Viewer")

        self.init_image_tab()
        self.init_metadata_tab()
        self.init_three_d_tab()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_image_tab(self):
        layout = QVBoxLayout()

        # Buttons for actions
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load DICOM File")
        self.load_button.clicked.connect(self.load_dicom_file)

        self.show_image_button = QPushButton("Show Image")
        self.show_image_button.clicked.connect(self.display_image)
        self.show_image_button.setEnabled(False)

        self.stop_video_button = QPushButton("Stop Video (M2D)")
        self.stop_video_button.clicked.connect(self.stop_video)
        self.stop_video_button.setEnabled(False)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.show_image_button)
        button_layout.addWidget(self.stop_video_button)

        # Image Display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        self.image_label.setFixedSize(500, 500)  # Set a fixed size for the video area
        self.image_label.setScaledContents(False)  # Prevent the video from scaling to fit the label

        layout.addLayout(button_layout)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)  # Center the label in the layout

        self.image_tab.setLayout(layout)


    def init_metadata_tab(self):
        layout = QVBoxLayout()

        # Buttons for metadata and search
        button_layout = QHBoxLayout()
        self.show_tags_button = QPushButton("Show All Tags")
        self.show_tags_button.clicked.connect(self.display_dicom_tags)
        self.show_tags_button.setEnabled(False)

        self.patient_button = QPushButton("Patient Info")
        self.patient_button.clicked.connect(self.display_patient_info)
        self.patient_button.setEnabled(False)

        self.pixel_button = QPushButton("Pixel Data")
        self.pixel_button.clicked.connect(self.display_pixel_data)
        self.pixel_button.setEnabled(False)

        self.study_button = QPushButton("Study Info")
        self.study_button.clicked.connect(self.display_study_info)
        self.study_button.setEnabled(False)

        self.modality_button = QPushButton("Modality Info")
        self.modality_button.clicked.connect(self.display_modality_info)
        self.modality_button.setEnabled(False)

        self.physician_button = QPushButton("Physician Info")  # New button
        self.physician_button.clicked.connect(self.display_physician_info)
        self.physician_button.setEnabled(False)

        self.image_button = QPushButton("Image Info")  # New button
        self.image_button.clicked.connect(self.display_image_info)
        self.image_button.setEnabled(False)

        self.anonymize_button = QPushButton("Anonymize DICOM")  # New button
        self.anonymize_button.clicked.connect(self.anonymize_dicom)
        self.anonymize_button.setEnabled(False)

        button_layout.addWidget(self.show_tags_button)
        button_layout.addWidget(self.patient_button)
        button_layout.addWidget(self.pixel_button)
        button_layout.addWidget(self.study_button)
        button_layout.addWidget(self.modality_button)
        button_layout.addWidget(self.physician_button)
        button_layout.addWidget(self.image_button)
        button_layout.addWidget(self.anonymize_button)

        
        # Search area
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search for DICOM Tag")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_dicom_tag)
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_button)

        layout.addLayout(button_layout)
        layout.addLayout(search_layout)
        

        self.metadata_tab.setLayout(layout)
            # Table for metadata display
        self.metadata_table = QTableWidget()
        self.metadata_table.setColumnCount(3)
        self.metadata_table.setHorizontalHeaderLabels(["Tag", "Name", "Value"])
        self.metadata_table.horizontalHeader().setStretchLastSection(True)
        self.metadata_table.horizontalHeader().setSectionResizeMode(0, 1)  # Adjust column sizes
        self.metadata_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)  # Adjust "Tag" column
        self.metadata_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)  # Allow resizing for "Name"
        self.metadata_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)  # Stretch "Value" column

        # Set a fixed initial width for the "Name" column
        self.metadata_table.setColumnWidth(1, 300)  # Adjust the width as needed

        layout.addLayout(button_layout)
        layout.addWidget(self.metadata_table)

        self.metadata_tab.setLayout(layout)

        self.metadata_display = QTextEdit(self)
        layout.addWidget(self.metadata_display)


    def init_three_d_tab(self):
        layout = QVBoxLayout()
        instruction_label = QLabel("3D DICOM Viewer")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Graphics View and Scene for Zoomable Display
        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        
        # Buttons for zoom controls
        zoom_layout = QHBoxLayout()
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(lambda: self.graphics_view.scale(1.2, 1.2))  # Zoom in by 20%

        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(lambda: self.graphics_view.scale(0.8, 0.8))  # Zoom out by 20%

        zoom_layout.addWidget(self.zoom_in_button)
        zoom_layout.addWidget(self.zoom_out_button)

        # Display Tiles Button
        self.display_tiles_button = QPushButton("Display 3D as Tiles")
        self.display_tiles_button.clicked.connect(self.display_3d_tiles)

        layout.addWidget(instruction_label)
        layout.addWidget(self.display_tiles_button)
        layout.addLayout(zoom_layout)
        layout.addWidget(self.graphics_view)

        self.three_d_tab.setLayout(layout)


    def load_dicom_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select DICOM File", "", "DICOM Files (*.dcm)")
        if file_path:
            self.dicom_file = pydicom.dcmread(file_path)
            self.show_image_button.setEnabled(True)
            self.show_tags_button.setEnabled(True)
            self.patient_button.setEnabled(True)
            self.pixel_button.setEnabled(True)
            self.study_button.setEnabled(True)
            self.modality_button.setEnabled(True)
            self.physician_button.setEnabled(True)
            self.image_button.setEnabled(True)
            self.anonymize_button.setEnabled(True)
    
            # Check for M2D and prepare frames
            if hasattr(self.dicom_file, "NumberOfFrames"):
                self.m2d_frames = [self.dicom_file.pixel_array[i] for i in range(self.dicom_file.NumberOfFrames)]
                self.metadata_display.append(f"Loaded an M2D file with {len(self.m2d_frames)} frames.")
            else:
                self.metadata_display.append("DICOM file loaded successfully.")
        else:
            self.metadata_display.append("No file selected.")


    def display_image(self):
        if not hasattr(self.dicom_file, "pixel_array"):
            self.metadata_display.append("No image data found in the DICOM file.")
            return

        if hasattr(self.dicom_file, "NumberOfFrames"):  # M2D - play video
            self.m2d_index = 0
            self.stop_video_button.setEnabled(True)

            # Safely disconnect any existing connections
            try:
                self.m2d_timer.timeout.disconnect(self.play_m2d_video)
            except TypeError:
                pass  # No connection exists, so nothing to disconnect

            # Reconnect and start the timer
            self.m2d_timer.timeout.connect(self.play_m2d_video)
            self.m2d_timer.start(100)  # Set the frame interval in milliseconds
            self.metadata_display.append(f"Playing M2D video with {len(self.m2d_frames)} frames.")
        else:  # 2D - show single image
            self.display_2d_image(self.dicom_file.pixel_array)




    def display_2d_image(self, pixel_array):
            try:
                # Handle DICOM-specific scaling (if applicable)
                if hasattr(self.dicom_file, "RescaleSlope") and hasattr(self.dicom_file, "RescaleIntercept"):
                    slope = float(self.dicom_file.RescaleSlope)
                    intercept = float(self.dicom_file.RescaleIntercept)
                    pixel_array = (pixel_array * slope + intercept).astype(np.float32)

                # Normalize the pixel array to 8-bit range (0-255)
                pixel_min = np.min(pixel_array)
                pixel_max = np.max(pixel_array)
                if pixel_max > pixel_min:  # Avoid division by zero
                    normalized_pixel_array = ((pixel_array - pixel_min) / (pixel_max - pixel_min) * 255).astype(np.uint8)
                else:
                    normalized_pixel_array = np.zeros_like(pixel_array, dtype=np.uint8)

                # Convert the NumPy array to QImage
                height, width = normalized_pixel_array.shape
                image = QImage(normalized_pixel_array.data, width, height, width, QImage.Format_Grayscale8)

                # Ensure the QImage is valid
                if image.isNull():
                    self.metadata_display.append("Failed to create QImage from pixel array.")
                    return

                # Set the image to the QLabel
                pixmap = QPixmap.fromImage(image)
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(True)  # Scale image to fit QLabel if needed
                self.metadata_display.append("DICOM image displayed successfully.")
            except Exception as e:
                self.metadata_display.append(f"Error displaying image: {e}")



    def play_m2d_video(self):
        if not self.m2d_frames or self.m2d_index >= len(self.m2d_frames):
            self.m2d_timer.stop()
            self.stop_video_button.setEnabled(False)
            return

        frame = self.m2d_frames[self.m2d_index]

        # Validate the frame
        if not isinstance(frame, np.ndarray):
            self.metadata_display.append(f"Frame at index {self.m2d_index} is not a valid NumPy array.")
            self.m2d_index += 1
            return

        try:
            # Convert color image to grayscale manually if needed
            if frame.ndim == 3 and frame.shape[2] == 3:
                # Using the standard grayscale formula: 0.2989 * R + 0.5870 * G + 0.1140 * B
                frame = (0.2989 * frame[:, :, 0] + 
                        0.5870 * frame[:, :, 1] + 
                        0.1140 * frame[:, :, 2]).astype(np.uint8)
            elif frame.ndim != 2:
                self.metadata_display.append(f"Frame at index {self.m2d_index} has unsupported shape: {frame.shape}")
                self.m2d_index += 1
                return

            # Normalize the frame for display
            if np.ptp(frame) == 0:
                normalized = (frame - np.min(frame)).astype(np.uint8)
            else:
                normalized = (255.0 * (frame - np.min(frame)) / np.ptp(frame)).astype(np.uint8)

            # Create QImage
            height, width = normalized.shape
            image = QImage(normalized.data, width, height, width, QImage.Format_Grayscale8)
            if image.isNull():
                self.metadata_display.append(f"Failed to create QImage for frame at index {self.m2d_index}.")
                self.m2d_index += 1
                return

            # Update QLabel
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

        except Exception as e:
            self.metadata_display.append(f"Error processing frame at index {self.m2d_index}: {e}")

        # Increment the frame index
        self.m2d_index += 1





    def stop_video(self):
        self.m2d_timer.stop()
        try:
            self.m2d_timer.timeout.disconnect(self.play_m2d_video)  # Safely disconnect
        except TypeError:
            pass
        self.stop_video_button.setEnabled(False)

    def display_3d_tiles(self):
        if not self.dicom_file:
            self.metadata_display.append("No DICOM file loaded for tiles.")
            return

        try:
            if hasattr(self.dicom_file, "NumberOfFrames") and self.dicom_file.NumberOfFrames > 1:
                slices = [self.dicom_file.pixel_array[i] for i in range(self.dicom_file.NumberOfFrames)]
                data_type = "2D multi-frame"
            elif self.dicom_file.pixel_array.ndim == 3:
                slices = [self.dicom_file.pixel_array[i] for i in range(self.dicom_file.pixel_array.shape[0])]
                data_type = "3D"
            elif self.dicom_file.pixel_array.ndim == 2:
                slices = [self.dicom_file.pixel_array]
                data_type = "Single 2D image"
            else:
                self.metadata_display.append("Unsupported DICOM format. Could not determine data type.")
                return
        except AttributeError as e:
            self.metadata_display.append(f"Error reading pixel data: {str(e)}")
            return

        self.graphics_scene.clear()

        # Tile dimensions
        thumbnail_width = 100  # Width of each tile
        thumbnail_height = 100  # Height of each tile
        columns = 5
        padding = 20

        total_tiles = len(slices)
        rows = (total_tiles + columns - 1) // columns

        for i, slice_image in enumerate(slices):
            if slice_image.ndim > 2:
                slice_image = slice_image.squeeze()
            if slice_image.ndim != 2:
                self.metadata_display.append(f"Slice {i} has an unsupported shape: {slice_image.shape}. Skipping.")
                continue

            normalized = (255.0 * (slice_image - np.min(slice_image)) / np.ptp(slice_image)).astype(np.uint8)

            # Resize ignoring aspect ratio
            thumbnail = QImage(normalized.data, normalized.shape[1], normalized.shape[0],
                            normalized.shape[1], QImage.Format_Grayscale8).scaled(
                thumbnail_width, thumbnail_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )

            pixmap = QPixmap.fromImage(thumbnail)

            row, col = divmod(i, columns)
            x_pos = col * (thumbnail_width + padding)
            y_pos = row * (thumbnail_height + padding)

            item = QGraphicsPixmapItem(pixmap)
            item.setPos(x_pos, y_pos)
            item.setData(0, normalized)
            self.graphics_scene.addItem(item)

        # Update scene dimensions
        self.graphics_scene.setSceneRect(0, 0, columns * (thumbnail_width + padding), rows * (thumbnail_height + padding))

        self.graphics_view.resetTransform()
        self.graphics_view.fitInView(self.graphics_scene.sceneRect(), Qt.KeepAspectRatio)
        self.graphics_view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.metadata_display.append(f"Displayed {data_type} data with {len(slices)} tiles.")








    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel and source == self.graphics_view.viewport():
            # Adjust quality when zooming
            scale_factor = self.graphics_view.transform().m11()  # Get current scale
            for item, pixmap_high_res in self.slice_items:
                if scale_factor > 1.5:  # Threshold for replacing with high-res
                    item.setPixmap(pixmap_high_res)
                else:  # Use thumbnail for normal display
                    item.setPixmap(pixmap_high_res.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        return super().eventFilter(source, event)






    def display_dicom_tags(self):
        not_rendered = "Pixel Data"
        self.metadata_table.setRowCount(0)  # Clear existing rows

        for elem in self.dicom_file.iterall():
            if elem.name != not_rendered:
                # Add a new row to the table
                row_position = self.metadata_table.rowCount()
                self.metadata_table.insertRow(row_position)

                # Populate the row with tag, name, and value
                self.metadata_table.setItem(row_position, 0, QTableWidgetItem(str(elem.tag)))
                self.metadata_table.setItem(row_position, 1, QTableWidgetItem(elem.name))
                self.metadata_table.setItem(row_position, 2, QTableWidgetItem(str(elem.value)))

    def search_dicom_tag(self):
        search_term = self.search_box.text().strip().lower()
        self.metadata_table.setRowCount(0)  # Clear existing rows

        found = False
        for elem in self.dicom_file.iterall():
            if search_term in elem.name.lower():  # Search in the name of the tag
                row_position = self.metadata_table.rowCount()
                self.metadata_table.insertRow(row_position)  # Add a new row

                # Insert Tag, Name, and Value into respective columns
                self.metadata_table.setItem(row_position, 0, QTableWidgetItem(str(elem.tag)))
                self.metadata_table.setItem(row_position, 1, QTableWidgetItem(elem.name))
                self.metadata_table.setItem(row_position, 2, QTableWidgetItem(str(elem.value)))

                found = True

        if not found:
            self.metadata_table.setRowCount(1)  # Add a single row to display "not found" message
            self.metadata_table.setItem(0, 0, QTableWidgetItem("N/A"))
            self.metadata_table.setItem(0, 1, QTableWidgetItem("No matching tag found"))
            self.metadata_table.setItem(0, 2, QTableWidgetItem("N/A"))


    def display_patient_info(self):
        self.metadata_table.setRowCount(0)  # Clear existing rows

        # Patient information fields
        patient_info = [
            ("(0010,0010)", "Patient's Name", self.dicom_file.get('PatientName', 'N/A')),
            ("(0010,0020)", "Patient ID", self.dicom_file.get('PatientID', 'N/A')),
            ("(0010,0030)", "Patient's Birth Date", self.dicom_file.get('PatientBirthDate', 'N/A')),
            ("(0010,0040)", "Patient's Sex", self.dicom_file.get('PatientSex', 'N/A')),
        ]

        for tag, name, value in patient_info:
            row_position = self.metadata_table.rowCount()
            self.metadata_table.insertRow(row_position)

            # Convert non-string values to strings
            if not isinstance(value, str):
                value = str(value)

            self.metadata_table.setItem(row_position, 0, QTableWidgetItem(tag))
            self.metadata_table.setItem(row_position, 1, QTableWidgetItem(name))
            self.metadata_table.setItem(row_position, 2, QTableWidgetItem(value))


    def display_pixel_data(self):
        self.metadata_table.setRowCount(0)  # Clear existing rows

        # Display pixel data
        tag = "(7FE0,0010)"
        name = "Pixel Data"
        value = self.dicom_file.get('PixelData', 'N/A')

        # Handle 'bytes' or other non-string data types
        if isinstance(value, bytes):
            # Display a string indicating the size of the data (e.g., "Binary data: 1024 bytes")
            value = f"Binary data: {len(value)} bytes"
        elif not isinstance(value, str):
            # Convert any other type to string
            value = str(value)

        row_position = self.metadata_table.rowCount()
        self.metadata_table.insertRow(row_position)
        self.metadata_table.setItem(row_position, 0, QTableWidgetItem(tag))
        self.metadata_table.setItem(row_position, 1, QTableWidgetItem(name))
        self.metadata_table.setItem(row_position, 2, QTableWidgetItem(value))


    def display_study_info(self):
        self.metadata_table.setRowCount(0)  # Clear existing rows

        # Populate table with study info
        study_data = [
            ("(0020,0010)", "Study ID", self.dicom_file.get('StudyID', 'N/A')),
            ("(0008,0020)", "Study Date", self.dicom_file.get('StudyDate', 'N/A')),
        ]

        for tag, name, value in study_data:
            row_position = self.metadata_table.rowCount()
            self.metadata_table.insertRow(row_position)
            self.metadata_table.setItem(row_position, 0, QTableWidgetItem(tag))
            self.metadata_table.setItem(row_position, 1, QTableWidgetItem(name))
            self.metadata_table.setItem(row_position, 2, QTableWidgetItem(value))


    def display_modality_info(self):
        self.metadata_table.setRowCount(0)  # Clear existing rows

        # Display modality info
        tag = "(0008,0060)"
        name = "Modality"
        value = self.dicom_file.get('Modality', 'N/A')

        row_position = self.metadata_table.rowCount()
        self.metadata_table.insertRow(row_position)
        self.metadata_table.setItem(row_position, 0, QTableWidgetItem(tag))
        self.metadata_table.setItem(row_position, 1, QTableWidgetItem(name))
        self.metadata_table.setItem(row_position, 2, QTableWidgetItem(value))


    def display_physician_info(self):
        self.metadata_table.setRowCount(0)  # Clear existing rows

        # Populate table with physician info
        physician_data = [
            ("(0008,0090)", "Physician Name", self.dicom_file.get('PhysicianName', 'N/A')),
            ("(0008,1048)", "Physician ID", self.dicom_file.get('PhysicianID', 'N/A')),
        ]

        for tag, name, value in physician_data:
            row_position = self.metadata_table.rowCount()
            self.metadata_table.insertRow(row_position)
            self.metadata_table.setItem(row_position, 0, QTableWidgetItem(tag))
            self.metadata_table.setItem(row_position, 1, QTableWidgetItem(name))
            self.metadata_table.setItem(row_position, 2, QTableWidgetItem(value))


    def display_image_info(self):
        self.metadata_table.setRowCount(0)  # Clear existing rows

        # Populate table with image info
        image_data = [
            ("(0008,0008)", "Image Type", self.dicom_file.get('ImageType', 'N/A')),
            ("(0028,0010)", "Rows", self.dicom_file.get('Rows', 'N/A')),
            ("(0028,0011)", "Columns", self.dicom_file.get('Columns', 'N/A')),
        ]

        for tag, name, value in image_data:
            # Convert value to a string if it's not a string
            if isinstance(value, bytes):
                value = value.decode('utf-8', errors='ignore')  # Decode bytes to string
            elif not isinstance(value, str):
                value = str(value)  # Convert other types (e.g., numbers, lists) to string

            row_position = self.metadata_table.rowCount()
            self.metadata_table.insertRow(row_position)
            self.metadata_table.setItem(row_position, 0, QTableWidgetItem(tag))
            self.metadata_table.setItem(row_position, 1, QTableWidgetItem(name))
            self.metadata_table.setItem(row_position, 2, QTableWidgetItem(value))



    
    def anonymize_dicom(self):
        # Ask user for a prefix to anonymize the fields
        prefix, ok = QInputDialog.getText(self, "Enter Prefix", "Enter the prefix for anonymization:")
        if ok and prefix:
            # Anonymizing sensitive fields
            self.dicom_file.PatientName = f"{prefix}_Patient"
            self.dicom_file.PatientID = f"{prefix}_ID"
            self.dicom_file.StudyID = f"{prefix}_Study"
            self.dicom_file.PatientBirthDate = f"{prefix}_BirthDate"
            self.dicom_file.PatientSex = "O"  # Replace gender with 'O' for other/unknown

            # Save the anonymized DICOM file
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Anonymized DICOM File", "", "DICOM Files (*.dcm)")
            if save_path:
                self.dicom_file.save_as(save_path)
                self.metadata_display.append(f"DICOM file anonymized and saved as {save_path}")
            else:
                self.metadata_display.append("Anonymization cancelled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DicomViewer()
    viewer.show()
    sys.exit(app.exec_())

