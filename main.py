import whisper
import os
import shutil
import cv2
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip
from tqdm import tqdm

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_THICKNESS = 2

class VideoTranscriber:
    def __init__(self, model_path, video_path):
        self.model = whisper.load_model(model_path)
        self.video_path = video_path
        self.audio_path = ''
        self.text_array = []
        self.fps = 0
        self.char_width = 0

    def transcribe_video(self):
        """
        Transcribes the video using the loaded model and extracts necessary information for text rendering.
        """
        print('Transcribing video')
        try:
            result = self.model.transcribe(self.audio_path)
            text = result["segments"][0]["text"]
            textsize = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)[0]
            cap = cv2.VideoCapture(self.video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            aspect_ratio = 16/9
            ret, frame = cap.read()
            width = frame[:, int(int(width - 1 / aspect_ratio * height) / 2):width - int((width - 1 / aspect_ratio * height) / 2)].shape[1]
            width = width - (width * 0.1)
            self.fps = cap.get(cv2.CAP_PROP_FPS)
            self.char_width = int(textsize[0] / len(text))
            
            for j in tqdm(result["segments"]):
                lines = []
                text = j["text"]
                end = j["end"]
                start = j["start"]
                total_frames = int((end - start) * self.fps)
                start = start * self.fps
                total_chars = len(text)
                words = text.split(" ")
                i = 0
                
                while i < len(words):
                    words[i] = words[i].strip()
                    if words[i] == "":
                        i += 1
                        continue
                    length_in_pixels = (len(words[i]) + 1) * self.char_width
                    remaining_pixels = width - length_in_pixels
                    line = words[i] 
                    
                    while remaining_pixels > 0:
                        i += 1 
                        if i >= len(words):
                            break
                        length_in_pixels = (len(words[i]) + 1) * self.char_width
                        remaining_pixels -= length_in_pixels
                        if remaining_pixels < 0:
                            continue
                        else:
                            line += " " + words[i]
                    
                    line_array = [line, int(start) + 15, int(len(line) / total_chars * total_frames) + int(start) + 15]
                    start = int(len(line) / total_chars * total_frames) + int(start)
                    lines.append(line_array)
                    self.text_array.append(line_array)
            
            cap.release()
            print('Transcription complete')
        except Exception as e:
            print(f"Error during transcription: {e}")

    def extract_audio(self):
        """
        Extracts audio from the input video file.
        """
        print('Extracting audio')
        try:
            audio_path = os.path.join(os.path.dirname(self.video_path), "audio.mp3")
            video = VideoFileClip(self.video_path)
            audio = video.audio 
            audio.write_audiofile(audio_path)
            self.audio_path = audio_path
            print('Audio extracted')
        except Exception as e:
            print(f"Error during audio extraction: {e}")

    def extract_frames(self, output_folder):
        """
        Extracts frames from the input video file and overlays text on frames based on transcribed data.
        """
        print('Extracting frames')
        try:
            cap = cv2.VideoCapture(self.video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            aspect_ratio = width / height
            N_frames = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = frame[:, int(int(width - 1 / aspect_ratio * height) / 2):width - int((width - 1 / aspect_ratio * height) / 2)]
                
                for i in self.text_array:
                    if N_frames >= i[1] and N_frames <= i[2]:
                        text = i[0]
                        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                        text_x = int((frame.shape[1] - text_size[0]) / 2)
                        text_y = int(height/2)
                        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        break
                
                cv2.imwrite(os.path.join(output_folder, str(N_frames) + ".jpg"), frame)
                N_frames += 1
            
            cap.release()
            print('Frames extracted')
        except Exception as e:
            print(f"Error during frame extraction: {e}")

    def create_video(self, output_video_path):
        """
        Creates a video with text overlays based on extracted frames and audio.
        """
        print('Creating video')
        try:
            image_folder = os.path.join(os.path.dirname(self.video_path), "frames")
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            
            self.extract_frames(image_folder)
            
            images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
            images.sort(key=lambda x: int(x.split(".")[0]))
            
            frame = cv2.imread(os.path.join(image_folder, images[0]))
            height, width, layers = frame.shape
            
            clip = ImageSequenceClip([os.path.join(image_folder, image) for image in images], fps=self.fps)
            audio = AudioFileClip(self.audio_path)
            clip = clip.set_audio(audio)
            clip.write_videofile(output_video_path)
            shutil.rmtree(image_folder)
            os.remove(os.path.join(os.path.dirname(self.video_path), "audio.mp3"))
        except Exception as e:
            print(f"Error creating video: {e}")

# Example usage
# model_path = "base"
# video_path = "test_videos/videoplayback.mp4"
# output_video_path = "output.mp4"
# output_audio_path = "test_videos/audio

if __name__ == "__main__":
    model_path = "base"
    video_path = "test_videos/videoplayback.mp4"
    output_video_path = "output.mp4"

    transcriber = VideoTranscriber(model_path, video_path)
    transcriber.extract_audio()
    transcriber.transcribe_video()
    transcriber.create_video(output_video_path)
