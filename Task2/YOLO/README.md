# Player Tracking and Heatmap Visualization System

# Description
This project combines YOLOv8-based video processing with a desktop application for player tracking and heatmap generation. The system processes sports videos to detect and track players, generating actionable heatmaps visualizing player activity on a field.

It consists of two primary components:

   1. **Colab Component**: For video processing, player tracking, and heatmap data generation.
   2. **GUI Component**: A desktop application for visualizing heatmaps, replaying videos, and interacting with tracking data.
# Features
## Colab Component:
  - Player Detection and Tracking:
    - Uses YOLOv8 for detecting players in videos.
    - Tracks player positions across frames and assigns unique IDs.
  - Heatmap Data Preparation:
    - Stores player positions in a pickle file for later visualization.
  - File Management:
    - Uploads and processes videos in Google Colab.
    - Downloads processed videos with player annotations.
## GUI Component:
  - Heatmap Visualization:
    - Displays detailed heatmaps for individual players.
    - Projects player positions onto a top-down view of the field using homography.
  - Video Playback:
    - Replays processed videos with player tracking annotations.
    - Supports play, pause, and stop controls.
  - Interactive Point Selection:
  - Allows users to manually select key points in the video and field images to improve field alignment.
# File Content
## Colab Component
### Key Functions
  - process_video(video_path):
    - Detects and tracks players in a video.
    - Saves the annotated video as tracked_players.mp4.
  - generate_heatmap(player_id):
    - Creates a heatmap for a specific player using their tracked positions.
  - files.upload():
    - Uploads a video file for processing in Colab.
  - files.download('tracked_players.mp4'):
    - Downloads the processed video with tracking annotations.
### Output
  - tracked_players.mp4: Video with bounding boxes and unique player IDs.
  - player_tracks.pkl: A pickle file storing player positions for heatmap generation.
  - last_frame.jpg: The last processed frame for heatmap overlay.
## GUI Component
### Classes
  - HeatmapViewer:
    - Implements the GUI for visualizing heatmaps and replaying processed videos.
### Key Functions
  - generate_heatmap(player_id):
    - Generates heatmaps for a selected player using field projections.
  - prompt_player_id():
    - Prompts the user to select a player ID and displays their heatmap.
  - play_video() / pause_video() / stop_video():
    - Controls video playback within the application.
### Interactive Field Selection
  - calc2(path):
    - Allows users to select four points in the video and field images to calculate the homography matrix.
# Usage
## Colab Component
1. **Install Dependencies**: Install YOLOv8 and related libraries:
```
!pip install ultralytics opencv-python-headless matplotlib
```
2. **Run Video Processing**:
  - Upload a video file:
  ```
  from google.colab import files
  uploaded = files.upload()
  ```
  - Process the video:
  ```
  video_path = next(iter(uploaded))
  process_video(video_path)
  ```
3. **Generate Heatmap Data**: Generate a heatmap for a player:
```
heatmap_frame = generate_heatmap(player_id=1)
plt.imshow(cv2.cvtColor(heatmap_frame, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('Heatmap for Player 1')
plt.show()
```
4. **Download Outputs**: Download the processed video:
```
files.download('tracked_players.mp4')
```
## GUI Component
1. **Install Requirements**: Ensure Python 3.8 or higher is installed. Install required libraries:
```
pip install opencv-python numpy matplotlib pillow
```

2. **Run the Application**: Execute the script:
```
python app.py
```
3. **Set Up Homography**: Select key points on the video and field images using the interactive tool:
```
calc2('tracked_players.mp4')  # Select points in the video
calc2('field_background.jpg')  # Select points in the field image
```
4. **View Heatmaps and Videos**:
  - Select a player to view their heatmap.
  - Replay processed videos with tracking annotations.
# Requirements
  - YOLOv8: For real-time player detection.
  - OpenCV: For video processing and visualization.
  - Tkinter: For the desktop application.
  - Matplotlib: For plotting heatmaps.
  - Google Colab: For cloud-based video processing.
# Output
## Colab Outputs:
  - tracked_players.mp4: Annotated video with player tracking.
  - player_tracks.pkl: Player position data for heatmap generation.
  - last_frame.jpg: A reference frame for overlaying heatmaps.
## GUI Outputs:
  - Heatmaps visualizing player movements.
  - Interactive playback of processed videos.
# License
This project is licensed under the MIT License.
