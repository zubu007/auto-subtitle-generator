#Using customtkinter for UI 
from customtkinter import *
from tkinter import filedialog
import main

#creating the window
app  = CTk ()
app.title("Auto subtitle generator")
app.geometry("500x400")

processLabel = CTkLabel(master=app, text="...",font=("Arial" , 20), text_color="#FFCC70")
processLabel.place(relx=0.5, rely=0.8,anchor="center")
#Event handling
def Browse():
    main.video_path = filedialog.askopenfilename()

def ProcessVideo ():
    processLabel.configure(text="Creating video... ")
    processLabel.update()
    main.transcriber = main.VideoTranscriber(main.model_path, main.video_path)
    main.transcriber.extract_audio()
    main.transcriber.transcribe_video()
    main.transcriber.create_video(main.output_video_path)
    processLabel.configure(text="Video created at: " + main.output_video_path)
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

#Process video
processBtn = CTkButton(master=app,text="Process video",command=ProcessVideo)
processBtn.place(relx=0.5, rely=0.7,anchor="center")



app.mainloop()

