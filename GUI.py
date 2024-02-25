#Using customtkinter for UI 
from customtkinter import *
from tkinter import filedialog
import main

#creating the window
app  = CTk ()
app.title("Auto subtitle generator")
app.geometry("500x400")

#Creating and placing the label that tells the user if a video is being created
processLabel = CTkLabel(master=app, text="",font=("Arial" , 20), text_color="#FFCC70")
processLabel.place(relx=0.5, rely=0.8,anchor="center")

main.video_path = ""

#Event handling
def Browse():
    main.video_path = filedialog.askopenfilename()

def ProcessVideo ():
    if (main.video_path != ""):
        processLabel.configure(text="Creating video... ")
        processLabel.update()
        main.transcriber = main.VideoTranscriber(main.model_path, main.video_path)

        main.transcriber.extract_audio()
        processLabel.configure(text="Extracting audio... ")
        processLabel.update()

        main.transcriber.transcribe_video()
        processLabel.configure(text="Transcribing video... ")
        processLabel.update()

        main.transcriber.create_video(main.output_video_path)
        processLabel.configure(text="Video created at: " + main.output_video_path)
        processLabel.update()
    else:
        processLabel.configure(text="Video file has not been selected")
        processLabel.update()


label = CTkLabel(master=app, text="Select video file",font=("Arial" , 20), text_color="#FFCC70")
label.place(relx=0.5, rely=0.1,anchor="center")

#Browse button
btn = CTkButton(master=app, text="Browse",command=Browse)
btn.place(relx=0.5,rely=0.2,anchor="center")

label = CTkLabel(master=app, text="Select model",font=("Arial" , 20), text_color="#FFCC70")
label.place(relx=0.5, rely=0.3,anchor="center")

model = CTkComboBox(master=app, values=["Whisper" , "Model 1" , "Model 2"])
model.place(relx=0.5, rely=0.4,anchor="center")

font = CTkComboBox(master=app, values=["Arial" , "Times New Roman" , "Courier"])
font.place(relx=0.5, rely=0.5,anchor="center")

#Process video
processBtn = CTkButton(master=app,text="Process video",command=ProcessVideo)
processBtn.place(relx=0.5, rely=0.7,anchor="center")



app.mainloop()

