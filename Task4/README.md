# DICOM Viewer

# Description
The DICOM Viewer is an intuitive application for loading, visualizing, and interacting with DICOM medical images. The application supports functionalities such as displaying images, exploring metadata, anonymizing sensitive fields, and visualizing 3D slices in a tiled format.

It uses PyQt5 for the user interface, pydicom for processing DICOM files, and NumPy for image data manipulation.

# Features

- **Image Viewer**:
    - Load and Display DICOM Images:
    - Supports single-frame and multi-frame DICOM files.
    - Plays multi-frame (M2D) files as videos with adjustable speed.
    - Error Handling:
      - Provides clear error messages for unsupported or invalid files.
- **Metadata Viewer**:
  - View Metadata:
    - Displays DICOM tags, patient details, pixel data, study info, modality, and physician info.
  - Search Functionality:
    - Search for specific tags within the DICOM metadata.
  - Anonymization Tool:
    - Easily anonymize sensitive fields using a custom prefix.
- **3D Viewer**:
  - View 3D Tiles:
    - Displays DICOM slices in a tiled layout for easy exploration.
  - Zoom Controls:
    - Zoom in and out of specific regions for enhanced analysis.
  
# File Content
## Classes
- **DicomViewer**: The main class that implements the graphical interface and core functionalities.
## Key Functions
### Image Loading and Display
- **load_dicom_file()**:
    - Loads a single DICOM file and initializes image and metadata-related functionalities.
- **display_image()**:
    - Displays single-frame images or plays multi-frame videos.
- **stop_video()**:
    - Stops multi-frame video playback.
- **display_2d_image(pixel_array)**:
    - Handles DICOM-specific scaling and normalizes pixel values for display.
- **play_m2d_video()**:
    - Plays multi-frame (M2D) images as videos.
### Metadata Handling
- **display_dicom_tags()**:
    - Displays all DICOM tags in a tabular format.
- **display_patient_info()**:
    - Shows patient-related metadata, including name, ID, birth date, and sex.
- **anonymize_dicom()**:
    - Anonymizes patient information with a user-specified prefix.
    - 3D Viewer and Zoom
- **display_3d_tiles()**:
    - Displays DICOM slices in a grid format with adjustable zoom.
- **eventFilter()**:
    - Adjusts quality and resolution of the tiles when zooming.
# Usage
1. **Install Dependencies**: Ensure you have Python installed (preferably version 3.8 or higher). Install the required dependencies using **requirements.txt**:
    ``` 
    pip install -r requirements.txt
    ```
2. **Launch the Application**: Run the Python script using:
    ``` 
    python Task4.py 
    ```
3. **Use the Image Viewer tab to load and view DICOM images**.
  - Supported formats:
    - Single-frame DICOM images.
    - Multi-frame DICOM images (M2D).
    - Explore Metadata:

3. **Use the Metadata Viewer tab to search, view, and anonymize DICOM metadata**.
  - 3D Viewer:
    - Load and visualize 3D DICOM slices as tiles using the 3D Viewer tab.
    - Use zoom controls to focus on specific areas.

6. Error Notifications: If any invalid file or folder is selected, the application will provide warnings and handle the error gracefully.
7. Exit the Application: Close the GUI window or press **Ctrl+C** in the terminal.

# LICENSE
This project is licensed under the [MIT License](../LICENSE.txt).
