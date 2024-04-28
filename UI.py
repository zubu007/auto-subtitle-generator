import tkinter as tk
from tkinter import filedialog, messagebox

class VideoProcessor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Video Processing GUI")

        self.models = ["Whisper", "Model 2", "Model 3"]  # Add more models if needed
        self.model_dropdown = tk.StringVar(self.window)
        self.model_dropdown.set(self.models[0])  # Set the default model

        self.setup_ui()

    def process_video(self):
        try:
            # Get the selected video file path
            video_file_path = filedialog.askopenfilename()
            
            if not video_file_path:
                messagebox.showwarning("Warning", "No video file selected.")
                return

            # Get the selected model from the dropdown menu
            selected_model = self.model_dropdown.get()

            # Get the output file name and location
            output_file_path = self.output_entry.get()

            if not output_file_path:
                messagebox.showwarning("Warning", "Please enter an output file path.")
                return

            # Process the video using the selected model and output file path
            # Placeholder for video processing code
            # Add your code here
            
            # Display a success message
            self.result_label.config(text="Video processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing video: {e}")

    def setup_ui(self):
        # Create a label for the video file selection
        video_label = tk.Label(self.window, text="Select Video File:")
        video_label.pack()

        # Create a button to browse and select the video file
        video_button = tk.Button(self.window, text="Browse", command=self.process_video)
        video_button.pack()

        # Create a label for the model selection
        model_label = tk.Label(self.window, text="Select Model:")
        model_label.pack()

        # Create a dropdown menu for model selection
        model_menu = tk.OptionMenu(self.window, self.model_dropdown, *self.models)
        model_menu.pack()

        # Create a label for the output file name and location
        output_label = tk.Label(self.window, text="Output File Name and Location:")
        output_label.pack()

        # Create an entry field for the output file name and location
        self.output_entry = tk.Entry(self.window)
        self.output_entry.pack()

        # Create a button to start the video processing
        process_button = tk.Button(self.window, text="Process Video", command=self.process_video)
        process_button.pack()

        # Create a label to display the result
        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()

    def run(self):
        # Start the GUI event loop
        self.window.mainloop()

if __name__ == "__main__":
    app = VideoProcessor()
    app.run()
