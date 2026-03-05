"""
FastAPI Backend for YouTube Video Downloader
Provides endpoints for fetching video information and downloading videos with format selection.
"""

import os
import json
import asyncio
import shutil
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp


# ============================================================================
# Configuration
# ============================================================================

DOWNLOADS_FOLDER = Path(__file__).parent / "downloads"
DOWNLOADS_FOLDER.mkdir(exist_ok=True)

# Find FFmpeg location
def find_ffmpeg():
    """Find ffmpeg executable location"""
    # Try to find in PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # Common Windows installation paths
    common_paths = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
    ]
    
    for path in common_paths:
        if Path(path).exists():
            return path
    
    return None

FFMPEG_LOCATION = find_ffmpeg()

# ============================================================================
# System Dependency Verification
# ============================================================================

class DependencyCheckError(Exception):
    """Custom exception for dependency check failures"""
    pass


def check_system_dependencies() -> dict:
    """
    Check if all required system dependencies are installed and accessible.
    
    Returns:
        dict: Status of each dependency with detailed information
        
    Raises:
        DependencyCheckError: If critical dependencies are missing
    """
    import subprocess
    
    dependencies_status = {
        "ffmpeg": {"installed": False, "version": None, "path": None, "error": None},
        "yt-dlp": {"installed": False, "version": None, "path": None, "error": None}
    }
    
    # Check FFmpeg
    if FFMPEG_LOCATION:
        dependencies_status["ffmpeg"]["path"] = FFMPEG_LOCATION
        try:
            result = subprocess.run(
                [FFMPEG_LOCATION, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                dependencies_status["ffmpeg"]["version"] = version_line
                dependencies_status["ffmpeg"]["installed"] = True
            else:
                dependencies_status["ffmpeg"]["error"] = "FFmpeg found but failed to execute"
        except Exception as e:
            dependencies_status["ffmpeg"]["error"] = str(e)
    else:
        dependencies_status["ffmpeg"]["error"] = (
            "FFmpeg not found in PATH. "
            "Install from https://ffmpeg.org/download.html or run: "
            "winget install FFmpeg.FFmpeg (Windows) / brew install ffmpeg (macOS)"
        )
    
    # Check yt-dlp
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            dependencies_status["yt-dlp"]["version"] = result.stdout.strip()
            dependencies_status["yt-dlp"]["installed"] = True
            # Find yt-dlp path
            import shutil as sh
            yt_dlp_path = sh.which("yt-dlp")
            if yt_dlp_path:
                dependencies_status["yt-dlp"]["path"] = yt_dlp_path
        else:
            dependencies_status["yt-dlp"]["error"] = "yt-dlp found but failed to execute"
    except FileNotFoundError:
        dependencies_status["yt-dlp"]["error"] = (
            "yt-dlp not found. Install with: pip install yt-dlp"
        )
    except Exception as e:
        dependencies_status["yt-dlp"]["error"] = str(e)
    
    return dependencies_status


def verify_dependencies_for_download() -> tuple[bool, str]:
    """
    Verify dependencies before allowing download.
    
    Returns:
        tuple: (bool: dependencies_ok, str: error_message or empty string)
    """
    status = check_system_dependencies()
    
    missing_deps = []
    for dep_name, dep_info in status.items():
        if not dep_info["installed"]:
            missing_deps.append(f"• {dep_name}: {dep_info['error']}")
    
    if missing_deps:
        error_msg = (
            "❌ Cannot proceed with download. Missing dependencies:\n\n" +
            "\n".join(missing_deps) +
            "\n\nPlease install missing dependencies and try again. "
            "See README.md for detailed installation instructions."
        )
        return False, error_msg
    
    return True, ""

# Suppress yt-dlp logs
import logging
logging.getLogger("yt_dlp").setLevel(logging.ERROR)


# ============================================================================
# Pydantic Models
# ============================================================================

class URLRequest(BaseModel):
    """Request model for URL input"""
    url: str


class DownloadRequest(BaseModel):
    """Request model for download with format selection"""
    url: str
    format_id: str


class FormatInfo(BaseModel):
    """Format information model"""
    format_id: str
    resolution: str
    ext: str
    filesize_mb: float


class VideoInfo(BaseModel):
    """Video information model"""
    title: str
    thumbnail: Optional[str]
    duration: int
    formats: list[FormatInfo]


class DownloadResponse(BaseModel):
    """Response model for download status"""
    status: str
    filename: Optional[str] = None
    message: str


# ============================================================================
# Helper Functions
# ============================================================================

def is_valid_youtube_url(url: str) -> bool:
    """Validate if URL is a valid YouTube URL"""
    youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com']
    return any(domain in url.lower() for domain in youtube_domains)


def get_video_info(url: str) -> dict:
    """
    Extract video information using yt-dlp
    
    Args:
        url: YouTube URL
        
    Returns:
        Dictionary with video info including formats
        
    Raises:
        Exception: If video info cannot be fetched
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'socket_timeout': 30,
    }
    
    # Add FFmpeg location if found
    if FFMPEG_LOCATION:
        ydl_opts['ffmpeg_location'] = FFMPEG_LOCATION
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        raise Exception(f"Failed to fetch video info: {str(e)}")


def extract_unique_formats(formats: list) -> list:
    """
    Extract unique video formats with resolutions
    
    Args:
        formats: List of all available formats from yt-dlp
        
    Returns:
        List of unique formats sorted by resolution (highest first)
    """
    unique_resolutions = {}
    
    for fmt in formats:
        # Only include video formats with height information
        if fmt.get('vcodec') != 'none' and fmt.get('height'):
            height = fmt.get('height')
            format_id = fmt.get('format_id')
            ext = fmt.get('ext', 'mp4')
            filesize = fmt.get('filesize', 0) or 0
            filesize_mb = filesize / (1024 * 1024)
            
            # Determine resolution label
            if height >= 2160:
                resolution = f"4K ({height}p)"
            elif height >= 1440:
                resolution = f"1440p (2K)"
            elif height >= 1080:
                resolution = "1080p"
            elif height >= 720:
                resolution = "720p"
            elif height >= 480:
                resolution = "480p"
            else:
                resolution = f"{height}p"
            
            # Keep highest quality for each resolution
            if resolution not in unique_resolutions or \
               height > unique_resolutions[resolution]['height']:
                unique_resolutions[resolution] = {
                    'format_id': format_id,
                    'resolution': resolution,
                    'height': height,
                    'ext': ext,
                    'filesize_mb': filesize_mb
                }
    
    # Convert to list and sort by height (descending)
    result = list(unique_resolutions.values())
    result.sort(key=lambda x: x['height'], reverse=True)
    
    return result


# ============================================================================
# Lifespan Context Manager
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("✓ FastAPI YouTube Downloader Backend Started")
    print(f"✓ Downloads folder: {DOWNLOADS_FOLDER.absolute()}")
    if FFMPEG_LOCATION:
        print(f"✓ FFmpeg found: {FFMPEG_LOCATION}")
    else:
        print("⚠ FFmpeg not found - video merging may fail")
    yield
    # Shutdown
    print("✓ Shutting down...")


# ============================================================================
# FastAPI App Setup
# ============================================================================

app = FastAPI(
    title="YouTube Downloader API",
    description="API for downloading YouTube videos with format selection",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "YouTube Downloader API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This message",
            "POST /get-formats": "Get available formats for a YouTube video",
            "POST /download": "Download a YouTube video with selected format",
            "GET /status": "Get download status"
        }
    }


@app.post("/get-formats", response_model=VideoInfo)
async def get_formats(request: URLRequest):
    """
    Get available formats for a YouTube video
    
    Args:
        request: URLRequest containing YouTube URL
        
    Returns:
        VideoInfo with title, thumbnail, and available formats
        
    Raises:
        HTTPException: If URL is invalid or video info cannot be fetched
    """
    # Validate URL
    if not request.url or not is_valid_youtube_url(request.url):
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL. Please provide a valid YouTube URL."
        )
    
    try:
        # Fetch video information
        info = get_video_info(request.url)
        
        # Extract video details
        title = info.get('title', 'Unknown Title')
        thumbnail = info.get('thumbnail', None)
        duration = info.get('duration', 0)
        
        # Extract unique formats
        all_formats = info.get('formats', [])
        unique_formats = extract_unique_formats(all_formats)
        
        if not unique_formats:
            raise HTTPException(
                status_code=400,
                detail="No video formats available for this video."
            )
        
        # Create format models
        format_list = [
            FormatInfo(
                format_id=fmt['format_id'],
                resolution=fmt['resolution'],
                ext=fmt['ext'],
                filesize_mb=fmt['filesize_mb']
            )
            for fmt in unique_formats
        ]
        
        return VideoInfo(
            title=title,
            thumbnail=thumbnail,
            duration=duration,
            formats=format_list
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching video information: {str(e)}"
        )


@app.post("/download", response_model=DownloadResponse)
async def download_video(request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    Download a YouTube video with selected format and merge with best audio
    
    Args:
        request: DownloadRequest with URL and format_id
        background_tasks: FastAPI background tasks
        
    Returns:
        DownloadResponse with status and filename
        
    Raises:
        HTTPException: If URL/format is invalid or download fails
    """
    # Validate URL
    if not request.url or not is_valid_youtube_url(request.url):
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL."
        )
    
    if not request.format_id:
        raise HTTPException(
            status_code=400,
            detail="Format ID is required."
        )
    
    # ✅ Check system dependencies before attempting download
    dependencies_ok, error_msg = verify_dependencies_for_download()
    if not dependencies_ok:
        raise HTTPException(
            status_code=503,
            detail=error_msg
        )
    
    try:
        # Configure yt-dlp options for high-quality download
        ydl_opts = {
            # Prefer m4a audio to avoid Opus-in-MP4 playback issues in browsers
            'format': (
                f'{request.format_id}+bestaudio[ext=m4a]/'
                f'bestvideo[ext=mp4]+bestaudio[ext=m4a]/'
                f'best[ext=mp4]/best'
            ),
            'merge_output_format': 'mp4',
            'outtmpl': str(DOWNLOADS_FOLDER / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        # Add FFmpeg location if found
        if FFMPEG_LOCATION:
            ydl_opts['ffmpeg_location'] = FFMPEG_LOCATION
        
        filename = None
        
        # Perform download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"[Download] Starting download for format: {request.format_id}")
            info = ydl.extract_info(request.url, download=True)
            filename = ydl.prepare_filename(info)
        
        if filename and Path(filename).exists():
            return DownloadResponse(
                status="success",
                filename=Path(filename).name,
                message=f"Video downloaded successfully: {Path(filename).name}"
            )
        else:
            raise Exception("Download completed but file not found")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )


@app.get("/downloads/{filename}")
async def download_file(filename: str):
    """
    Download a previously downloaded video file
    
    Args:
        filename: Name of the file to download
        
    Returns:
        FileResponse with the video file
        
    Raises:
        HTTPException: If file not found
    """
    # Security: Prevent directory traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )
    
    file_path = DOWNLOADS_FOLDER / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {filename}"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='video/mp4'
    )


@app.get("/status")
async def get_status():
    """Get current download folder status"""
    try:
        files = list(DOWNLOADS_FOLDER.glob("*.mp4"))
        total_size = sum(f.stat().st_size for f in files)
        
        return {
            "status": "healthy",
            "downloaded_videos": len(files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "downloads_folder": str(DOWNLOADS_FOLDER.absolute())
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting status: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint that verifies all system dependencies.
    
    Returns:
        dict: System health status including dependency information
    """
    try:
        dep_status = check_system_dependencies()
        all_ok = all(dep["installed"] for dep in dep_status.values())
        
        return {
            "status": "healthy" if all_ok else "degraded",
            "dependencies": dep_status,
            "ready_for_download": all_ok,
            "errors": [
                f"{name}: {info['error']}" 
                for name, info in dep_status.items() 
                if not info['installed']
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "detail": f"Internal server error: {str(exc)}"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
