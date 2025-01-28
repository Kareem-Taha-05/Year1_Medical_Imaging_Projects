# AI Organ Classification System

# Description
The AI Organ Classification System is a complete pipeline for training and deploying a multi-organ classification model. It includes tools for training a deep learning model using custom datasets and a user-friendly desktop application for real-time organ prediction from images. The system supports classification of organs such as Brain, Lung, Kidney, and Hand.

The system leverages TensorFlow for building and training models, Tkinter for creating a desktop interface, and Google Colab for scalable training with cloud storage integration.

# Features

**1. Training Pipeline**:
  - Custom Dataset Support:
    - Train the model using labeled folders of images stored locally or on Google Drive.
  - Convolutional Neural Network (CNN):
    - A 4-class CNN architecture for organ classification.
  - Scalable Training:
    - Compatible with Google Colab for faster GPU-based training.
  - Preprocessing:
    - Normalizes images and resizes them to a uniform resolution.
  - Metrics:
    - Tracks training and validation accuracy and loss during training.
  
**2. Prediction Application**:
  - User-Friendly GUI:
    - Intuitive interface to upload images, adjust contrast/brightness, and view predictions.
  - Real-Time Prediction:
    - Classifies organs with confidence scores using the trained model.
  - Image Manipulation:
    - Supports zooming, panning, and contrast/brightness adjustments.
  - Prediction History:
    - Saves and displays past predictions.
  
# File Content
## Training Code
  - create_multi_organ_model(img_height, img_width, num_classes):
    - Builds a CNN model for organ classification.
  - preprocess_images(image_files, img_height, img_width):
    - Processes image files by resizing and normalizing them.
  - prepare_data_for_training(folder_paths, labels, img_height, img_width):
    - Loads datasets from folders, encodes labels, and splits them into training and validation sets.
  - train_model(folder_paths, organ_labels, img_height, img_width, batch_size, epochs):
    - Trains the model using the provided data and returns training history.
  - Google Colab Integration:
    - Includes functions for loading datasets and saving models directly to Google Drive.
## Prediction Application
  - ImagePredictionApp:
    - Implements a GUI for uploading and predicting images.
  - load_model():
    - Loads the trained model from the file system.
  - predict_image(file_path):
    - Predicts the organ type and confidence score for an uploaded image.
  - Interactive Image Features:
    - Supports zooming, panning, and brightness/contrast adjustments.
# Usage
## Training the Model
- **1. Set Up Google Colab**:
    - Upload the training script to Google Colab.
    - Mount your Google Drive:       ( or use this [Training DataSet](https://drive.google.com/drive/folders/1QKBY2AZs-VXAgsRsJu0PHWKcZuPCwQYf) instead )
    ```
    from google.colab import drive
    drive.mount('/content/drive')
    ```
- **2. Prepare Your Dataset**:
    - Organize images into folders named after their labels (e.g., brain, lung, kidney, hand).
    - Example folder structure:
    ```
    dataset/
      brain/
        image1.jpg
        image2.jpg
      lung/
        image1.jpg
        image2.jpg
    ```
- **3. Run the Training Script**:
  - Specify folder paths and corresponding labels:
  ```
  folder_paths = [
      "/content/drive/My Drive/dataset/brain",
      "/content/drive/My Drive/dataset/lung",
      "/content/drive/My Drive/dataset/kidney",
      "/content/drive/My Drive/dataset/hand"
  ]
  organ_labels = [0, 1, 2, 3]
  ```
  - Train the model:
  ```
  model, history = train_model(folder_paths, organ_labels, epochs=10)
  model.save('/content/drive/My Drive/multi_organ_classifier.keras')
  ```
- **4. Save the Model**:
  - The model will be saved as multi_organ_classifier.keras.

## Using the Prediction App
- **1. Install Dependencies**:
Ensure Python 3.8 or higher is installed. Install required libraries:
```
pip install tensorflow pillow numpy
```
- **2. Run the App**:
  - Launch the application:
  ```
  python app.py
  ```
- **3. Upload Images**:
    - Click Upload Image to select an image for prediction.
    - View predictions with confidence scores.
- **4. Interact with the Image**:
    - Adjust zoom, contrast, and brightness using the provided controls.
    - View and manage prediction history in the History tab.
# Requirements
- Python: 3.8 or higher.
- TensorFlow: 2.x or higher.
- Pillow: 8.x or higher.
- Tkinter: Pre-installed with Python on most platforms.
- Google Colab: For training with cloud resources.
# License
This project is licensed under the MIT License.
