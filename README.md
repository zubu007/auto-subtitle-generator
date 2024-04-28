# Auto Subtitle Generator

Auto Subtitle Generator is a program that generates subtitles in the format of Instagram and Facebook Reels, YouTube Shorts, and TikTok videos.

---

## Installation and Usage

1. If using Git to download the repository, type the following command in your terminal:
   ```bash
   git clone https://github.com/zubu007/auto-subtitle-generator.git
   ```

2. Install [FFmpeg](https://ffmpeg.org):
   - **Windows:**
     - Install [Chocolately](https://chocolatey.org/install) and run:
       ```bash
       choco install ffmpeg
       ```
   - **Linux:**
     ```bash
     sudo apt install ffmpeg
     ```
       
3. Install the necessary Python packages in your environment using pip:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Run the Python script:
   - Windows:
     ```bash
     python main.py
     ```
   - Linux:
     ```bash
     python3 main.py
     ```

## TODO
- [ ] Control number of words shown together with a variable.
- [ ] Add support for multiple languages.
- [ ] Add support for multiple video formats.
- [ ] Add support for multiple video resolutions.
- [ ] Add option to select font color.
- [ ] Font size option.

## Done
- [x] Create a GUI for the program.
- [x] Design UI for the program.
- [x] Create variables for text size and font.
- [x] Update this read.me to make professional.
- [x] Add comments to the code.

