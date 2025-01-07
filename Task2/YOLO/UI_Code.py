import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from PIL import Image, ImageTk

# Assume calc2 is a function that captures the necessary points
from calc import calc2

# Load video and field image points
video = calc2("tracked_players.mp4")
image = calc2("field_background.jpg")
video_points = np.array([  # Adjust these indices based on your function's output
    list(video[0]),
    list(video[1]),
    list(video[2]),
    list(video[3])  # Example bottom-left corner in the video
], dtype=np.float32)

field_points = np.array([  # Adjust these indices based on your function's output
    list(image[0]),
    list(image[1]),
    list(image[2]),
    list(image[3])  # Example bottom-left corner in the field image
], dtype=np.float32)


class HeatmapViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Heatmap Viewer")

        # Calculate homography matrix
        self.homography_matrix, _ = cv2.findHomography(video_points, field_points)

        # Configure grid layout
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Load tracking data
        with open('player_tracks.pkl', 'rb') as f:
            self.player_tracks = pickle.load(f)

        # Load last frame if available for dimensions
        self.frame_height, self.frame_width = 720, 1280  # Default dimensions
        if os.path.exists('last_frame.jpg'):
            frame = cv2.imread('last_frame.jpg')
            self.frame_height, self.frame_width = frame.shape[:2]

        # Create matplotlib figure with aspect ratio matching the video
        aspect_ratio = self.frame_width / self.frame_height
        self.fig = Figure(figsize=(5, 5/aspect_ratio))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Video label setup
        self.video_frame = tk.Frame(self.root, width=self.frame_width//2, height=self.frame_height//2)
        self.video_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(expand=True, fill='both')

        # Add control buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')

        self.btn_view_heatmap = tk.Button(button_frame, text="View Player Heatmap", command=self.prompt_player_id)
        self.btn_view_heatmap.pack(side='left', padx=5)

        self.btn_play_video = tk.Button(button_frame, text="Play Video", command=self.play_video)
        self.btn_play_video.pack(side='left', padx=5)

        self.btn_pause_video = tk.Button(button_frame, text="Pause Video", command=self.pause_video)
        self.btn_pause_video.pack(side='left', padx=5)

        self.btn_stop_video = tk.Button(button_frame, text="Stop Video", command=self.stop_video)
        self.btn_stop_video.pack(side='left', padx=5)

        self.video_path = 'tracked_players.mp4'  # Ensure this path is correct
        self.cap = None
        self.playing = False

        self.selected_player_id = None

    def generate_heatmap(self, player_id):
        if player_id not in self.player_tracks:
            messagebox.showwarning("Error", f"Player ID {player_id} not found in tracking data.")
            return

        # Load background image (field image)
        background = cv2.imread('field_background.jpg')
        if background is None:
            print("Error: Background image not found")
            return
        background_height, background_width = background.shape[:2]

        # Create empty heatmap array with dimensions matching the field background
        heatmap = np.zeros((background_height, background_width))

        # Aggregate and transform player positions
        positions = self.player_tracks[player_id]
        for pos in positions:
            # Apply homography to transform position to top-down view
            transformed_pos = cv2.perspectiveTransform(np.array([[pos]], dtype=np.float32), self.homography_matrix)
            x, y = int(transformed_pos[0][0][0]), int(transformed_pos[0][0][1])

            # Only add to heatmap if the transformed coordinates are within bounds
            if 0 <= y < background_height and 0 <= x < background_width:
                heatmap[y, x] += 1

        # Smooth the heatmap using Gaussian blur
        heatmap = cv2.GaussianBlur(heatmap, (151, 151), 0)

        # Convert background to RGB format (cv2 loads images in BGR)
        background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)

        # Create the heatmap overlay
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.imshow(background)

        # Normalize heatmap for better visualization and overlay it
        heatmap_normalized = cv2.normalize(heatmap, None, 0, 1, cv2.NORM_MINMAX)
        heatmap_plot = ax.imshow(heatmap_normalized, cmap='hot', alpha=0.6)
        ax.set_title(f'Heatmap for Player {player_id}')
        ax.axis('off')

        # Add colorbar and finalize layout
        self.fig.colorbar(heatmap_plot, ax=ax, label='Position Density')
        ax.set_aspect('equal')
        self.fig.tight_layout()

        # Draw the updated heatmap on the canvas
        self.canvas.draw()

    def prompt_player_id(self):
        try:
            # Show available player IDs
            available_ids = sorted(self.player_tracks.keys())
            message = f"Available Player IDs: {', '.join(map(str, available_ids))}\nEnter the Player ID:"
            player_id = simpledialog.askinteger("Player ID", message, parent=self.root)
            if player_id is not None:
                self.generate_heatmap(player_id)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid integer Player ID.")

    def play_video(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            messagebox.showerror("Error", "Unable to open video file.")
            return

        self.playing = True

        def update_frame():
            if self.playing:
                ret, frame = self.cap.read()
                if ret:
                    # Resize the frame to half the window width
                    frame_resized = cv2.resize(frame, (self.frame_width // 2, self.frame_height // 2))
                    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.video_label.imgtk = imgtk
                    self.video_label.configure(image=imgtk)
                    self.root.after(30, update_frame)  # Correct frame update rate
                else:
                    self.cap.release()
                    self.cap = None

        update_frame()

    def pause_video(self):
        self.playing = False

    def stop_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.playing = False
        self.video_label.configure(image='')
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = HeatmapViewer(root)
    root.mainloop()
