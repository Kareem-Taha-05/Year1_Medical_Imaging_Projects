import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Label, Scale, HORIZONTAL
import numpy as np
import tensorflow as tf
from PIL import Image, ImageTk, ImageEnhance
import os

class ImagePredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Organ Prediction App")
        self.root.geometry("900x700")
        self.root.configure(bg="#4a6f91")

        # Model-related attributes
        self.model = None
        self.history = []
        
        # Image manipulation attributes
        self.zoom_factor = 1.0
        self.pan_x, self.pan_y = 0, 0

        # Setup UI
        self.setup_notebook()
        self.load_model()

    def load_model(self):
        try:
            # Model verification function from the first script
            def verify_model_path(model_path):
                possible_locations = [
                    model_path,
                    os.path.join(os.getcwd(), model_path),
                    os.path.join(os.path.dirname(__file__), model_path),
                ]
                
                for location in possible_locations:
                    if os.path.exists(location):
                        print(f"Found model at: {location}")
                        return location
                
                # If model not found, let user select it
                messagebox.showinfo("Model Not Found", 
                                   "Please select the 'multi_organ_classifier2.keras' file location")
                file_path = filedialog.askopenfilename(
                    title='Select the model file',
                    filetypes=[("Keras files", "*.keras")]
                )
                
                if file_path:
                    return file_path
                else:
                    raise FileNotFoundError("No model file selected")

            # Load the model
            model_path = verify_model_path('multi_organ_classifier.keras')
            self.model = tf.keras.models.load_model(model_path)
            print("Model loaded successfully!")
        except Exception as e:
            messagebox.showerror("Model Error", f"Could not load model: {str(e)}")
            self.root.quit()

    def setup_notebook(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Prediction Tab
        self.prediction_tab = tk.Frame(self.notebook, bg="#e1e6f2")
        self.notebook.add(self.prediction_tab, text="Predict Image")

        # Setup prediction tab components
        self.setup_prediction_tab()

        # History Tab
        self.history_tab = tk.Frame(self.notebook, bg="#557a95")
        self.notebook.add(self.history_tab, text="History")

        self.history_frame = tk.Frame(self.history_tab, bg="#557a95")
        self.history_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        self.update_history_tab()

    def setup_prediction_tab(self):
        # Header
        header_label = ttk.Label(self.prediction_tab, text="Organ Classifier", 
                                 font=("Helvetica", 18, "bold"), background="#e1e6f2")
        header_label.pack(pady=20)

        # Canvas for image display
        self.canvas = tk.Canvas(self.prediction_tab, width=650, height=400, 
                                bg="#ffffff", bd=2, relief="solid")
        self.canvas.pack(pady=10)

        # Bind panning events
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag_image)

        # Button frame
        button_frame = tk.Frame(self.prediction_tab, bg="#e1e6f2")
        button_frame.pack(pady=10)

        # Buttons
        upload_button = ttk.Button(button_frame, text="Upload Image", command=self.load_image)
        upload_button.grid(row=0, column=0, padx=10)

        zoom_in_button = ttk.Button(button_frame, text="Zoom In", command=self.zoom_in)
        zoom_in_button.grid(row=0, column=1, padx=10)

        zoom_out_button = ttk.Button(button_frame, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.grid(row=0, column=2, padx=10)

        # Contrast and Brightness Controls
        controls_frame = tk.Frame(self.prediction_tab, bg="#e1e6f2")
        controls_frame.pack(pady=10)

        contrast_label = ttk.Label(controls_frame, text="Contrast", background="#e1e6f2")
        contrast_label.grid(row=0, column=0, pady=5, padx=10)

        self.contrast_scale = Scale(controls_frame, from_=0.5, to=2.0, resolution=0.1, 
                                    orient=HORIZONTAL, command=self.adjust_contrast)
        self.contrast_scale.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

        brightness_label = ttk.Label(controls_frame, text="Brightness", background="#e1e6f2")
        brightness_label.grid(row=1, column=0, pady=5, padx=10)

        self.brightness_scale = Scale(controls_frame, from_=0.5, to=2.0, resolution=0.1, 
                                      orient=HORIZONTAL, command=self.adjust_brightness)
        self.brightness_scale.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        # Prediction Label
        self.prediction_label = ttk.Label(self.prediction_tab, text="Prediction: ", 
                                          font=("Helvetica", 14), background="#e1e6f2")
        self.prediction_label.pack(pady=10)

    def preprocess_image(self, image_path, img_height=128, img_width=128):
        """Image preprocessing function from the first script"""
        img = Image.open(image_path).convert('RGB').resize((img_width, img_height))
        img_array = np.array(img, dtype=np.float32) / 255.0
        return np.expand_dims(img_array, axis=0)

    def predict_image(self, file_path):
        """Prediction logic for recognizing Brain, Hands, Lung, and Kidney"""
        if not self.model:
            messagebox.showerror("Error", "Model not loaded")
            return "Error", 0

        # Preprocess the image
        image_data = self.preprocess_image(file_path)
        
        # Make prediction
        prediction = list(self.model.predict(image_data)[0])
        
        # Initialize variables
        i = 0
        answer = prediction[0]
        
        # Dictionary with organs
        organs = {0: "Brain", 1: "Hands", 2: "Lung", 3: "Kidney"}
        
        # Find the highest prediction
        for num in prediction:
            if num > answer:
                answer = num
                i = prediction.index(answer)
        
        return organs[i], answer * 100


    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg")]
        )
        if not file_path:
            return

        try:
            # Open and prepare the image
            img = Image.open(file_path)
            img.thumbnail((600, 600))  # Resize for display
            self.canvas.original_image = img
            self.canvas.display_image = img

            # Display the image
            self.display_image_on_canvas()

            # Reset zoom and panning
            self.zoom_factor = 1.0
            self.pan_x, self.pan_y = 0, 0

            # Reset contrast and brightness scales
            self.contrast_scale.set(1.0)
            self.brightness_scale.set(1.0)

            # Predict the image
            predicted_organ, confidence = self.predict_image(file_path)
            prediction_text = f"Prediction: {predicted_organ} ({confidence:.2f}% confidence)"
            self.prediction_label.config(text=prediction_text)

            # Save to history
            self.history.append((file_path, predicted_organ, confidence))
            self.update_history_tab()

        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")

    def display_image_on_canvas(self):
        """Render the image on the canvas based on the zoom factor and pan offsets."""
        if not hasattr(self.canvas, "display_image"):
            return

        # Resize the image
        img = self.canvas.display_image.resize(
            (int(self.canvas.display_image.width * self.zoom_factor), 
             int(self.canvas.display_image.height * self.zoom_factor)),
            Image.Resampling.LANCZOS
        )

        # Convert to PhotoImage for Tkinter
        self.canvas.image_tk = ImageTk.PhotoImage(img)

        # Calculate bounds
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width = img.width
        img_height = img.height

        max_pan_x = max((img_width - canvas_width) // 2, 0)
        max_pan_y = max((img_height - canvas_height) // 2, 0)

        pan_x_bound = max(-max_pan_x, min(self.pan_x, max_pan_x))
        pan_y_bound = max(-max_pan_y, min(self.pan_y, max_pan_y))

        self.pan_x = pan_x_bound
        self.pan_y = pan_y_bound

        # Clear the canvas and draw the image centered
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2 + self.pan_x, 
                                 canvas_height // 2 + self.pan_y, 
                                 anchor=tk.CENTER, image=self.canvas.image_tk)

    def apply_adjustments(self):
        """Apply zoom, contrast, and brightness cumulatively to the original image."""
        if not hasattr(self.canvas, "original_image"):
            return

        # Start with the original image
        img = self.canvas.original_image

        # Adjust contrast
        contrast_value = float(self.contrast_scale.get())
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(contrast_value)

        # Adjust brightness
        brightness_value = float(self.brightness_scale.get())
        brightness_enhancer = ImageEnhance.Brightness(img)
        img = brightness_enhancer.enhance(brightness_value)

        # Apply zoom
        width, height = img.size
        img = img.resize(
            (int(width * self.zoom_factor), int(height * self.zoom_factor)),
            Image.Resampling.LANCZOS
        )

        # Update the display image and redraw it on the canvas
        self.canvas.display_image = img
        self.display_image_on_canvas()

    def adjust_contrast(self, value):
        """Adjust the contrast and apply all adjustments."""
        self.apply_adjustments()

    def adjust_brightness(self, value):
        """Adjust the brightness and apply all adjustments."""
        self.apply_adjustments()

    def zoom_in(self):
        """Increase the zoom factor and apply all adjustments."""
        self.zoom_factor *= 1.1
        self.apply_adjustments()

    def zoom_out(self):
        """Decrease the zoom factor and apply all adjustments."""
        self.zoom_factor /= 1.1
        self.apply_adjustments()

    def start_drag(self, event):
        """Record the starting point for panning."""
        self.canvas.start_x = event.x
        self.canvas.start_y = event.y

    def drag_image(self, event):
        """Handle image dragging, ensuring it doesn't go out of bounds."""
        dx = event.x - self.canvas.start_x
        dy = event.y - self.canvas.start_y

        self.pan_x += dx
        self.pan_y += dy

        self.display_image_on_canvas()

        self.canvas.start_x = event.x
        self.canvas.start_y = event.y

    def update_history_tab(self):
        """Update the history tab with the latest prediction results."""
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not self.history:
            Label(self.history_frame, text="No history available.", 
                  font=("Helvetica", 12), bg="#f7f7f7").pack(pady=20)
            return

        for i, (file_path, organ, confidence) in enumerate(self.history):
            frame = tk.Frame(self.history_frame, bg="#ffffff", relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, padx=10, pady=5)

            Label(frame, text=f"{i + 1}. File: {os.path.basename(file_path)}", 
                  font=("Helvetica", 10), bg="#ffffff").pack(anchor="w", padx=5, pady=2)
            Label(frame, text=f"Prediction: {organ}", 
                  font=("Helvetica", 10), bg="#ffffff").pack(anchor="w", padx=5)
            Label(frame, text=f"Confidence: {confidence:.2f}%", 
                  font=("Helvetica", 10), bg="#ffffff").pack(anchor="w", padx=5)

def main():
    root = tk.Tk()
    app = ImagePredictionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()