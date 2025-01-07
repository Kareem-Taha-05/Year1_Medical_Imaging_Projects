import cv2
import matplotlib.pyplot as plt
def calc2(path):
    # Load the video and capture the first frame
    video_path = path  # Update with the path to your video file
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()  # Capture the first frame or a clear key frame with the field in view
    cap.release()

    if not ret:
        print("Error: Unable to capture the first frame from the video.")
    else:
        # Convert the frame from BGR to RGB for displaying with Matplotlib
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set up a list to store the selected points
        points = []

        # Define a function for handling mouse clicks
        def onclick(event):
            # Check if the mouse click is within the image bounds
            if event.xdata is not None and event.ydata is not None:
                points.append((int(event.xdata), int(event.ydata)))
                print(f"Point selected: {(int(event.xdata), int(event.ydata))}")
                if len(points) == 4:
                    plt.close()  # Close the plot when four points are selected

        # Display the image and connect the mouse click event
        fig, ax = plt.subplots()
        ax.imshow(frame_rgb)
        ax.set_title("Click on the four corners of the field in the video frame")
        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

        print("Selected video points:", points)
    return points
    
