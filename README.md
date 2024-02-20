#     auto-subtitle-generator
A program that generates subtitles in the format of instagram and facebook reels, youtube shorts and tiktok videos.
*** 
### Installation and usage:
1. If using git to download repo type: `git clone https://github.com/zubu007/auto-subtitle-generator.git` 
2. Install [ffmpeg](https://ffmpeg.org)
   * On Windows
     * Install [Chocolately](https://chocolatey.org/install) and type `choco install ffmpeg` 
   * On Linux
     * `sudo apt install ffmpeg`
       
3. Install the necessary python packages in your environment using `pip install -r requirements.txt`
4. Create a folder called `test_videos` in the source and put your video inside with the name `"videoplayback.mp4"` 
5. Run the python script
   * Windows:  `python main.py`
   * Linux:  `python3 main.py`

*** 

### TODO
- [ ] Update this read.me to make professional
- [ ] Add command line inputs using python argument parser
- [ ] Create variables for text size and font.
- [ ] Control number of words shown together with a variable
- [ ] Add support for multiple languages
- [ ] Create a GUI for the program
- [ ] Design UI for the program
- [ ] Add support for multiple video formats
- [ ] Add support for multiple video resolutions
- [ ] Add comments to the code