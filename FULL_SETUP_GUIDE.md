# 🚀 YouTube Video Downloader - Full Stack Setup Guide

A professional full-stack application combining FastAPI backend and Vue 3 frontend with glassmorphism design.

---

## 📋 Table of Contents
1. [Requirements](#requirements)
2. [Quick Start](#quick-start)
3. [Manual Setup](#manual-setup)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)
6. [Project Structure](#project-structure)
7. [Features](#features)

---

## 📦 Requirements

Before starting, ensure you have:

### Essential
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **npm 7+** - Comes with Node.js

### Recommended
- **FFmpeg** - For audio/video merging
  - **Windows**: `winget install FFmpeg.FFmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt-get install ffmpeg`

---

## 🎯 Quick Start (Windows)

### Step 1: Run Setup Script
```bash
setup.bat
```
This will automatically:
- Create Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies

### Step 2: Open Two Terminals

**Terminal 1 - Backend:**
```bash
start_backend.bat
```
You should see:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Frontend:**
```bash
start_frontend.bat
```
You should see:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://127.0.0.1:5173/
```

### Step 3: Open Browser
Navigate to: **http://127.0.0.1:5173**

---

## 🎯 Quick Start (macOS/Linux)

### Step 1: Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Open Two Terminals

**Terminal 1 - Backend:**
```bash
chmod +x start_backend.sh
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
chmod +x start_frontend.sh
./start_frontend.sh
```

### Step 3: Open Browser
Navigate to: **http://127.0.0.1:5173**

---

## 🛠️ Manual Setup (if scripts don't work)

### Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

The backend will run on: **http://127.0.0.1:8000**

### Frontend Setup

```bash
# In a new terminal, navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on: **http://127.0.0.1:5173**

---

## 🚀 Running the Application

### Architecture Overview
```
┌─────────────────────────────────────────┐
│      Browser (http://127.0.0.1:5173)    │
│  ┌─────────────────────────────────┐    │
│  │   Vue 3 + Tailwind Frontend    │    │
│  │  - URL Input                   │    │
│  │  - Format Selection            │    │
│  │  - Download Management         │    │
│  └─────────────────────────────────┘    │
└──────────────────┬──────────────────────┘
                   │ HTTP (axios)
┌──────────────────▼──────────────────────┐
│  FastAPI (http://127.0.0.1:8000)        │
│  ┌─────────────────────────────────┐    │
│  │  POST /get-formats             │    │
│  │  POST /download                │    │
│  │  GET  /downloads/{filename}    │    │
│  └─────────────────────────────────┘    │
│              │                          │
│              ▼                          │
│        yt-dlp + FFmpeg                 │
│       (downloads folder)               │
└─────────────────────────────────────────┘
```

### How It Works

1. **User inputs YouTube URL** in the Vue 3 frontend
2. **Frontend calls** `/get-formats` endpoint
3. **Backend extracts** video information using yt-dlp
4. **Backend returns** available resolutions with thumbnails
5. **User selects** preferred resolution
6. **Frontend calls** `/download` endpoint with selected format
7. **Backend downloads** video + best audio and merges with FFmpeg
8. **File saved** to `backend/downloads/` folder as MP4
9. **User notified** of successful download

---

## 📁 Project Structure

```
Video Downloader/
├── backend/
│   ├── main.py                  # FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── venv/                    # Virtual environment (created by setup)
│   └── downloads/               # Downloaded videos folder
├── frontend/
│   ├── src/
│   │   ├── App.vue             # Main Vue component
│   │   ├── main.js             # Vue entry point
│   │   └── style.css           # Tailwind CSS
│   ├── index.html              # HTML entry point
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js      # Tailwind configuration
│   └── postcss.config.js       # PostCSS configuration
├── setup.bat                    # Windows setup script
├── setup.sh                     # macOS/Linux setup script
├── start_backend.bat           # Windows backend launcher
├── start_frontend.bat          # Windows frontend launcher
├── start_backend.sh            # macOS/Linux backend launcher
├── start_frontend.sh           # macOS/Linux frontend launcher
├── youtube_downloader.py       # Standalone CLI script
├── requirements.txt            # Global dependencies
└── README.md                   # Documentation
```

---

## ✨ Features

### Backend (FastAPI)
- ✅ **GET /** - API information endpoint
- ✅ **POST /get-formats** - Extract video formats with thumbnails
- ✅ **POST /download** - Download with format selection
- ✅ **GET /downloads/{filename}** - Download merged video file
- ✅ **GET /status** - Download folder statistics
- ✅ **CORS enabled** - For frontend communication
- ✅ **Error handling** - Comprehensive error messages
- ✅ **yt-dlp integration** - Latest YouTube support
- ✅ **FFmpeg merging** - High-quality audio/video merge

### Frontend (Vue 3 + Tailwind)
- 🎨 **Glassmorphism Design** - Modern frosted glass UI
- 📱 **Responsive Layout** - Mobile-friendly design
- 🎥 **Video Preview** - Thumbnail and metadata display
- 📊 **Format Grid** - Click to select resolution
- 📥 **Download Manager** - Progress tracking
- 💾 **Download History** - LocalStorage persistence
- ⚡ **Real-time Updates** - Instant format feedback
- 🎯 **Error Handling** - User-friendly messages
- 🌗 **Dark Theme** - Professional dark mode

---

## 🐛 Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows - Find and kill process on port 8000/5173
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### FFmpeg Not Found

**Error:** `FFmpeg not found in PATH`

**Solution:**
1. Install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add to PATH environment variable
3. Restart terminal and verify: `ffmpeg -version`

### Backend Connection Error

**Error:** `Connection refused` when frontend tries to reach backend

**Solutions:**
1. Ensure backend is running on `http://127.0.0.1:8000`
2. Check CORS is enabled in `backend/main.py`
3. Verify both are using `127.0.0.1` (not `localhost`)

### Virtual Environment Issues

**Error:** `venv is not recognized`

**Solution:**
```bash
# Create new virtual environment
python -m venv venv

# Verify activation worked (should show (venv) in prompt)
venv\Scripts\activate.bat  # Windows
source venv/bin/activate   # macOS/Linux
```

### npm Package Installation Failed

**Error:** `npm ERR!` during `npm install`

**Solution:**
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Video Download Issues

**Error:** `Video unavailable` or `private video`

**Solutions:**
- Video may be private or removed
- Try a different YouTube video
- Ensure URL is correct
- Check internet connection
- Try updating yt-dlp: `pip install --upgrade yt-dlp`

---

## 🎨 Customization

### Change API URL
Edit [frontend/src/App.vue](frontend/src/App.vue#L52):
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000'
```

### Change Backend Port
Edit [backend/main.py](backend/main.py#L440):
```python
uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Change Frontend Port
Edit [frontend/vite.config.js](frontend/vite.config.js#L6):
```javascript
server: { port: 5173, host: '127.0.0.1' }
```

### Change Download Folder
Edit [backend/main.py](backend/main.py#L23):
```python
DOWNLOADS_FOLDER = Path(__file__).parent / "downloads"
```

---

## 📊 API Reference

### GET `/` 
Returns API information

**Response:**
```json
{
  "name": "YouTube Downloader API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

### POST `/get-formats`
Extract available video formats

**Request:**
```json
{ "url": "https://www.youtube.com/watch?v=..." }
```

**Response:**
```json
{
  "title": "Video Title",
  "thumbnail": "https://...",
  "duration": 600,
  "formats": [
    {
      "format_id": "22",
      "resolution": "1080p",
      "ext": "mp4",
      "filesize_mb": 125.5
    }
  ]
}
```

### POST `/download`
Download video with selected format

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "format_id": "22"
}
```

**Response:**
```json
{
  "status": "success",
  "filename": "Video Title.mp4",
  "message": "Video downloaded successfully"
}
```

### GET `/downloads/{filename}`
Download merged video file

**Response:** Binary MP4 file

### GET `/status`
Get download folder statistics

**Response:**
```json
{
  "status": "healthy",
  "downloaded_videos": 5,
  "total_size_mb": 2500.5,
  "downloads_folder": "/path/to/downloads"
}
```

---

## 🎓 Portfolio Value

This project demonstrates:
- **Full-stack development** - Backend + Frontend integration
- **Modern UI/UX** - Glassmorphism design patterns
- **Vue 3 expertise** - Composition API, reactive state, hooks
- **FastAPI proficiency** - REST API, CORS, async operations
- **State management** - LocalStorage for history
- **Error handling** - User-friendly error messages
- **Responsive design** - Mobile-first approach
- **Real-world API integration** - yt-dlp library usage
- **Professional code organization** - Clean, modular structure

---

## 📝 License

Free to use for personal and educational purposes.

## ⚖️ Disclaimer

This tool is for downloading videos you own or have permission to download. Please respect copyright laws and YouTube's Terms of Service.

---

## 🚀 Next Steps

For production deployment:
1. Configure CORS to specific domains
2. Add authentication/authorization
3. Implement rate limiting
4. Add database for download history
5. Deploy to cloud (AWS, Heroku, Vercel, etc.)
6. Add progress WebSockets for real-time updates
7. Implement file cleanup/quota system

---

## 📞 Support

For issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Verify all requirements are installed
3. Check browser console for errors (F12)
4. Verify backend is running: `http://127.0.0.1:8000`
5. Review [API Reference](#api-reference)

