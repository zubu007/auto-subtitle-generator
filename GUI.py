import tkinter as tk
from tkinter import filedialog, messagebox
import threading as th
import main

# Printing message before importing main
print("Starting...")

# Initialize variables
main.video_path = ""
processing = False  # Checks if the program is processing a video or not

# Create the window
app = tk.Tk()
app.title("Auto subtitle generator")
app.geometry("500x400")

# Create and place the label that tells the user if a video is being created
processLabel = tk.Label(master=app, text="", font=("Arial", 20), fg="#FFCC70")
processLabel.place(relx=0.5, rely=0.8, anchor="center")

# This label is at the very bottom and gives feedback to the user that the program is still running
dotsLabel = tk.Label(master=app, text="", font=("Arial", 20), fg="#FFCC70")
dotsLabel.place(relx=0.5, rely=0.9, anchor="center")

# Event handling methods
# Selecting the video
def Browse():
    main.video_path = filedialog.askopenfilename()

dots = "."
count = 0

# This method gives feedback to the user that the program is still running
def Dots():
    global count, dots, processing
    if processing:
        if count > 15:
            count = -1
            dots = "."
        else:
            dots += "."
        dotsLabel.config(text=dots)
        count += 1
        app.after(100, Dots)
    else:
        dots = ""
        dotsLabel.config(text=dots)

def ProcessVideo():
    global processing
    if main.video_path:
        processLabel.config(text="Creating video... ")
        processLabel.update()
        main.transcriber = main.VideoTranscriber(main.model_path, main.video_path)

        main.transcriber.extract_audio()
        processLabel.config(text="Extracting audio... ")
        processLabel.update()

        main.transcriber.transcribe_video()
        processLabel.config(text="Transcribing video... ")
        processLabel.update()

        main.transcriber.create_video(main.output_video_path)
        processLabel.config(text="Video created at: " + main.output_video_path)
        processLabel.update()
        processing = False
    else:
        messagebox.showwarning("Warning", "Video file has not been selected")

def StartVideoProcess():
    global processing
    processThread = th.Thread(target=ProcessVideo)
    processThread.start()
    processing = True
    Dots()

label = tk.Label(master=app, text="Select video file", font=("Arial", 20), fg="#FFCC70")
label.place(relx=0.5, rely=0.1, anchor="center")

btn = tk.Button(master=app, text="Browse", command=Browse)
btn.place(relx=0.5, rely=0.2, anchor="center")

label = tk.Label(master=app, text="Select model", font=("Arial", 20), fg="#FFCC70")
label.place(relx=0.5, rely=0.3, anchor="center")

model = tk.StringVar(app)
model.set("Whisper")  # Set default model
modelMenu = tk.OptionMenu(app, model, "Whisper", "Model 1", "Model 2")
modelMenu.place(relx=0.5, rely=0.4, anchor="center")

font = tk.StringVar(app)
font.set("Arial")  # Set default font
fontMenu = tk.OptionMenu(app, font, "Arial", "Times New Roman", "Courier")
fontMenu.place(relx=0.5, rely=0.5, anchor="center")

processBtn = tk.Button(master=app, text="Process", command=StartVideoProcess)
processBtn.place(relx=0.5, rely=0.7, anchor="center")

app.mainloop()
