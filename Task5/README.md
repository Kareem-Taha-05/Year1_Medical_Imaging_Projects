# Medical Image Editor

## Description
The Medical Image Editor is a comprehensive application for processing and analyzing medical image data, primarily in the DICOM format. It provides advanced features for editing, visualizing, and enhancing medical images, making it a valuable tool for professionals and researchers in the medical imaging field. The project leverages PyQt5 for the graphical user interface, OpenCV for image processing, and pydicom for handling DICOM files.

## Features

- **Image Processing and Enhancement**:
  - Add noise: Gaussian, Salt & Pepper, Pink noise.
  - Apply filters: Gaussian, Median, Pink, High-pass, Low-pass filters.
  - Contrast and brightness adjustment for improved visualization.
  - Advanced enhancements:
    - Histogram Equalization
    - CLAHE (Contrast Limited Adaptive Histogram Equalization)
    - Morphological Enhancements
  
- **SNR/CNR Analysis**:
  - Interactive noise and signal analysis using selectable regions of interest (ROI).
  - Real-time updates of Signal-to-Noise Ratio (SNR) and Contrast-to-Noise Ratio (CNR).

- **Zoom and Resolution Settings**:
  - Dynamic zoom-in and zoom-out functionalities with support for various interpolation modes (e.g., Nearest-Neighbor, Bilinear, Cubic).
  - Resolution scaling for efficient image rendering.

- **Histogram Visualization**:
  - Displays detailed histograms for the selected image with key statistics (mean, median, standard deviation).

- **Error Handling and Feedback**:
  - Clear error messages for invalid or unsupported file formats.
  - Smooth handling of large datasets with progress feedback.

## File Content

### Classes
- **AnalysisLabel**: Handles image display, zooming, and interaction.
- **MainWindow**: Implements the main graphical interface and connects all functionalities.

### Functions
#### File Loading Functions
- **import_dicom**: Loads and displays a DICOM file, normalizing it for consistent visualization.
- **normalize_image**: Normalizes image pixel values to an 8-bit range.

#### Image Rendering Functions
- **apply_contrast**: Adjusts the contrast of the currently selected image.
- **apply_brightness**: Applies brightness changes to the displayed image.
- **apply_resolution**: Dynamically adjusts the resolution of the selected image for improved performance.

#### Enhancement Functions
- **apply_histogram_equalization**: Enhances image contrast using histogram equalization.
- **apply_clahe**: Performs local contrast enhancement with CLAHE.
- **apply_morphological_enhancement**: Enhances image details using top-hat, black-hat, and gradient operations.

#### Analysis Functions
- **perform_snr_analysis**: Computes SNR and CNR values based on user-selected regions.
- **delete_analysis_boxes**: Resets selected analysis regions and updates display.

#### Zoom and Navigation Functions
- **zoom_in/zoom_out**: Implements zooming functionality with real-time feedback.
- **select_viewport**: Allows users to select and navigate different image views.

## Usage

1. **Install Dependencies**: Ensure Python 3.8 or later is installed. Then, install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Application**: Start the application with:
    ```bash
    python Task5.py
    ```

3. **Load a DICOM Image**:
    - Click the "Import DICOM" button to select and load a .dcm file.

4. **Edit and Enhance Images**:
    - Use the toolbar options to add noise, apply filters, and adjust contrast, brightness, or resolution.
    - Select advanced enhancement techniques like CLAHE or Histogram Equalization for better image quality.

5. **Analyze Images**:
    - Activate SNR/CNR analysis and select regions of interest for calculating metrics.
    - View the results dynamically updated in the application interface.

6. **Zoom and View Images**:
    - Use the zoom functionality to focus on specific regions of the image.
    - Adjust interpolation modes for enhanced viewing quality.

7. **View Histograms**:
    - Double-click on an image to open a detailed histogram view with key statistics.

8. **Exit the Application**:
    - Close the GUI window or terminate the application from the command line.

## License
This project is licensed under the [MIT License](LICENSE).