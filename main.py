import whisper
import re
import subprocess
import os
import shutil
import cv2
from moviepy import ImageSequenceClip, AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip
from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm
import pysrt

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_THICKNESS = 2

class VideoTranscriber:
    def __init__(self, model_path, video_path, text_color, text_size, text_font, y_axis=0):
        self.model = whisper.load_model(model_path)
        self.video_path = video_path
        self.text_color = text_color
        self.text_size = text_size
        # self.text_font = text_font
        self.text_font = "/System/Library/Fonts/Apple Symbols.ttf"
        self.y_axis = y_axis

        # self.audio_path = ''
        self.sub_texts = []
        # self.fps = 0
        # self.char_width = 0
        # self.max_width = 0
        self.video = VideoFileClip(video_path)
        self.width = self.video.w
        self.height = self.video.h

    def transcribe_video(self):
        print('Transcribing video')
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file {self.video_path} does not exist.")
        # Detect silence offset
        silence_offset = self.detect_silence_offset(self.video_path)
        result = self.model.transcribe(self.video_path, task="transcribe")
        text_array = result['segments']
        if silence_offset > 0:
            text_array[0]['start'] += silence_offset

        sub_clips = []
        for seg in tqdm(text_array, desc="Creating text clips"):
            # txt = TextClip(
            #     seg["text"],
            #     fontsize= self.text_size,
            #     color= self.text_color,
            #     font= self.text_font,
            #     method="caption",
            #     size=(self.width - 100, None),  # autowrap
            #     bg_color="black"
            # )
            # wrapped_text = self.wrap_text_to_width(seg["text"], self.text_font, self.text_size, self.width - 100)
            txt = TextClip(
                text=seg["text"],
                font_size=self.text_size,
                color=self.text_color,
                font=self.text_font, # Add font file path here
                method="caption",
                size=(self.width - 100, None),  # autowrap
                bg_color="black"
            )
            txt = txt.with_start(seg["start"]) \
                     .with_duration(seg["end"] - seg["start"]) \
                     .with_position(("center", self.height - 50 - self.y_axis))
            sub_clips.append(txt)
        self.sub_texts = sub_clips

    def detect_silence_offset(self, file_path, noise_threshold="-30dB", min_silence=0.5):
        """
        Returns the end of the initial silence (in seconds), or 0 if none found.
        """
        cmd = [
            "ffmpeg", "-i", file_path,
            "-af", f"silencedetect=noise={noise_threshold}:d={min_silence}",
            "-f", "null", "-"
        ]
        
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        _, stderr = process.communicate()
        
        # Look for "silence_end"
        matches = re.findall(r"silence_end:\s*([0-9.]+)", stderr)
        if matches:
            return float(matches[0])  # First silence_end = start of speech
        return 0.0

    def create_video_with_subtitles(self, output_video_path=None, subtitles=None):
        print('Creating video with subtitles')
        if not self.sub_texts:
            raise ValueError("No subtitles available. Please transcribe the video first.")
        
        # Determine the video path to use
        video_clip = self.video if not output_video_path else VideoFileClip(output_video_path)

        # Create a composite video with subtitles
        subtitle_clips = CompositeVideoClip([video_clip] + self.sub_texts).with_duration(video_clip.duration)
        print("main clip duration:", video_clip.duration)
        # print("subtitle clip duration:", self.sub_texts.duration)
        
        # Write the final video file
        output_path = self.video_path + "_with_subtitles.mp4" if not output_video_path else output_video_path
        subtitle_clips.write_videofile(output_path, codec="libx264", audio_codec="aac", audio=True, fps=video_clip.fps)
        print('Video with subtitles created successfully')

    def wrap_text_to_width(self, text, font_path, font_size, max_width):
        font = ImageFont.truetype(font_path, font_size)
        lines = []
        words = text.split()
        current_line = ""

        def get_text_width(text):
            dummy_img = Image.new("RGB", (1, 1))
            draw = ImageDraw.Draw(dummy_img)
            bbox = draw.textbbox((0, 0), text, font=font)
            return bbox[2] - bbox[0]

        for word in words:
            test_line = current_line + " " + word if current_line else word
            if get_text_width(test_line) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    # def extract_audio(self):
    #     print('Extracting audio')
    #     audio_path = os.path.join(os.path.dirname(self.video_path), "audio.mp3")
    #     video = VideoFileClip(self.video_path)
    #     audio = video.audio 
    #     audio.write_audiofile(audio_path)
    #     self.audio_path = audio_path
    #     print('Audio extracted')
    
    # def extract_frames(self, output_folder):
    #     print('Extracting frames')
    #     cap = cv2.VideoCapture(self.video_path)
    #     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     self.width = width
    #     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     # asp = width / height
    #     self.max_width = int(width * 0.8)  # Set max width for text wrapping 
    #     # get the frames per second
    #     self.fps = int(cap.get(cv2.CAP_PROP_FPS))
    #     N_frames = 0
    #     
    #     while True:
    #         ret, frame = cap.read()
    #         if not ret:
    #             break
    #         
    #         # frame = frame[:, int(int(width - 1 / asp * height) / 2):width - int((width - 1 / asp * height) / 2)]
    #         
    #         for segment in self.text_array:
    #             start_frame = int(segment['start'] * self.fps)
    #             end_frame = int(segment['end'] * self.fps)
    #             if N_frames >= start_frame and N_frames <= end_frame:
    #                 text = segment['text'].strip()
    #                 if text:
    #                     # Calculate position for text
    #                     org = (10, height - 10 - self.y_axis)  # Bottom-left corner with y-axis offset
    #                     color = self.text_color
    #                     self.put_multiline_text(frame, text, org, FONT, self.text_size, color, FONT_THICKNESS, self.max_width)
    #         cv2.imwrite(os.path.join(output_folder, str(N_frames) + ".jpg"), frame)
    #         N_frames += 1
    #     
    #     cap.release()
    #     print('Frames extracted')

    def wrap_text(self, text, font, font_scale, thickness, max_width):
        """
        Splits text into multiple lines so it fits inside max_width.
        """
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            (w, h), _ = cv2.getTextSize(test_line, font, font_scale, thickness)
            if w <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    # def put_multiline_text(self, img, text, org, font, font_scale, color, thickness, max_width, line_spacing=10):
    #     """
    #     Draw wrapped text (multi-line) on an image using cv2.putText.
    #     org = (x, y) top-left corner of the text block.
    #     """
    #     x, y = org
    #     lines = self.wrap_text(text, font, font_scale, thickness, max_width)

    #     for line in lines:
    #         (w, h), _ = cv2.getTextSize(line, font, font_scale, thickness)
    #         x_centered = (self.width - w) // 2
    #         cv2.putText(img, line, (x_centered, y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
    #         y += h + line_spacing  # move down for next line

    # def create_video(self, output_video_path):
    #     print('Creating video')
    #     image_folder = os.path.join(os.path.dirname(self.video_path), "frames")
    #     if not os.path.exists(image_folder):
    #         os.makedirs(image_folder)
    #     
    #     self.extract_frames(image_folder)
    #     
    #     images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    #     images.sort(key=lambda x: int(x.split(".")[0]))
    #     
    #     frame = cv2.imread(os.path.join(image_folder, images[0]))
    #     height, width, layers = frame.shape
    #     
    #     clip = ImageSequenceClip([os.path.join(image_folder, image) for image in images], fps=self.fps)
    #     audio = AudioFileClip(self.audio_path)
    #     # clip.audio = audio
    #     clip = clip.with_audio(audio)
    #     clip.write_videofile(output_video_path)
    #     shutil.rmtree(image_folder)
    #     # os.remove(os.path.join(os.path.dirname(self.video_path), "audio.mp3"))

