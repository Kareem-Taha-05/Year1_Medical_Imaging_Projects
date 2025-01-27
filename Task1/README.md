# 3D Medical image viewer

# Description
The 3D Medical Image Viewer is a comprehensive application for visualizing 3D medical image data in multiple formats, including DICOM and NIfTI. This project enables users to load, process, and interact with medical images through intuitive visualization tools. It supports various functionalities, such as displaying axial, sagittal, and coronal views, as well as adjusting brightness and contrast and zooming into specific regions of interest.

The project uses PyQt5 for the graphical user interface, matplotlib for rendering images, and libraries such as pydicom and nibabel for handling medical image formats.

# Features

- **Multi-View Visualization**:
    - Displays three orthogonal views of medical image data:
        - Axial View: Horizontal slice of the image.
        - Sagittal View: Vertical slice from the side.
        - Coronal View: Vertical slice from the front.
    - Each view is rendered dynamically and updated as users interact with the application.
- **DICOM and NIfTI Support**: 
    - Users can load and process DICOM folders containing .dcm files or NIfTI files (.nii, .nii.gz) seamlessly.
    - Handles metadata, pixel data, and compression formats.
- **Interactive Brightness and Contrast Adjustment**:
    - Real-time modification of image brightness and contrast using sliders.
    - Automatically applies changes to all displayed views.
- **Dynamic Crosshair Navigation**:
    - Allows users to navigate through slices interactively.
    - Crosshairs in one view update corresponding slices in other views, ensuring spatial consistency.
- **Zoom Functionality**: 
    - Zoom into or out of specific regions in any view.
    - Provides visual feedback with custom zoom cursors.
    - Supports zoom centering on a specific cursor position.

- **Error Handling and Progress Feedback**:
    - Displays progress bars while processing large datasets.
    - Informs users of invalid or missing files with clear error messages.
- **Customizable User Interface**:
    - Aesthetic UI with styled buttons, sliders, and layouts.
    - Resizable and responsive widgets.

# File Content
## Classes
- **MedicalImageViewer**: The central class of the project, which implements the graphical user interface (GUI) and application logic.
## Functions
### File Loading Functions
- **upload_folder()**:
    - Opens a dialog for the user to select a folder containing DICOM files.
    - Invokes load_dicom_folder() to process and display the data.
- **load_dicom_folder(folder_path)**:
    - Reads all .dcm files in the selected folder.
    - Handles missing or invalid files gracefully, with warnings for skipped files.
    - Sorts and processes slices to create a 3D volume (image_volume).
    - Initializes sliders for navigation and updates image views.
- **upload_nifti_folder()**:
    - Opens a dialog for the user to select a NIfTI file (.nii or .nii.gz).
    - Invokes load_nifti_file() for processing.
- **load_nifti_file(file_path)**:
    - Loads the selected NIfTI file using nibabel.
    - Converts data into a 3D volume compatible with the application.
    - Updates sliders and displays the data in all views.
- **load_dicom_slice(filepath)**:
    - Reads a single DICOM slice from a file.
    - Applies rescale slope and intercept if available.
    - Normalizes pixel values to an 8-bit range for consistency.
### Image Rendering Functions
- **show_views()**:
    - Displays the current slices for axial, sagittal, and coronal views.
    - Invokes prepare_canvas() to render each view on its respective canvas.
- **prepare_canvas(canvas, image, title)**:
    - Clears and updates a given canvas with the provided image and title.
    - Used for rendering individual slices in the axial, sagittal, and coronal views.
- **update_views()**:
    - Adjusts and refreshes all views based on user interactions (e.g., slider movement, brightness/contrast changes).
    - Calls adjust_brightness_contrast() to apply user-defined modifications.
- **plot_view(view, canvas, index, crosshair_position=None)**:
    - Plots a single 2D slice on the given canvas.
    - Optionally includes crosshairs at the specified position.
### Image Adjustment Functions
- **adjust_brightness_contrast(image, brightness, contrast)**:
    - Applies brightness and contrast adjustments to the given image.
    - Uses a linear transformation formula and ensures pixel values remain within valid bounds.
- **update_axial_index(value) / update_sagittal_index(value) / update_coronal_index(value)**:
    - Updates the current slice index for the respective view (axial, sagittal, coronal) based on slider movement.
    - Calls update_views() to reflect the changes.
- **handle_cursor_motion(event)**:
    - Updates crosshair positions and synchronizes the slice indices across views.
    - Triggered when the user moves the mouse within the canvas.
- **zoom_in() / zoom_out()**:
    - Activates zoom-in or zoom-out modes.
    - Updates the mouse cursor to indicate the zooming mode.
- **perform_zoom(canvas, x, y)**:
    - Executes a zoom operation centered on the specified (x, y) coordinates.
    - Adjusts the display limits of the canvas for magnification or reduction.
- **update_canvas_limits(ax, zoom_factor, x=None, y=None)**:
    - Calculates and applies new axis limits for zooming.
    - Ensures the zoom is centered around the specified coordinates.
### Mode Switching Functions
- **toggle_mode()**:
    - Toggles between cursor mode and zoom mode.
    - Updates button states and cursor appearance.
- **set_cursor_mode()**:
    - Enables cursor mode and disables zoom functionality.
- **set_zoom_mode()**:
    - Enables zoom mode and activates zoom-related controls.
- **reset_zoom_mode()**:
    - Resets the zoom state and restores the default cursor.
### Event Handlers
- **on_mouse_press(event)**:
    - Handles mouse button presses.
    - Initiates zooming or updates crosshair positions based on the current mode.
- **on_mouse_release(event)**:
    - Handles mouse button releases.
    - Ends zooming or crosshair movement.
- **on_mouse_motion(event)**:
    - Tracks mouse movements while the button is pressed.
    - Updates views or performs zooming.
# Usage
1. **Install Dependencies**: Ensure you have Python installed (preferably version 3.8 or higher). Install the required dependencies using **requirements.txt**:
    ``` 
    pip install -r requirements.txt
    ```
2. **Launch the Application**: Run the Python script using:
    ``` 
    python Task1.py 
    ```
3. **Load Medical Data**:
    - Upload DICOM Folder: Click the "Upload DICOM Folder" button and select a folder containing .dcm files.
    - Upload NIfTI File: Click the "Upload NIfTI File" button and choose a .nii or .nii.gz file.
4. **Adjust Views**:
    - Use the sliders below each view to navigate through the image slices.
    - Adjust brightness and contrast sliders to enhance image visibility.
5. **Zoom Features**:
    - Switch to zoom mode by clicking "Switch to Zoom Mode".
    - Use "Zoom In" or "Zoom Out" to magnify or shrink a specific region.
6. Error Notifications: If any invalid file or folder is selected, the application will provide warnings and handle the error gracefully.
7. Exit the Application: Close the GUI window or press **Ctrl+C** in the terminal.
# Photos
![Image](https://github.com/user-attachments/assets/835db456-ca8e-470e-9231-b77f36223118)

![Image](https://github.com/user-attachments/assets/00d95091-3c1f-4f81-9c02-4ab254518ef2)
# Video
https://github.com/user-attachments/assets/af8d3366-2321-4864-9fe0-ecd4f9bfd52b
# LICENSE
This project is licensed under the [MIT License](../LICENSE.txt).




    


