#Using customtkinter for UI 
from customtkinter import *
from tkinter import filedialog
import threading as th
from CTkColorPicker import *

#printing message before importing main
print ("Starting...")
from main import VideoTranscriber

#variables
processing = False #checks if the program is processing a video or not
video_path = "" #path to the video file
output_video_path = "" #path to the output video file

#creating the window
app  = CTk ()
app.title("Auto subtitle generator")
#window resolution
app.geometry("500x600")

#Creating and placing the label that tells the user if a video is being created
processLabel = CTkLabel(master=app, text="",font=("Arial" , 20), text_color="#FFCC70")
processLabel.place(relx=0.5, rely=0.9,anchor="center")

#this label is at the very bottom and gives feedback to the player that the program is still running
dotsLabel = CTkLabel(master=app, text="",font=("Arial" , 20), text_color="#FFCC70")
dotsLabel.place(relx=0.5, rely=0.9,anchor="center")

#Creating the button that will open the color picker
def ask_color():
    pick_color = AskColor() # open the color picker
    color = pick_color.get() # get the color string
    color_button.configure(fg_color=color)

#Event handling methods
#Selecting the video
def Browse():
    global video_path, output_video_path
    video_path  = filedialog.askopenfilename()
    output_video_path = video_path.split("/")[-1].split(".")[0] + "_subtitled.mp4"

dots="." #a string that will be used for the Dots() method
count = 0
def Dots (): # This method gives feedback to the player that the program is still running
    global count, dots , processing
    if (processing is True):
        if (count > 15):
            count = -1
            dots = "."
            dotsLabel.configure(text=dots)
            dotsLabel.after(100,Dots)
        else:
            dots = dots + dots[count]
            dotsLabel.configure(text=dots)
            count += 1
            dotsLabel.after(100,Dots)
    else:
        dots = ""
        dotsLabel.configure(text=dots)        

def ProcessVideo (): 
    global processing
    if (video_path != ""):
        processLabel.configure(text="Creating video... ")
        processLabel.update()
        try:
            font_size_value = int(font_size_entry.get())
        except ValueError:
            processLabel.configure(text="Invalid font size. Please enter a number.")
            processLabel.update()
            return

        print("Selected model:", model.get())
        print("Selected font:", font.get())
        print("Selected font size:", font_size_value)
        print("Selected color:", color_button.cget("fg_color"))
        hex_color = color_button.cget("fg_color")
        rgb_color = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        transcriber = VideoTranscriber(model.get(), video_path, rgb_color, font_size_value, font.get(), y_axis=int(y_axis_entry.get()))

        transcriber.extract_audio()
        processLabel.configure(text="Extracting audio... ")
        processLabel.update()

        transcriber.transcribe_video()
        processLabel.configure(text="Transcribing video... ")
        processLabel.update()

        transcriber.create_video(output_video_path)
        processLabel.configure(text="Video created at: " + output_video_path)
        processLabel.update()
        processing = False
    else:
        processLabel.configure(text="Video file has not been selected")
        processLabel.update()

#Threading setup in order to start creating the video
def StartVideoProcess ():
    global processing
    processThread = th.Thread(target=ProcessVideo)
    processThread.start()
    dotsThread = th.Thread(target=Dots)
    processing = True
    dotsThread.start()

label = CTkLabel(master=app, text="Select video file",font=("Arial" , 20), text_color="#FFCC70")
label.place(relx=0.5, rely=0.1,anchor="center")

#Browse button
btn = CTkButton(master=app, text="Browse",command=Browse)
btn.place(relx=0.5,rely=0.2,anchor="center")

label = CTkLabel(master=app, text="Select model",font=("Arial" , 20), text_color="#FFCC70")
label.place(relx=0.5, rely=0.3,anchor="center")

model = CTkComboBox(master=app, values=["tiny.en" , "base.en" , "small.en"])
model.place(relx=0.5, rely=0.4,anchor="center")

font = CTkComboBox(master=app, values=["Arial" , "Times New Roman" , "Courier"])
font.place(relx=0.5, rely=0.5,anchor="center")

font_size_label = CTkLabel(master=app, text="Font size (px)", font=("Arial", 16), text_color="#FFCC70")
font_size_label.place(relx=0.5, rely=0.6, anchor="center")

font_size_entry = CTkEntry(master=app)
font_size_entry.insert(0, "24")
font_size_entry.place(relx=0.5, rely=0.65, anchor="center")

y_axis_label = CTkLabel(master=app, text="Y-axis position (px)", font=("Arial", 16), text_color="#FFCC70")
y_axis_label.place(relx=0.5, rely=0.7, anchor="center")
y_axis_entry = CTkEntry(master=app)
y_axis_entry.insert(0, "50")
y_axis_entry.place(relx=0.5, rely=0.75, anchor="center")

processBtn = CTkButton(master=app, text="Process",command=StartVideoProcess)
processBtn.place(relx=0.5, rely=0.8,anchor="center")

color_button = CTkButton(master=app, text="CHOOSE COLOR", text_color="black", command=ask_color)
color_button.place(relx=0.5, rely=0.85, anchor="center")

app.mainloop()

