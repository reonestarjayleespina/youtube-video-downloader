# YouTube Video Downloader

A Python script for downloading YouTube videos with user-selected quality and automatic audio merging using FFmpeg.

## Features

✓ **URL Validation** - Validates YouTube URLs before processing
✓ **Format Listing** - Displays all available video resolutions (1080p, 1440p, 4K, etc.)
✓ **Format Selection** - Allows users to select specific format IDs
✓ **Audio Merging** - Automatically merges selected video quality with the best available audio
✓ **MP4 Output** - Saves files as MP4 with the video title as filename
✓ **Error Handling** - Comprehensive error handling for invalid URLs and failed downloads
✓ **Progress Tracking** - Shows download progress with speed and ETA

## System Prerequisites

### Windows Users - Complete Setup Guide

#### Step 1: Install Python 3.11+
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT**: Check ✓ "Add Python to PATH" during installation
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

#### Step 2: Install FFmpeg (Required for audio merging)

**Option A: Download & Setup (Recommended)**
1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows
   - Choose "Full build" or "essentials build"
2. Extract to: `C:\ffmpeg` (create folder if needed)
3. **Add to System Environment Variables:**
   - Press `Win + X` → Search "Environment Variables" → "Edit the system environment variables"
   - Click "Environment Variables" button
   - Under "System variables", click "New"
   - Variable name: `FFMPEG_PATH`
   - Variable value: `C:\ffmpeg\bin`
   - Click OK → Apply → OK
   - Add to PATH (if not there already):
     - Select "Path" → Edit → New → `C:\ffmpeg\bin` → OK

4. **Verify FFmpeg is accessible:**
   ```bash
   ffmpeg -version
   ```
   If successful, output should show version info. If you see "ffmpeg is not recognized", restart your terminal and try again.

**Option B: Using Chocolatey (if installed)**
```bash
choco install ffmpeg
ffmpeg -version
```

**Option C: Using Winget (Windows 10/11)**
```bash
winget install FFmpeg.FFmpeg
ffmpeg -version
```

#### Step 3: Install yt-dlp (Required)
```bash
pip install yt-dlp
yt-dlp --version
```

### macOS Prerequisites

1. **Install Homebrew** (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python and FFmpeg:**
   ```bash
   brew install python@3.11 ffmpeg
   python3 --version
   ffmpeg -version
   ```

3. **Install Python dependencies:**
   ```bash
   pip install yt-dlp
   ```

### Linux (Ubuntu/Debian) Prerequisites

```bash
sudo apt update
sudo apt install python3.11 python3-pip ffmpeg
python3 --version
ffmpeg -version
pip install yt-dlp
```

---

## Requirements

- **Python 3.6+** (3.11+ recommended for Windows)
- **yt-dlp** - YouTube video downloader library
- **FFmpeg** - For audio/video merging (required)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install yt-dlp
```

### 2. Install FFmpeg

**Windows:**
- Download from: https://ffmpeg.org/download.html
- Or use Chocolatey: `choco install ffmpeg`
- Or use Winget: `winget install FFmpeg.FFmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg
```

## Usage

Run the script:

```bash
python youtube_downloader.py
```

### Steps:

1. **Enter YouTube URL** - Paste the YouTube video link
2. **View Available Resolutions** - The script displays all available video qualities
3. **Select Format** - Enter the Format ID of your desired quality
4. **Download** - The script downloads the video and merges it with the best audio
5. **Save** - Video is saved as MP4 in the `downloads` folder with the video title

## Example

```
================================================================================
YouTube Video Downloader
================================================================================

Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Fetching video information...
Video Title: Rick Astley - Never Gonna Give You Up (Video)

Available resolutions: 18

================================================================================
#     Format ID       Resolution      FPS      File Size      
================================================================================
1     22              720p            30       ~50.25 MB
2     18              360p            30       ~15.50 MB
3     17              144p            30       ~2.30 MB
================================================================================

Enter the Format ID you want to download (or 'q' to quit): 22
Downloading video with format ID: 22...
Progress: 100.0% at 5.2MB/s ETA: 0:00:00

✓ Download completed successfully!
Saved to: C:\Users\YourName\OneDrive\Desktop\projects\Video Downloader\downloads\Rick Astley - Never Gonna Give You Up (Video).mp4
```

## Error Handling

The script handles the following scenarios:

- **Invalid YouTube URLs** - Validates URL format before processing
- **Video Not Found** - Gracefully handles removed or private videos
- **Download Failures** - Provides error messages if download fails
- **Missing Dependencies** - Alerts user if yt-dlp or FFmpeg is not installed
- **User Interruption** - Handles keyboard interrupt (Ctrl+C) gracefully

## Output

Downloaded videos are saved in the `downloads` folder with the following naming convention:

```
Video Title.mp4
```

## Troubleshooting

### "FFmpeg is not installed"
- Make sure FFmpeg is installed and available in your system PATH
- Verify installation: `ffmpeg -version`

### "Download failed: Video unavailable"
- The video may be private, restricted, or removed
- Try a different YouTube video

### "Invalid YouTube URL"
- Make sure the URL starts with `https://www.youtube.com/` or `https://youtu.be/`
- Copy the full URL from your browser's address bar

### "yt-dlp is not installed"
- Run: `pip install yt-dlp`
- Ensure pip is correctly installed: `pip --version`

## Command-line Alternatives

If you prefer command-line usage without the interactive script:

```bash
# Using yt-dlp directly
yt-dlp -f 22 https://www.youtube.com/watch?v=VIDEO_ID
```

## License

Free to use for personal and educational purposes only.

## Disclaimer

This tool is for downloading videos you own or have permission to download. Please respect copyright laws and YouTube's Terms of Service.
