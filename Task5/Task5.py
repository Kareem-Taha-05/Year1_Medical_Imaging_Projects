import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QScrollArea,
    QMenu, QLineEdit, QSlider, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect
from matplotlib.backend_bases import FigureCanvasBase
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pydicom
import numpy as np
import cv2

class AnalysisLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom_factor = 1.0 
        self.original_pixmap = None
        self.base_pixmap = None
        self.analysis_type = None
        self.snr_callback = None
        self.is_main_image = False
        self.setAlignment(Qt.AlignCenter)
        # Add viewport-specific settings
        self.contrast_value = 0
        self.brightness_value = 0  # Add brightness value
        self.resolution_scale = 1.0
        self.needs_resolution_update = False
        self.interpolation_mode = "Bilinear Interpolation"

    def set_original_pixmap(self, pixmap):
        # Store both original and base pixmaps
        self.original_pixmap = pixmap
        self.base_pixmap = pixmap.copy()
        self.update_display()

    def update_display(self):
        if self.base_pixmap and hasattr(self, 'numpy_image'):
            # Get original image dimensions
            height, width = self.numpy_image.shape
            
            # Calculate new dimensions based on zoom factor
            new_width = int(width * self.zoom_factor)
            new_height = int(height * self.zoom_factor)

            # Choose interpolation method based on mode
            if self.interpolation_mode == "Nearest-Neighbor":
                interpolation = cv2.INTER_NEAREST
            elif self.interpolation_mode == "Linear Interpolation":
                interpolation = cv2.INTER_LINEAR
            elif self.interpolation_mode == "Bilinear Interpolation":
                interpolation = cv2.INTER_LINEAR
            elif self.interpolation_mode == "Cubic Interpolation":
                interpolation = cv2.INTER_CUBIC
            else:
                interpolation = cv2.INTER_LINEAR  # Default to bilinear

            # Resize the image using the selected interpolation method
            resized_image = cv2.resize(
                self.numpy_image,
                (new_width, new_height),
                interpolation=interpolation
            )

            # Convert back to QPixmap
            height, width = resized_image.shape
            q_image = QImage(resized_image.data, width, height, width, QImage.Format_Grayscale8)
            zoomed_pixmap = QPixmap.fromImage(q_image)

            # Set the zoomed pixmap
            self.setPixmap(zoomed_pixmap)

            # Update minimum size to accommodate zoomed image
            self.setMinimumSize(zoomed_pixmap.size())

            # Adjust scroll area if needed
            scroll_area = self.parent().parent()
            if isinstance(scroll_area, QScrollArea):
                scroll_area.setWidgetResizable(True)

    def apply_zoom_mode(self, mode):
        # Store the interpolation mode
        self.interpolation_mode = mode
        # Update the display with new interpolation mode
        self.update_display()
    
    def update_zoom(self):
        self.update_display()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Only adjust to fit window if not zoomed
        if self.zoom_factor == 1.0:
            self.update_pixmap_size()

    def update_pixmap_size(self):
        if self.base_pixmap and self.zoom_factor == 1.0:
            scroll_area = self.parent().parent()
            if isinstance(scroll_area, QScrollArea):
                viewport_size = scroll_area.viewport().size()
                scaled_pixmap = self.base_pixmap.scaled(
                    viewport_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):  # Update in AnalysisLabel class
        try:
            # Check if all required attributes are initialized
            if not (self.original_pixmap and self.analysis_type and self.snr_callback):
                print("Essential attributes are missing or not set.")
                return

            # Get the current pixmap and ensure it exists
            current_pixmap = self.pixmap()
            if current_pixmap is None:
                print("Current pixmap is None.")
                return

            # Calculate scaling factors
            if self.original_pixmap.width() == 0 or self.original_pixmap.height() == 0:
                print("Original pixmap dimensions are zero.")
                return

            scale_x = current_pixmap.width() / self.original_pixmap.width()
            scale_y = current_pixmap.height() / self.original_pixmap.height()

            # Get mouse position and check if it's within the pixmap's bounds
            pos = event.pos()
            label_rect = self.rect()
            pixmap_rect = current_pixmap.rect()

            if not pixmap_rect.contains(pos):
                print("Mouse click is outside the valid pixmap area.")
                return

            # Calculate the mouse position relative to the pixmap
            x_offset = (label_rect.width() - pixmap_rect.width()) // 2
            y_offset = (label_rect.height() - pixmap_rect.height()) // 2
            x = (pos.x() - x_offset) / scale_x
            y = (pos.y() - y_offset) / scale_y

            # Validate `self.numpy_image`
            if self.numpy_image is None:
                print("numpy_image is not set.")
                return

            img_height, img_width = self.numpy_image.shape
            box_size = 30

            # Clamp coordinates to valid ranges
            box_x = max(0, min(int(x), img_width - 1))
            box_y = max(0, min(int(y), img_height - 1))

            box_x_start = max(0, box_y - box_size // 2)
            box_x_end = min(img_height, box_y + box_size // 2 + 1)
            box_y_start = max(0, box_x - box_size // 2)
            box_y_end = min(img_width, box_x + box_size // 2 + 1)

            # Extract data only if the region is valid
            if box_x_start < box_x_end and box_y_start < box_y_end:
                box_data = self.numpy_image[box_x_start:box_x_end, box_y_start:box_y_end]
                self.snr_callback(self.analysis_type, box_data)
            else:
                print("Invalid region for box data extraction.")

            # Draw a box on the pixmap
            pixmap_with_box = self.original_pixmap.copy()
            painter = QPainter(pixmap_with_box)
            pen = QPen(Qt.red if self.analysis_type == 'noise' else
                    Qt.green if self.analysis_type == 'signal1' else Qt.blue, 2)
            painter.setPen(pen)
            painter.drawRect(QRect(int(x - box_size // 2), int(y - box_size // 2), box_size, box_size))
            painter.end()

            # Update pixmap and refresh display
            self.original_pixmap = pixmap_with_box
            self.base_pixmap = pixmap_with_box.copy()
            self.update_pixmap_size()
            event.accept()
        except Exception as e:
            print(f"An error occurred: {e}")
            pass

    def mouseDoubleClickEvent(self, event):
        # When double-clicked, show the histogram of the image
        if hasattr(self, 'numpy_image'):
            # Get the main window instance
            main_window = self.window()
            if main_window:
                main_window.show_histogram(self.numpy_image, "Image Histogram")
        super().mouseDoubleClickEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Medical Image Editor")
        self.setGeometry(100, 100, 1400, 900)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Top toolbar layout
        self.toolbar_layout = QHBoxLayout()
        self.main_layout.addLayout(self.toolbar_layout)

        # Buttons setup
        self.setup_buttons()

        # SNR panel setup
        self.setup_snr_panel()
        self.setup_edit_panel()
        self.setup_zoom_panel()

        # Content layout
        self.setup_content_layout()

        # State variables
        self.dicom_image = None
        self.selected_viewport = None
        self.active_viewport = None
        self.noise_mean = None
        self.signal_mean = None
        self.noise_std = None
        self.signal1_mean = None
        self.signal2_mean = None

        # Sliders for contrast and resolution
        self.setup_sliders()

        #histogram intialization
        self.histogram_window = None
        self.setup_histogram_window()
    
    def setup_histogram_window(self):
        # Create a new window for the histogram
        self.histogram_window = QMainWindow(self)
        self.histogram_window.setWindowTitle("Histogram View")
        self.histogram_window.setGeometry(100, 100, 600, 400)
        
        # Create the main widget for the histogram window
        main_widget = QWidget()
        self.histogram_window.setCentralWidget(main_widget)
        
        # Create a vertical layout
        layout = QVBoxLayout(main_widget)
        
        # Create the matplotlib figure
        self.histogram_figure = Figure(figsize=(5, 4), dpi=100)
        self.histogram_canvas = FigureCanvas(self.histogram_figure)
        layout.addWidget(self.histogram_canvas)

    def show_histogram(self, image, title):
        if image is not None:
            # Clear the previous histogram
            self.histogram_figure.clear()
            
            # Create a new subplot
            ax = self.histogram_figure.add_subplot(111)
            
            # Calculate histogram using cv2
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            
            # Plot the histogram
            ax.plot(hist, color='blue')
            ax.set_title(title)
            ax.set_xlabel("Pixel Intensity")
            ax.set_ylabel("Frequency")
            ax.set_xlim([0, 256])
            
            # Add grid for better readability
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Calculate and display statistics
            mean_val = np.mean(image)
            std_val = np.std(image)
            median_val = np.median(image)
            
            stats_text = f'Mean: {mean_val:.2f}\nStd Dev: {std_val:.2f}\nMedian: {median_val:.2f}'
            ax.text(0.95, 0.95, stats_text,
                   transform=ax.transAxes,
                   verticalalignment='top',
                   horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Update the canvas
            self.histogram_canvas.draw()
            
            # Show the histogram window
            self.histogram_window.show()
            self.histogram_window.raise_()
        
    def setup_buttons(self):
        # Import button
        self.import_button = QPushButton("Import DICOM")
        self.import_button.clicked.connect(self.import_dicom)
        self.toolbar_layout.addWidget(self.import_button)

        # Edit button
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.toggle_edit_panel)
        self.toolbar_layout.addWidget(self.edit_button)

        # zoom button
        self.zoom_button = QPushButton("Zoom settings")
        self.zoom_button.clicked.connect(self.toggle_zoom_panel)
        self.toolbar_layout.addWidget(self.zoom_button)

        # SNR button
        self.snr_button = QPushButton("SNR/CNR")
        self.snr_button.clicked.connect(self.toggle_snr_panel)
        self.toolbar_layout.addWidget(self.snr_button)
       
        # Viewport selector
        self.view_selector_button = QPushButton("Select Viewport (None)")
        self.view_selector_menu = QMenu()
        self.view_selector_button.setMenu(self.view_selector_menu)
        self.toolbar_layout.addWidget(self.view_selector_button)

    def setup_zoom_panel(self):
            self.zoom_panel = QWidget()
            self.zoom_panel_layout = QHBoxLayout()
            self.zoom_panel.setLayout(self.zoom_panel_layout)
            self.main_layout.addWidget(self.zoom_panel)

            # Zoom in button
            self.zoom_in_button = QPushButton("Zoom In")
            self.zoom_in_button.clicked.connect(self.zoom_in)
            self.zoom_panel_layout.addWidget(self.zoom_in_button)

            # Zoom out button
            self.zoom_out_button = QPushButton("Zoom Out")
            self.zoom_out_button.clicked.connect(self.zoom_out)
            self.zoom_panel_layout.addWidget(self.zoom_out_button)

            # Zoom mode button and menu
            self.zoom_mode_button = QPushButton("Zoom mode")
            self.zoom_mode_menu = QMenu()
            self.zoom_mode_button.setMenu(self.zoom_mode_menu)
            
            # Add interpolation mode options
            self.selected_mode = "Bilinear Interpolation"  # Default mode
            modes = [
                "Nearest-Neighbor",
                "Linear Interpolation",
                "Bilinear Interpolation",
                "Cubic Interpolation"
            ]
            
            for mode in modes:
                action = self.zoom_mode_menu.addAction(mode)
                action.triggered.connect(lambda checked, m=mode: self.select_zoom_mode(m))
            
            self.zoom_panel_layout.addWidget(self.zoom_mode_button)

            # Add Apply Zoom Mode button
            self.apply_zoom_mode_button = QPushButton("Apply Zoom Mode")
            self.apply_zoom_mode_button.clicked.connect(self.apply_selected_zoom_mode)
            self.zoom_panel_layout.addWidget(self.apply_zoom_mode_button)

            self.zoom_panel.setVisible(False)
            
    def select_zoom_mode(self, mode):
        self.selected_mode = mode
        # Update button text to show selected mode
        self.zoom_mode_button.setText(f"Zoom mode: {mode}")

    def apply_selected_zoom_mode(self):
        if self.selected_viewport:
            self.selected_viewport.apply_zoom_mode(self.selected_mode)      

    def change_zoom_mode(self, mode):
        # This function now only updates the selected mode without applying it
        self.select_zoom_mode(mode)

    def zoom_in(self):
        if self.selected_viewport and self.selected_viewport.original_pixmap:
            self.selected_viewport.zoom_factor *= 1.2
            self.selected_viewport.update_zoom()

    def zoom_out(self):
        if self.selected_viewport and self.selected_viewport.original_pixmap:
            self.selected_viewport.zoom_factor /= 1.2
            self.selected_viewport.update_zoom()

    def update_zoom(self):
        if self.original_pixmap:
            # Calculate new size based on zoom factor
            new_size = self.original_pixmap.size() * self.zoom_factor
            scaled_pixmap = self.original_pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Set the new pixmap
            self.setPixmap(scaled_pixmap)

            # Adjust the position of the zoomed image
            self.setGeometry(QRect(self.zoom_center.x() - scaled_pixmap.width() // 2,
                                    self.zoom_center.y() - scaled_pixmap.height() // 2,
                                    scaled_pixmap.width(),
                                    scaled_pixmap.height()))

    def setup_snr_panel(self):
        # SNR panel
        self.snr_panel = QWidget()
        self.snr_panel_layout = QHBoxLayout()
        self.snr_panel.setLayout(self.snr_panel_layout)
        self.main_layout.addWidget(self.snr_panel)

        # Noise button
        self.noise_button = QPushButton("Noise")
        self.noise_button.clicked.connect(self.activate_noise_analysis)
        self.snr_panel_layout.addWidget(self.noise_button)

        # Signal buttons
        self.signal1_button = QPushButton("Signal 1")
        self.signal1_button.clicked.connect(lambda: self.activate_signal_analysis(1))
        self.snr_panel_layout.addWidget(self.signal1_button)

        self.signal2_button = QPushButton("Signal 2")
        self.signal2_button.clicked.connect(lambda: self.activate_signal_analysis(2))
        self.snr_panel_layout.addWidget(self.signal2_button)

        # Create a layout for displays
        self.displays_layout = QHBoxLayout()
        self.snr_panel_layout.addLayout(self.displays_layout)

        # SNR display
        self.snr_display = QLineEdit("SNR: N/A")
        self.snr_display.setReadOnly(True)
        self.snr_panel_layout.addWidget(self.snr_display)

        # CNR display
        self.cnr_display = QLineEdit("CNR: N/A")
        self.cnr_display.setReadOnly(True)
        self.displays_layout.addWidget(self.cnr_display)

        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_analysis_boxes)
        self.snr_panel_layout.addWidget(self.delete_button)

        # Hide SNR panel by default
        self.snr_panel.setVisible(False)
   
    def toggle_zoom_panel(self):
        self.zoom_panel.setVisible(not self.zoom_panel.isVisible())

    def setup_content_layout(self):
        # Content layout setup
        self.content_layout = QHBoxLayout()
        self.main_layout.addLayout(self.content_layout)

        # Left side
        self.left_layout = QVBoxLayout()
        self.content_layout.addLayout(self.left_layout, 1)

        # Custom labels with analysis capabilities
        self.image_label = AnalysisLabel("No DICOM loaded.")
        self.image_label.is_main_image = True
        self.top_right_panel = AnalysisLabel("Top Right Panel")
        self.bottom_right_panel = AnalysisLabel("Bottom Right Panel")

        # Setup viewport selection menu
        self.view_selector_menu.addAction("View1 (Top Right)", lambda: self.select_viewport("view1"))
        self.view_selector_menu.addAction("View2 (Bottom Right)", lambda: self.select_viewport("view2"))

        # Scroll areas
        self.left_scroll_area = QScrollArea()
        self.left_scroll_area.setWidgetResizable(True)
        self.left_scroll_area.setWidget(self.image_label)
        self.left_layout.addWidget(self.left_scroll_area)

        # Right side layout
        self.right_layout = QVBoxLayout()
        self.content_layout.addLayout(self.right_layout, 1)

        # Right scroll areas
        self.top_right_scroll_area = QScrollArea()
        self.top_right_scroll_area.setWidgetResizable(True)
        self.top_right_scroll_area.setWidget(self.top_right_panel)
        self.right_layout.addWidget(self.top_right_scroll_area)

        self.bottom_right_scroll_area = QScrollArea()
        self.bottom_right_scroll_area.setWidgetResizable(True)
        self.bottom_right_scroll_area.setWidget(self.bottom_right_panel)
        self.right_layout.addWidget(self.bottom_right_scroll_area)

    def setup_edit_panel(self):
        self.edit_panel = QWidget()
        self.edit_panel_layout = QHBoxLayout()
        self.edit_panel.setLayout(self.edit_panel_layout)
        self.main_layout.addWidget(self.edit_panel)

        # Original noise and filter buttons
        self.gaussian_noise_button = QPushButton("Gaussian Noise")
        self.edit_panel_layout.addWidget(self.gaussian_noise_button)
        self.gaussian_noise_button.clicked.connect(lambda: self.apply_effect('gaussian_noise'))

        self.gaussian_filter_button = QPushButton("Gaussian Filter")
        self.edit_panel_layout.addWidget(self.gaussian_filter_button)
        self.gaussian_filter_button.clicked.connect(lambda: self.apply_effect('gaussian_filter'))

        self.salt_papper_button = QPushButton("Salt and Pepper Noise")
        self.edit_panel_layout.addWidget(self.salt_papper_button)
        self.salt_papper_button.clicked.connect(lambda: self.apply_effect('salt_pepper'))

        self.median_filter_button = QPushButton("Median Filter")
        self.edit_panel_layout.addWidget(self.median_filter_button)
        self.median_filter_button.clicked.connect(lambda: self.apply_effect('median_filter'))

        # Add new contrast enhancement buttons
        self.hist_eq_button = QPushButton("Histogram Equalization")
        self.edit_panel_layout.addWidget(self.hist_eq_button)
        self.hist_eq_button.clicked.connect(self.apply_histogram_equalization)

        self.clahe_button = QPushButton("CLAHE")
        self.edit_panel_layout.addWidget(self.clahe_button)
        self.clahe_button.clicked.connect(self.apply_clahe)

        self.morph_enhance_button = QPushButton("Morphological Enhancement")
        self.edit_panel_layout.addWidget(self.morph_enhance_button)
        self.morph_enhance_button.clicked.connect(self.apply_morphological_enhancement)

        # Rest of your existing buttons...
        self.pink_noise_button = QPushButton("Pink Noise")
        self.edit_panel_layout.addWidget(self.pink_noise_button)
        self.pink_noise_button.clicked.connect(lambda: self.apply_effect('pink_noise'))

        self.pink_filter_button = QPushButton("Pink Filter")
        self.edit_panel_layout.addWidget(self.pink_filter_button)
        self.pink_filter_button.clicked.connect(lambda: self.apply_effect('pink_filter'))

        self.high_filter_button = QPushButton("High pass filter")
        self.edit_panel_layout.addWidget(self.high_filter_button)
        self.high_filter_button.clicked.connect(self.apply_high_filter)

        self.low_filter_button = QPushButton("Low pass filter")
        self.edit_panel_layout.addWidget(self.low_filter_button)
        self.low_filter_button.clicked.connect(self.apply_low_filter)

        # Hide edit panel by default
        self.edit_panel.setVisible(False)

    def apply_histogram_equalization(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'numpy_image'):
            try:
                # Get current image
                current_image = self.selected_viewport.numpy_image.copy()

                # Apply histogram equalization
                equalized = cv2.equalizeHist(current_image)

                # Update viewport
                q_image = QImage(equalized, equalized.shape[1], equalized.shape[0], 
                            QImage.Format_Grayscale8)
                self.selected_viewport.set_original_pixmap(QPixmap.fromImage(q_image))
                self.selected_viewport.numpy_image = equalized

            except Exception as e:
                print(f"Error in histogram equalization: {str(e)}")

    def apply_clahe(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'numpy_image'):
            try:
                # Get current image
                current_image = self.selected_viewport.numpy_image.copy()

                # Create CLAHE object
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                
                # Apply CLAHE
                enhanced = clahe.apply(current_image)

                # Update viewport
                q_image = QImage(enhanced, enhanced.shape[1], enhanced.shape[0], 
                            QImage.Format_Grayscale8)
                self.selected_viewport.set_original_pixmap(QPixmap.fromImage(q_image))
                self.selected_viewport.numpy_image = enhanced

            except Exception as e:
                print(f"Error in CLAHE enhancement: {str(e)}")

    def apply_morphological_enhancement(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'numpy_image'):
            try:
                # Get current image
                current_image = self.selected_viewport.numpy_image.copy()

                # Create structuring elements of different sizes
                kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                kernel_medium = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

                # Apply top-hat transform (original - opening)
                # This enhances bright details
                tophat = cv2.morphologyEx(current_image, cv2.MORPH_TOPHAT, kernel_small)

                # Apply black-hat transform (closing - original)
                # This enhances dark details
                blackhat = cv2.morphologyEx(current_image, cv2.MORPH_BLACKHAT, kernel_small)

                # Enhance edges using morphological gradient
                gradient = cv2.morphologyEx(current_image, cv2.MORPH_GRADIENT, kernel_medium)

                # Combine the enhancements
                # Add bright details and dark details back to the original image
                enhanced = cv2.add(current_image, tophat)
                enhanced = cv2.subtract(enhanced, blackhat)

                # Blend with gradient for edge enhancement
                alpha = 0.2  # Weight for gradient contribution
                enhanced = cv2.addWeighted(enhanced, 1.0, gradient, alpha, 0)

                # Normalize the result
                enhanced = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX)
                enhanced = enhanced.astype(np.uint8)

                # Update viewport
                q_image = QImage(enhanced, enhanced.shape[1], enhanced.shape[0], 
                            QImage.Format_Grayscale8)
                self.selected_viewport.set_original_pixmap(QPixmap.fromImage(q_image))
                self.selected_viewport.numpy_image = enhanced

            except Exception as e:
                print(f"Error in morphological enhancement: {str(e)}")

    def apply_effect(self, effect_type, params=None):
        """Unified function to apply various effects to images."""
        if not (self.selected_viewport and hasattr(self.selected_viewport, 'numpy_image')):
            return

        img = self.selected_viewport.numpy_image.copy()
        if not isinstance(img, np.ndarray):
            return

        try:
            # Default parameters
            params = params or {}
            
            effects = {
                'gaussian_noise': lambda: np.clip(
                    img + np.random.normal(0, params.get('std', 15), img.shape), 0, 255
                ).astype(np.uint8),
                
                'gaussian_filter': lambda: cv2.GaussianBlur(
                    img, params.get('ksize', (3, 3)), params.get('sigma', 0.7)
                ),
                
                'salt_pepper': lambda: self._apply_salt_pepper(
                    img, params.get('density', 0.02)
                ),
                
                'median_filter': lambda: cv2.medianBlur(
                    img, params.get('ksize', 3)
                ),
                
                'pink_noise': lambda: self._apply_pink_noise(
                    img, params.get('intensity', 0.3)
                ),
                
                'pink_filter': lambda: self._apply_pink_filter(
                    img, params.get('alpha', 0.3)
                )
            }

            if effect_type in effects:
                processed = effects[effect_type]()
                self._update_image(processed)

        except Exception as e:
            print(f"Error applying {effect_type}: {e}")

    def _apply_salt_pepper(self, img, density):
        """Helper for salt and pepper noise."""
        noisy = img.copy()
        num_salt = int(img.size * density / 2)
        coords = [np.random.randint(0, i, num_salt) for i in img.shape]
        noisy[tuple(coords)] = 255
        coords = [np.random.randint(0, i, num_salt) for i in img.shape]
        noisy[tuple(coords)] = 0
        return noisy

    def _apply_pink_noise(self, img, intensity):
        """Helper for pink noise."""
        rows, cols = img.shape
        f = np.fft.fftfreq
        fx, fy = np.meshgrid(f(cols), f(rows))
        freq = np.sqrt(fx**2 + fy**2)
        freq[freq == 0] = 1e-10
        
        pink = (1.0 / np.sqrt(freq)) / np.max(1.0 / np.sqrt(freq))
        noise = np.real(np.fft.ifft2(pink * np.exp(1j * np.random.uniform(0, 2*np.pi, (rows, cols)))))
        noise = (noise - noise.mean()) / noise.std() * (img.std() * intensity)
        
        return np.clip(img + noise, 0, 255).astype(np.uint8)

    def _apply_pink_filter(self, img, alpha):
        """Helper for pink filter."""
        rows, cols = img.shape
        u = np.fft.fftfreq(rows).reshape(-1, 1)
        v = np.fft.fftfreq(cols)
        dist = np.sqrt(u**2 + v**2)
        dist[0, 0] = 1e-6
        
        f_transform = cv2.dft(img.astype(np.float32), flags=cv2.DFT_COMPLEX_OUTPUT)
        pink_filter = ((1.0 / np.sqrt(dist)) / np.sqrt(dist).max())[:, :, np.newaxis]
        filtered = cv2.idft(f_transform * pink_filter, flags=cv2.DFT_SCALE)
        filtered = cv2.magnitude(filtered[:, :, 0], filtered[:, :, 1])
        
        filtered = (filtered - filtered.mean()) * img.std() / (filtered.std() + 1e-6) + img.mean()
        filtered = np.clip(filtered, 0, 255).astype(np.uint8)
        
        return cv2.addWeighted(img, 1-alpha, filtered, alpha, 0)

    def _update_image(self, img):
        """Helper to update the viewport."""
        qimg = QImage(img, img.shape[1], img.shape[0], QImage.Format_Grayscale8)
        self.selected_viewport.set_original_pixmap(QPixmap.fromImage(qimg))
        self.selected_viewport.numpy_image = img

    def apply_high_filter(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'numpy_image'):
            try:
                # Get current image
                current_image = self.selected_viewport.numpy_image.copy()

                # Convert to float for processing
                image_float = current_image.astype(np.float32)

                # Apply Fourier Transform
                f_transform = np.fft.fft2(image_float)
                f_transform_shifted = np.fft.fftshift(f_transform)

                # Get dimensions
                rows, cols = image_float.shape
                center_row, center_col = rows // 2, cols // 2

                # Initialize or update filter parameters
                if not hasattr(self.selected_viewport, 'high_pass_radius'):
                    self.selected_viewport.high_pass_radius = min(rows, cols) * 0.1  # Start with 10% cutoff
                    self.selected_viewport.high_pass_strength = 0.3  # Initial strength
                    self.selected_viewport.blend_factor = 0.1  # Initial blend factor
                else:
                    # Gradually increase the effect while maintaining image quality
                    self.selected_viewport.high_pass_radius = min(
                        min(rows, cols) * 0.5,  # Maximum 50% cutoff
                        self.selected_viewport.high_pass_radius * 1.2  # 20% increase per click
                    )
                    self.selected_viewport.blend_factor = min(0.7, self.selected_viewport.blend_factor + 0.05)  # Gradually increase blend factor

                # Create frequency grid
                y, x = np.ogrid[-center_row:rows-center_row, -center_col:cols-center_col]
                d = np.sqrt(x * x + y * y)

                # Create Butterworth high-pass filter (smoother transition than ideal filter)
                n = 2  # Filter order
                cutoff = self.selected_viewport.high_pass_radius
                h = 1 / (1 + (cutoff / (d + 1e-6)) ** (2 * n))

                # Apply filter
                f_transform_shifted_filtered = f_transform_shifted * h

                # Inverse FFT
                f_transform_filtered = np.fft.ifftshift(f_transform_shifted_filtered)
                filtered_image = np.real(np.fft.ifft2(f_transform_filtered))

                # Normalize and blend
                filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX)
                filtered_image = filtered_image.astype(np.uint8)

                # Blend with original image for natural look
                blended_image = cv2.addWeighted(
                    current_image, 1 - self.selected_viewport.blend_factor,
                    filtered_image, self.selected_viewport.blend_factor,
                    0
                )

                # Update viewport
                q_image = QImage(blended_image, blended_image.shape[1], blended_image.shape[0],
                                QImage.Format_Grayscale8)
                self.selected_viewport.set_original_pixmap(QPixmap.fromImage(q_image))
                self.selected_viewport.numpy_image = blended_image

            except Exception as e:
                print(f"Error in apply_high_filter: {str(e)}")

    def apply_low_filter(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'numpy_image'):
            try:
                # Get current image
                current_image = self.selected_viewport.numpy_image.copy()
                
                # Convert to float for processing
                image_float = current_image.astype(np.float32)
                
                # Apply Fourier Transform
                f_transform = np.fft.fft2(image_float)
                f_transform_shifted = np.fft.fftshift(f_transform)
                
                # Get dimensions
                rows, cols = image_float.shape
                center_row, center_col = rows // 2, cols // 2
                
                # Initialize or update filter parameters with more conservative values
                if not hasattr(self.selected_viewport, 'low_pass_radius'):
                    self.selected_viewport.low_pass_radius = min(rows, cols) * 0.5  # Start with 50% cutoff
                else:
                    # Gradually decrease the cutoff frequency
                    self.selected_viewport.low_pass_radius = max(
                        min(rows, cols) * 0.1,  # Minimum 10% cutoff
                        self.selected_viewport.low_pass_radius * 0.8  # 20% decrease per click
                    )
                
                # Create frequency grid
                y, x = np.ogrid[-center_row:rows-center_row, -center_col:cols-center_col]
                d = np.sqrt(x*x + y*y)
                
                # Create ideal low-pass filter with smooth transition
                cutoff = self.selected_viewport.low_pass_radius
                # Use ideal low-pass filter with smooth transition
                h = 1 / (1 + (d / cutoff)**(2*2))  # Order of 2 for smooth transition
                
                # Apply filter
                f_transform_shifted_filtered = f_transform_shifted * h
                
                # Inverse FFT
                f_transform_filtered = np.fft.ifftshift(f_transform_shifted_filtered)
                filtered_image = np.real(np.fft.ifft2(f_transform_filtered))
                
                # Normalize to maintain proper intensity range
                filtered_image = filtered_image - filtered_image.min()
                filtered_image = filtered_image * (255.0 / filtered_image.max())
                filtered_image = filtered_image.astype(np.uint8)
                
                # Apply subtle Gaussian blur to reduce any ringing artifacts
                filtered_image = cv2.GaussianBlur(filtered_image, (3, 3), 0.5)
                
                # Update viewport
                q_image = QImage(filtered_image, filtered_image.shape[1], filtered_image.shape[0], 
                            QImage.Format_Grayscale8)
                self.selected_viewport.set_original_pixmap(QPixmap.fromImage(q_image))
                self.selected_viewport.numpy_image = filtered_image
                
            except Exception as e:
                print(f"Error in apply_low_filter: {str(e)}")

    def setup_sliders(self):
        # Create a horizontal layout for sliders
        self.slider_layout = QHBoxLayout()
        self.main_layout.addLayout(self.slider_layout)

        # Create sliders for contrast, brightness, and resolution
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-100, 100)  # Range for contrast adjustment
        self.contrast_slider.setValue(0)  # Default value
        self.contrast_slider.setTickPosition(QSlider.TicksBelow)
        self.contrast_slider.setTickInterval(10)
        self.slider_layout.addWidget(QLabel("Contrast"))
        self.slider_layout.addWidget(self.contrast_slider)

        # Add brightness slider
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)  # Range for brightness adjustment
        self.brightness_slider.setValue(0)  # Default value
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.setTickInterval(10)
        self.slider_layout.addWidget(QLabel("Brightness"))
        self.slider_layout.addWidget(self.brightness_slider)

        self.resolution_slider = QSlider(Qt.Horizontal)
        self.resolution_slider.setRange(5, 100)  # Range from 5% to 100% resolution
        self.resolution_slider.setValue(100)  # Start at maximum resolution
        self.resolution_slider.setTickPosition(QSlider.TicksBelow)
        self.resolution_slider.setTickInterval(5)
        self.slider_layout.addWidget(QLabel("Resolution"))
        self.slider_layout.addWidget(self.resolution_slider)

        # Connect slider value changes to their respective functions
        self.contrast_slider.valueChanged.connect(self.apply_contrast)
        self.brightness_slider.valueChanged.connect(self.apply_brightness)
        self.resolution_slider.sliderPressed.connect(self.resolution_slider_pressed)
        self.resolution_slider.sliderReleased.connect(self.resolution_slider_released)

    def apply_brightness(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'original_numpy_image'):
            # Store brightness value in viewport
            self.selected_viewport.brightness_value = self.brightness_slider.value() / 100.0
            
            # Start with original image
            adjusted_image = self.selected_viewport.original_numpy_image.copy()
            
            # Apply brightness
            adjusted_image = self.adjust_brightness(adjusted_image, self.selected_viewport.brightness_value)
            
            # Apply contrast if needed
            if self.selected_viewport.contrast_value != 0:
                adjusted_image = self.adjust_contrast(adjusted_image, self.selected_viewport.contrast_value)
            
            # Apply resolution scaling if needed
            if self.selected_viewport.resolution_scale < 0.99:
                adjusted_image = self.adjust_resolution(adjusted_image, self.selected_viewport.resolution_scale)
            
            # Update display
            q_image = QImage(adjusted_image, adjusted_image.shape[1], adjusted_image.shape[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.selected_viewport.set_original_pixmap(pixmap)
            self.selected_viewport.numpy_image = adjusted_image

    def adjust_brightness(self, image, brightness_value):
        # Convert to float for processing
        image_float = image.astype(np.float32)
        
        # Apply brightness adjustment
        if brightness_value >= 0:
            # For positive brightness: add value
            adjusted = image_float + (brightness_value * 127.5)  # Max brightness adds half the possible range
        else:
            # For negative brightness: subtract value
            adjusted = image_float - (abs(brightness_value) * 127.5)
        
        # Ensure values stay within valid range
        adjusted = np.clip(adjusted, 0, 255)
        return adjusted.astype(np.uint8)

    def resolution_slider_pressed(self):
        if self.selected_viewport:
            self.selected_viewport.needs_resolution_update = True

    def resolution_slider_released(self):
        if self.selected_viewport and self.selected_viewport.needs_resolution_update:
            self.apply_resolution()
            self.selected_viewport.needs_resolution_update = False
        
        # Re-enable sliders after resolution adjustment
        if self.selected_viewport and self.dicom_image is not None:
            self.contrast_slider.setEnabled(True)
            self.resolution_slider.setEnabled(True)

    def toggle_edit_panel(self):
        self.edit_panel.setVisible(not self.edit_panel.isVisible())

    def apply_contrast(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'original_numpy_image'):
            # Store contrast value in viewport
            self.selected_viewport.contrast_value = self.contrast_slider.value() / 100.0
            
            # Apply contrast
            adjusted_image = self.adjust_contrast(
                self.selected_viewport.original_numpy_image.copy(), 
                self.selected_viewport.contrast_value
            )
            
            # Apply viewport's current resolution
            if self.selected_viewport.resolution_scale < 0.99:
                adjusted_image = self.adjust_resolution(
                    adjusted_image, 
                    self.selected_viewport.resolution_scale
                )
            
            # Update display
            q_image = QImage(adjusted_image, adjusted_image.shape[1], adjusted_image.shape[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.selected_viewport.set_original_pixmap(pixmap)
            self.selected_viewport.numpy_image = adjusted_image

    def apply_resolution(self):
        if self.selected_viewport and hasattr(self.selected_viewport, 'original_numpy_image'):
            # Store resolution scale in viewport
            self.selected_viewport.resolution_scale = self.resolution_slider.value() / 200.0
            
            # Start with original image
            base_image = self.selected_viewport.original_numpy_image.copy()
            
            # Apply stored contrast value
            if self.selected_viewport.contrast_value != 0:
                base_image = self.adjust_contrast(
                    base_image, 
                    self.selected_viewport.contrast_value
                )
            
            # Apply resolution
            if self.selected_viewport.resolution_scale < 0.99:
                adjusted_image = self.adjust_resolution(
                    base_image, 
                    self.selected_viewport.resolution_scale
                )
            else:
                adjusted_image = base_image
            
            # Update display
            q_image = QImage(adjusted_image, adjusted_image.shape[1], adjusted_image.shape[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.selected_viewport.set_original_pixmap(pixmap)
            self.selected_viewport.numpy_image = adjusted_image

    def adjust_contrast(self, image, contrast_value):
        # Convert to float for processing
        image_float = image.astype(np.float32)
        
        # Calculate mean intensity
        mean = np.mean(image_float)
        
        # Improved contrast adjustment using sigmoid-like function
        if contrast_value >= 0:
            # For positive contrast: enhance differences above mean
            adjusted = mean + (image_float - mean) * (1 + contrast_value * 3)
        else:
            # For negative contrast: compress differences around mean
            adjusted = mean + (image_float - mean) / (1 + abs(contrast_value) * 3)
        
        # Normalize back to 0-255 range
        adjusted = np.clip(adjusted, 0, 255)
        return adjusted.astype(np.uint8)

    def adjust_resolution(self, image, scale):
        if scale >= 0.99:  # If scale is essentially 1, return original image
            return image
        
        original_height, original_width = image.shape
        
        # Calculate new dimensions while maintaining aspect ratio
        new_width = max(int(original_width * scale), 1)
        new_height = max(int(original_height * scale), 1)
        
        # Create downsampled image
        downsampled = np.zeros((new_height, new_width), dtype=np.uint8)
        
        # Calculate pixel mapping
        x_ratio = original_width / new_width
        y_ratio = original_height / new_height
        
        # Efficient downsampling using area averaging
        for i in range(new_height):
            for j in range(new_width):
                # Calculate the boundaries of the original pixels that map to this new pixel
                x_start = int(j * x_ratio)
                x_end = int((j + 1) * x_ratio)
                y_start = int(i * y_ratio)
                y_end = int((i + 1) * y_ratio)
                
                # Take the average of the corresponding area in the original image
                downsampled[i, j] = np.mean(image[y_start:y_end, x_start:x_end])
        
        # Resize back to original dimensions using nearest neighbor interpolation
        # This maintains the FOV while showing the reduced resolution
        result = np.zeros((original_height, original_width), dtype=np.uint8)
        
        y_scale = original_height / new_height
        x_scale = original_width / new_width
        
        for i in range(original_height):
            for j in range(original_width):
                result[i, j] = downsampled[min(int(i / y_scale), new_height - 1)][min(int(j / x_scale), new_width - 1)]
        
        return result

    def import_dicom(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm)", options=options)
        if file_path:
            dataset = pydicom.dcmread(file_path)
            image_data = dataset.pixel_array
            self.dicom_image = image_data

            normalized_image = self.normalize_image(image_data)
            q_image = QImage(normalized_image, normalized_image.shape[1], normalized_image.shape[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Initialize or reset viewport settings
            for label in [self.image_label, self.top_right_panel, self.bottom_right_panel]:
                label.numpy_image = normalized_image
                label.original_numpy_image = normalized_image.copy()
                label.set_original_pixmap(pixmap)
                label.contrast_value = 0
                label.resolution_scale = 1.0

            # Reset sliders to default values
            self.contrast_slider.setValue(0)
            self.resolution_slider.setValue(200)
            
    def select_viewport(self, viewport):
        if viewport == "view1":
            self.selected_viewport = self.top_right_panel
            self.view_selector_button.setText("Selected: View1")
        elif viewport == "view2":
            self.selected_viewport = self.bottom_right_panel
            self.view_selector_button.setText("Selected: View2")

        # Update sliders to match selected viewport's settings
        if self.selected_viewport and self.dicom_image is not None:
            self.contrast_slider.setValue(int(self.selected_viewport.contrast_value * 100))
            self.brightness_slider.setValue(int(getattr(self.selected_viewport, 'brightness_value', 0) * 100))
            self.resolution_slider.setValue(int(self.selected_viewport.resolution_scale * 200))
            self.contrast_slider.setEnabled(True)
            self.brightness_slider.setEnabled(True)
            self.resolution_slider.setEnabled(True)

    def normalize_image(self, image):
        image = image.astype(np.float32)
        image -= image.min()
        image /= image.max()
        image *= 255.0
        return image.astype(np.uint8)

    def toggle_snr_panel(self):
        self.snr_panel.setVisible(not self.snr_panel.isVisible())

    def activate_noise_analysis(self):
        self.reset_analysis_mode()
        self.image_label.analysis_type = 'noise'
        self.image_label.snr_callback = self.perform_snr_analysis
        self.active_viewport = self.image_label

    def activate_signal_analysis(self, signal_number):
        self.reset_analysis_mode()
        self.image_label.analysis_type = f'signal{signal_number}'
        self.image_label.snr_callback = self.perform_snr_analysis
        self.active_viewport = self.image_label

    def reset_analysis_mode(self):
        for viewport in [self.image_label, self.top_right_panel, self.bottom_right_panel]:
            viewport.analysis_type = None
            viewport.snr_callback = None

    def delete_analysis_boxes(self):
        if hasattr(self.image_label, 'numpy_image'):
            normalized_image = self.normalize_image(self.image_label.numpy_image)
            q_image = QImage(normalized_image, normalized_image.shape[1], normalized_image.shape[0], QImage.Format_Grayscale8)
            original_pixmap = QPixmap.fromImage(q_image)
            self.image_label.set_original_pixmap(original_pixmap)
        
        self.noise_mean = None
        self.signal1_mean = None
        self.signal2_mean = None
        self.noise_std = None
        self.snr_display.setText("SNR: N/A")
        self.cnr_display.setText("CNR: N/A")

    def perform_snr_analysis(self, analysis_type, box_data):
        if analysis_type == 'noise':
            self.noise_mean = np.mean(box_data)
            self.noise_std = np.std(box_data)
        elif analysis_type == 'signal1':
            self.signal1_mean = np.mean(box_data)
        elif analysis_type == 'signal2':
            self.signal2_mean = np.mean(box_data)

        # Calculate and update SNR if we have signal1 and noise
        if self.signal1_mean is not None and self.noise_mean is not None and self.noise_std is not None:
            snr = (self.signal1_mean - self.noise_mean) / self.noise_std
            self.snr_display.setText(f"SNR: {snr:.4f}")

        # Calculate and update CNR if we have both signals and noise
        if (self.signal1_mean is not None and self.signal2_mean is not None and 
                self.noise_std is not None):
            cnr = (self.signal1_mean - self.signal2_mean) / self.noise_std
            self.cnr_display.setText(f"CNR: {cnr:.4f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())