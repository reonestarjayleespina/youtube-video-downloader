# 🎬 YouTube Video Downloader - Quick Visual Guide

## 📊 System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        YOUR COMPUTER                           │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         BROWSER (http://127.0.0.1:5173)                 │ │
│  │                                                          │ │
│  │  ┌────────────────────────────────────────────────────┐ │ │
│  │  │  ╔═══════════════════════════════════════════════╗ │ │ │
│  │  │  ║                                               ║ │ │ │
│  │  │  ║    🎨 Vue 3 + Tailwind Glassmorphism UI      ║ │ │ │
│  │  │  ║                                               ║ │ │ │
│  │  │  ║   ┌─────────────────────────────────────┐    ║ │ │ │
│  │  │  ║   │  YouTube URL Input [          ]    │    ║ │ │ │
│  │  │  ║   └─────────────────────────────────────┘    ║ │ │ │
│  │  │  ║                                               ║ │ │ │
│  │  │  ║   ┌────────────────────────────────────────┐ ║ │ │ │
│  │  │  ║   │  🎥 Video Preview (Thumbnail)         │ ║ │ │ │
│  │  │  ║   │  Title: Rick Astley - Never Gonna...   │ ║ │ │ │
│  │  │  ║   │  Duration: 3m 32s                      │ ║ │ │ │
│  │  │  ║   └────────────────────────────────────────┘ ║ │ │ │
│  │  │  ║                                               ║ │ │ │
│  │  │  ║   ┌──────────┬──────────┬──────────────────┐ ║ │ │ │
│  │  │  ║   │  4K      │  1440p   │  1080p           │ ║ │ │ │
│  │  │  ║   │  (2160p) │  (2K)    │   (Selected)     │ ║ │ │ │
│  │  │  ║   └──────────┴──────────┴──────────────────┘ ║ │ │ │
│  │  │  ║                                               ║ │ │ │
│  │  │  ║   ┌────────────────────────────────────────┐ ║ │ │ │
│  │  │  ║   │ [📥 Download Now] ↓ 100%              │ ║ │ │ │
│  │  │  ║   └────────────────────────────────────────┘ ║ │ │ │
│  │  │  ║                                               ║ │ │ │
│  │  │  ║   Download History:                           ║ │ │ │
│  │  │  ║   • Video 1 (1080p) - 2h ago                ║ │ │ │
│  │  │  ║   • Video 2 (720p) - 5h ago                 ║ │ │ │
│  │  │  ║                                               ║ │ │ │
│  │  │  ╚═══════════════════════════════════════════════╝ │ │ │
│  │  │                                                    │ │ │
│  │  └────────────────────────────────────────────────────┘ │ │
│  │                         ▲                                │ │
│  │                         │ (HTTP)                         │ │
│  │                         │ Axios                          │ │
│  │                         │                                │ │
│  └─────────────────────────┼────────────────────────────────┘ │
│                            │                                  │
│                            ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │         BACKEND (http://127.0.0.1:8000)                │ │
│  │                                                         │ │
│  │  ╔════════════════════════════════════════════════════╗ │ │
│  │  ║         FastAPI Python Server                      ║ │ │
│  │  ║                                                    ║ │ │
│  │  ║  POST /get-formats                                ║ │ │
│  │  ║  ├─→ Validate URL                                 ║ │ │
│  │  ║  ├─→ Use yt-dlp to extract video info             ║ │ │
│  │  ║  ├─→ Get thumbnail, duration, formats             ║ │ │
│  │  ║  └─→ Return JSON with available resolutions       ║ │ │
│  │  ║                                                    ║ │ │
│  │  ║  POST /download                                   ║ │ │
│  │  ║  ├─→ Download video stream (selected format)      ║ │ │
│  │  ║  ├─→ Download best audio stream                   ║ │ │
│  │  ║  ├─→ Use FFmpeg to merge video + audio            ║ │ │
│  │  ║  └─→ Save as MP4 in downloads/ folder             ║ │ │
│  │  ║                                                    ║ │ │
│  │  ║  GET /status                                      ║ │ │
│  │  ║  └─→ Return download folder statistics            ║ │ │
│  │  ║                                                    ║ │ │
│  │  ╚════════════════════════════════════════════════════╝ │ │
│  │                         │                                │ │
│  │              ┌──────────┴──────────┐                     │ │
│  │              ▼                     ▼                     │ │
│  │          ┌────────────┐       ┌──────────┐              │ │
│  │          │  yt-dlp    │       │ FFmpeg   │              │ │
│  │          │ (YouTube   │       │ (Merge   │              │ │
│  │          │  extractor)│       │  audio)  │              │ │
│  │          └────────────┘       └──────────┘              │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                            │                                  │
│                            ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         📁 backend/downloads/                        │   │
│  │                                                      │   │
│  │  Rick Astley - Never Gonna Give You Up.mp4          │   │
│  │  Ed Sheeran - Shape of You.mp4                      │   │
│  │  Taylor Swift - Anti-Hero.mp4                       │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Download Flow

```
1. USER INPUT
   │
   └─→ "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        │
        ▼
2. FRONTEND
   │
   ├─→ Validate URL (check for youtube.com/youtu.be)
   │
   └─→ Call: POST /get-formats
        │
        ▼
3. BACKEND - FETCH INFO
   │
   ├─→ Use yt-dlp to extract video data
   │
   ├─→ Get: Title, Thumbnail, Duration, All Formats
   │
   ├─→ Filter unique resolutions (1080p, 720p, etc.)
   │
   └─→ Return JSON response
        │
        ▼
4. FRONTEND - DISPLAY
   │
   ├─→ Show video thumbnail
   │
   ├─→ Show video title & duration
   │
   └─→ Show resolution grid (clickable cards)
        │
        ▼
5. USER SELECTION
   │
   └─→ Click "1080p" (or other resolution)
        │
        ▼
6. FRONTEND
   │
   └─→ Call: POST /download
       ├─→ URL: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
       └─→ Format ID: "22"
            │
            ▼
7. BACKEND - DOWNLOAD & MERGE
   │
   ├─→ Download video stream (format_id: 22)
   │
   ├─→ Download best audio stream
   │
   ├─→ Use FFmpeg to merge video + audio:
   │   ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a aac output.mp4
   │
   └─→ Save to: backend/downloads/[VideoTitle].mp4
        │
        ▼
8. FRONTEND - SUCCESS
   │
   ├─→ Show "Download complete!" message
   │
   ├─→ Add to History (localStorage)
   │
   └─→ Display: "Rick Astley - Never Gonna Give You Up.mp4"
        │
        ▼
9. USER
   │
   └─→ Video file is ready in backend/downloads/
       Can be played with any media player
```

---

## 📱 Frontend Structure

```
App.vue (Main Component)
│
├── 🎨 Template (HTML)
│   ├── Header Section
│   │   └─ "YouTube Downloader" with gradient text
│   │
│   ├── Main Content (Grid Layout)
│   │   ├── Left Column (2/3 width)
│   │   │   ├── URL Input Card (glass effect)
│   │   │   │   ├─ Input field
│   │   │   │   ├─ Check button
│   │   │   │   └─ Error messages
│   │   │   │
│   │   │   ├── Video Preview Card (if loaded)
│   │   │   │   ├─ Video thumbnail
│   │   │   │   ├─ Title
│   │   │   │   └─ Duration
│   │   │   │
│   │   │   └── Resolution Grid (clickable cards)
│   │   │       ├─ 4K button
│   │   │       ├─ 1440p button
│   │   │       ├─ 1080p button
│   │   │       └─ ... more resolutions
│   │   │
│   │   └── Right Column (1/3 width - Sticky Sidebar)
│   │       ├── Download Card
│   │       │   ├─ Download button
│   │       │   ├─ Progress bar
│   │       │   └─ Success message
│   │       │
│   │       ├── History Card (scrollable)
│   │       │   ├─ Previous download 1
│   │       │   ├─ Previous download 2
│   │       │   └─ Clear button
│   │       │
│   │       └── Info Card
│   │           └─ "How it works" steps
│   │
│   └── Background (Fixed)
│       └─ Animated blob gradients
│
├── 📝 Script (JavaScript)
│   ├── State Variables (ref)
│   │   ├── youtubeUrl
│   │   ├── videoInfo
│   │   ├── selectedFormat
│   │   ├── loading
│   │   ├── downloading
│   │   ├── downloadProgress
│   │   ├── downloadSuccess
│   │   ├── downloadHistory
│   │   └── error
│   │
│   ├── Lifecycle Hooks
│   │   └── onMounted() - Load history from localStorage
│   │
│   └── Methods
│       ├── fetchFormats() - POST /get-formats
│       ├── downloadVideo() - POST /download
│       ├── clearHistory() - Clear localStorage
│       ├── formatDuration() - Convert seconds to time
│       └── formatDate() - Format timestamps
│
└── 🎨 Style (CSS)
    ├── Tailwind utilities
    ├── Custom animations
    │   ├─ @keyframes fadeInScale
    │   ├─ @keyframes blob
    │   └─ @keyframes pulse
    └── Glassmorphism classes
        ├─ .glass (main containers)
        └─ .glass-subtle (sidebar)
```

---

## 🛠️ Backend Structure

```
main.py (FastAPI Application)
│
├── 📦 Imports & Config
│   ├── FastAPI, CORS, Pydantic
│   ├── yt-dlp library
│   └── DOWNLOADS_FOLDER setup
│
├── 📋 Pydantic Models (Data Validation)
│   ├── URLRequest (input: url)
│   ├── DownloadRequest (input: url, format_id)
│   ├── FormatInfo (output: format_id, resolution, ext, filesize_mb)
│   ├── VideoInfo (output: title, thumbnail, duration, formats)
│   └── DownloadResponse (output: status, filename, message)
│
├── 🔧 Helper Functions
│   ├── is_valid_youtube_url()
│   │   └─ Check if URL contains youtube.com/youtu.be
│   │
│   ├── get_video_info()
│   │   └─ Use yt-dlp to extract video metadata
│   │
│   └── extract_unique_formats()
│       └─ Filter and group formats by resolution
│
├── 🌐 FastAPI App Setup
│   ├── Create app instance
│   ├── Add CORS middleware (allow all origins)
│   └── Setup lifespan events
│
├── 📡 API Endpoints
│   │
│   ├── GET /
│   │   └─ Return API information and available endpoints
│   │
│   ├── POST /get-formats
│   │   ├─ Receive: YouTube URL
│   │   ├─ Process: Extract video info using yt-dlp
│   │   └─ Return: VideoInfo (title, thumbnail, formats)
│   │
│   ├── POST /download
│   │   ├─ Receive: URL + format_id
│   │   ├─ Download: Video stream + best audio
│   │   ├─ Merge: Use FFmpeg to combine
│   │   ├─ Save: To downloads/ folder as MP4
│   │   └─ Return: DownloadResponse (status, filename)
│   │
│   ├── GET /downloads/{filename}
│   │   ├─ Security: Prevent directory traversal
│   │   ├─ Verify: File exists in downloads folder
│   │   └─ Return: MP4 file as binary
│   │
│   └── GET /status
│       └─ Return: Number of videos, total size, folder path
│
└── ⚠️ Error Handlers
    ├── HTTPException handler
    └── General Exception handler
```

---

## 🎯 User Journey Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    START: User Opens Browser                    │
│                  http://127.0.0.1:5173                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  See Glasmorphism UI       │
        │  With input field          │
        └────────┬───────────────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │ Paste YouTube URL        │
    │ Click "Check" button     │
    └────────┬─────────────────┘
             │
             ▼
    ┌──────────────────────────┐
    │ Loading spinner shows    │
    │ (fetching info...)       │
    └────────┬─────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ Video preview appears            │
    │ • Thumbnail                      │
    │ • Title                          │
    │ • Duration                       │
    │ • Available resolutions          │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ Click resolution card            │
    │ (e.g., "1080p")                  │
    │ Card highlights with blue border │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ Click "Download Now" button      │
    │ (becomes green, with spinner)    │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ Progress bar animates 0 → 100%   │
    │ Shows download is happening      │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ Download complete!               │
    │ Green success notification       │
    │ Shows filename saved             │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ Entry added to Download History  │
    │ • Title                          │
    │ • Resolution selected            │
    │ • Timestamp                      │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ File saved to:                   │
    │ backend/downloads/               │
    │ [Video Title].mp4                │
    │                                  │
    │ Ready to watch! 🎬               │
    └──────────────────────────────────┘
```

---

## 🚀 Run Commands

### Windows
```
Step 1: setup.bat
Step 2: Terminal 1: start_backend.bat
Step 3: Terminal 2: start_frontend.bat
Step 4: Open: http://127.0.0.1:5173
```

### macOS/Linux
```
Step 1: ./setup.sh
Step 2: Terminal 1: ./start_backend.sh
Step 3: Terminal 2: ./start_frontend.sh
Step 4: Open: http://127.0.0.1:5173
```

---

## 📦 File Locations After Download

```
backend/downloads/
│
├── Rick Astley - Never Gonna Give You Up (Official Video).mp4
├── Taylor Swift - Anti-Hero (Official Video).mp4
├── Ed Sheeran - Shape of You (Official Video).mp4
│
└── ... more downloaded videos
```

Each file:
- ✅ Named with video title
- ✅ Format: MP4 (merged video + audio)
- ✅ Quality: User-selected resolution
- ✅ Audio: Best available quality
- ✅ Ready to play in any media player

---

## 🎉 Summary

**What it does:**
1. User provides YouTube URL
2. Frontend displays available video qualities with thumbnail
3. User selects preferred resolution
4. Backend downloads video + audio and merges them
5. File saved as MP4 with video title
6. User can download via browser

**Tech Stack:**
- **Backend:** FastAPI + yt-dlp + FFmpeg
- **Frontend:** Vue 3 + Tailwind CSS + Axios
- **Communication:** REST API over HTTP

**Result:**
A professional, full-stack YouTube downloader with beautiful UI!

🚀 Ready to use - Just run the scripts! 🚀

