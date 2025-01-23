# Project Repository
# Description
This repository contains six distinct projects organized into separate folders. Each project focuses on a unique problem-solving or development task, ranging from video processing and AI-based applications to interactive visualization tools and even games. The repository serves as a showcase for diverse technologies, programming techniques, and design principles.

Each folder in the repository represents a standalone project, complete with its own codebase, documentation, and resources.

# Repository Structure
## 1. Midterm
- Project Name: TumorScent
- Description:
  - TumorScent is a fictional imaging technique that breaks the boundaries of physics by inventing a revolutionary method for cancer detection based on scent. This speculative project envisions leveraging advanced theoretical principles to capture and analyze scent patterns emitted by cancerous tissues, enabling a non-invasive and ultra-sensitive diagnostic tool.
## 2. Task1
- Project Name: 3D Medical Image Viewer
- Description:
  - A comprehensive application for visualizing 3D medical image data in multiple formats, including DICOM and NIfTI. This project enables users to load, process, and interact with medical images through intuitive visualization tools, offering features such as multi-view displays, dynamic crosshair navigation, brightness/contrast adjustment, and zooming.
- Key Features:
  - Multi-view visualization (axial, sagittal, coronal).
  - Interactive controls for image navigation, brightness/contrast, and zoom.
  - Supports DICOM and NIfTI formats with error handling for invalid files.
- Technologies: Python, PyQt5, Matplotlib, pydicom, nibabel.
- Readme: [README](https://github.com/Kareem-Taha-05/Year1_Medical_Imaging_Projects/tree/main/Task1)
## 3. Task2
- Project Name: YOLO Player Tracker & Image Classifier
- Description:
  - Task2 consists of two parts:
    - 1. YOLO Player Tracker: A real-time player detection and tracking system using YOLOv8. This project processes sports videos, identifies players, tracks their movements, and generates heatmaps for their positional activity.
    - 2. Image Classifier: A machine learning model to classify images into predefined categories. The project includes data preprocessing, training, and prediction pipelines.
- Key Features:
  - YOLO Player Tracker:
    - Real-time player detection and tracking using YOLOv8.
    - Generates annotated videos with player IDs and bounding boxes.
    - Visualizes positional heatmaps using homography.
  - Image Classifier:
    - Custom dataset support with preprocessing.
    - Training pipeline for multi-class classification.
    - TensorFlow-based deep learning model.
- Technologies: Python, YOLOv8, OpenCV, TensorFlow, Matplotlib, Tkinter.
- Readme:
    - [README 1 ](https://github.com/Kareem-Taha-05/Year1_Medical_Imaging_Projects/tree/main/Task2/ImageClassifier)
    - [README 2](https://github.com/Kareem-Taha-05/Year1_Medical_Imaging_Projects/tree/main/Task2/YOLO)
## 4. Task3
- Project Name: 3D Brain Puzzle Game
- Description:
  - A Unity-based 3D puzzle game where players reconstruct a scattered brain by moving and rotating individual parts. The game promotes spatial awareness and problem-solving skills through an engaging and interactive experience.
- Key Features:
  - Drag-and-rotate mechanics for assembling brain parts.
  - Realistic 3D models with high-quality textures.
  - Dynamic camera controls for 360° exploration of the puzzle.
  - Progress tracking and achievements for completing the puzzle efficiently.
- Technologies: Unity, C#, Blender
- Readme: [README](https://github.com/Kareem-Taha-05/Year1_Medical_Imaging_Projects/tree/main/Task3)
## 5. Task4
- Project Name:  DICOM Viewer
- Description:
  - A feature-rich application for loading, viewing, and interacting with DICOM medical images. The project supports displaying single-frame and multi-frame DICOM files, viewing metadata, anonymizing sensitive patient data, and generating 3D slice layouts.
- Key Features:
  - Image Viewer:
    - Supports single-frame and multi-frame DICOM files.
    - Real-time image adjustments (brightness, contrast, zoom).
  - Metadata Viewer:
    - Displays DICOM tags and allows anonymization of sensitive data.
  - 3D Viewer:
    - Visualizes DICOM slices in a tiled layout for detailed analysis.
- Technologies: Python, Tkinter, pydicom, NumPy, Matplotlib.
- Readme: [README](https://github.com/Kareem-Taha-05/Year1_Medical_Imaging_Projects/tree/main/Task4)
## 6. Task5
- **Project Name**: Medical Image Editor
- **Description**:
    - The Medical Image Editor is a comprehensive application for processing and analyzing medical image data, primarily in the DICOM format. It provides advanced features for editing, visualizing, and enhancing medical images, making it a valuable tool for professionals and researchers in the medical imaging field. The project leverages PyQt5 for the graphical user interface, OpenCV for image processing, and pydicom for handling DICOM files.
- **Key Features**:
    - DICOM Image Support: Imports and normalizes DICOM files for visualization.
    - Image Processing Tools: Includes noise addition, filters (Gaussian, median), morphological enhancements, contrast, brightness, and resolution adjustments.
    - Zoom and Pan: Multiple zoom modes (e.g., bilinear, cubic).
    - Histogram Visualization: Displays intensity histograms with statistical measures.
    - SNR and CNR Analysis: Calculates Signal-to-Noise and Contrast-to-Noise Ratios using selected image regions.
    - Fourier Filtering: Implements low-pass and high-pass filters with blending options.
    - Interactive GUI: Built with PyQt5, featuring multiple viewports, sliders, buttons, and menus.
- **Technologies**: PyQt5, pydicom, OpenCV, NumPy, Matplotlib.
- **Readme**: [README](https://github.com/Kareem-Taha-05/Year1_Medical_Imaging_Projects/tree/main/Task5)
# Getting Started
## Prerequisites
Each project has its own dependencies and setup instructions detailed in its respective README file. General prerequisites include:
  - Python 3.8+ for Python-based projects.
  - Required Python libraries (install via pip install -r requirements.txt where applicable).
  - Specific tools and frameworks listed in individual project READMEs.
## Installation
  - 1. Clone the repository:
```
git clone https://github.com/yourusername/repository-name.git
cd repository-name
```
  - 2. Navigate to the desired project folder and follow the setup instructions in its README.

# Contributors
1. [Kareem Taha](https://github.com/Kareem-Taha-05)
2. [Omar Gamal](https://github.com/OmarGamalH)
3. [Kareem Hassan](https://github.com/karimhassan-808)
4. [Omar Amein](https://github.com/OmarAmein)
5. [Sulaiman](https://github.com/SulaimanAlfozan)
# License
This repository is licensed under the MIT License.
