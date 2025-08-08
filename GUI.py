#Using customtkinter for UI 
from customtkinter import *
from tkinter import filedialog
import threading as th

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
app.geometry("500x400")

#Creating and placing the label that tells the user if a video is being created
processLabel = CTkLabel(master=app, text="",font=("Arial" , 20), text_color="#FFCC70")
processLabel.place(relx=0.5, rely=0.8,anchor="center")

#this label is at the very bottom and gives feedback to the player that the program is still running
dotsLabel = CTkLabel(master=app, text="",font=("Arial" , 20), text_color="#FFCC70")
dotsLabel.place(relx=0.5, rely=0.9,anchor="center")

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
        transcriber = VideoTranscriber(model.get(), video_path)

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

processBtn = CTkButton(master=app, text="Process",command=StartVideoProcess)
processBtn.place(relx=0.5, rely=0.7,anchor="center")

app.mainloop()

