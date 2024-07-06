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
- [ ] Control number of words shown together with a variable
- [ ] Add support for multiple languages
- [ ] Add support for multiple video formats
- [ ] Add support for multiple video resolutions
- [ ] Add comments to the code
- [ ] Update this read.me to make professional
- [ ] Add option to select font color
- [ ] Font size option

### Done
- [x] Create a GUI for the program
- [x] Design UI for the program
- [x] Create variables for text size and font.

