#     auto-subtitle-generator
A program that generates subtitles in the format of instagram and facebook reels, youtube shorts and tiktok videos.
*** 
### Installation and usage:
1. If using git to download repo type: `git clone https://github.com/zubu007/auto-subtitle-generator.git` 
2. Check if you have [ffmpeg](https://ffmpeg.org) installed on your system
   * Open a terminal and type `ffmpeg -version`. If you get an error, you need to install ffmpeg.

3. Install [ffmpeg](https://ffmpeg.org)
   * On Windows
     * Install [Chocolately](https://chocolatey.org/install) and type `choco install ffmpeg` 
   * On Linux
     * `sudo apt install ffmpeg`
   * On Mac
     * `brew install ffmpeg`
       
4. Install the necessary python packages in your environment using `pip install -r requirements.txt`

5. Run the python script
   * Windows:  `python GUI.py`
   * Linux/Mac:  `python3 GUI.py`


*** 

### TODO
- [ ] Add comments to the code
- [ ] Update this read.me to make professional

- [ ] add preview of the options selected.
- [ ] Fix audio sync issue. (Maybe FPS is the problem.)

### Done
- [x] configure font color selection to the main loop
- [x] configure text size selection to the main loop
- [x] configure font style selection to the main loop
- [x] Add option for y position of the text
- [x] Create a GUI for the program
- [x] Design UI for the program
- [x] Create variables for text size and font.
- [x] Text alignment in middle

### Issues
* Fix overlapping text in the subtitles.
