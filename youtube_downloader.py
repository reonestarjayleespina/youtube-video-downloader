#!/usr/bin/env python3
"""
YouTube Video Downloader using yt-dlp
Downloads YouTube videos with user-selected quality and merges with best audio using FFmpeg.
"""

import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Install it using: pip install yt-dlp")
    sys.exit(1)


def is_valid_youtube_url(url: str) -> bool:
    """
    Validate if the URL is a valid YouTube URL.
    
    Args:
        url: The URL to validate
        
    Returns:
        True if valid YouTube URL, False otherwise
    """
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        return any(yt_domain in domain for yt_domain in youtube_domains)
    except Exception:
        return False


def get_video_info(url: str) -> dict:
    """
    Fetch video information from YouTube.
    
    Args:
        url: The YouTube URL
        
    Returns:
        Dictionary containing video information
        
    Raises:
        Exception: If unable to fetch video information
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        raise Exception(f"Failed to fetch video information: {str(e)}")


def list_available_formats(info: dict) -> list:
    """
    List all available video formats with resolutions.
    
    Args:
        info: Video information dictionary
        
    Returns:
        List of available formats with their details
    """
    formats = info.get('formats', [])
    video_formats = []
    
    # Filter formats that have both video and audio capability
    for fmt in formats:
        if fmt.get('vcodec') != 'none' and fmt.get('height'):  # Has video
            format_id = fmt.get('format_id')
            height = fmt.get('height', 'Unknown')
            fps = fmt.get('fps', 'Unknown')
            ext = fmt.get('ext', 'Unknown')
            filesize = fmt.get('filesize', 0) or 0
            filesize_mb = filesize / (1024 * 1024) if filesize > 0 else 0
            
            format_info = {
                'format_id': format_id,
                'height': height,
                'fps': fps,
                'ext': ext,
                'filesize': filesize_mb,
                'format_obj': fmt
            }
            video_formats.append(format_info)
    
    # Sort by height in descending order
    video_formats.sort(key=lambda x: x['height'], reverse=True)
    
    return video_formats


def display_available_resolutions(formats: list) -> None:
    """
    Display available resolutions in a formatted table.
    
    Args:
        formats: List of available formats
    """
    print("\n" + "=" * 80)
    print(f"{'#':<5} {'Format ID':<15} {'Resolution':<15} {'FPS':<8} {'File Size':<15}")
    print("=" * 80)
    
    for idx, fmt in enumerate(formats, 1):
        resolution = f"{fmt['height']}p"
        fps = fmt['fps'] if isinstance(fmt['fps'], (int, float)) else "Unknown"
        filesize = f"{fmt['filesize']:.2f} MB" if fmt['filesize'] > 0 else "Unknown"
        
        print(f"{idx:<5} {fmt['format_id']:<15} {resolution:<15} {fps:<8} {filesize:<15}")
    
    print("=" * 80 + "\n")


def select_format(formats: list) -> str:
    """
    Allow user to select a format.
    
    Args:
        formats: List of available formats
        
    Returns:
        Selected format ID
    """
    while True:
        try:
            choice = input("Enter the Format ID you want to download (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                print("Exiting...")
                sys.exit(0)
            
            # Check if format ID exists
            if any(fmt['format_id'] == choice for fmt in formats):
                return choice
            
            print(f"Error: Format ID '{choice}' not found. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


def check_ffmpeg() -> bool:
    """
    Check if FFmpeg is installed on the system.
    
    Returns:
        True if FFmpeg is available, False otherwise
    """
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def download_video(url: str, format_id: str, output_path: str = "downloads") -> None:
    """
    Download YouTube video with selected format and merge with best audio.
    
    Args:
        url: The YouTube URL
        format_id: The selected format ID
        output_path: Directory to save the video
        
    Raises:
        Exception: If download or merge fails
    """
    # Create output directory if it doesn't exist
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': f'{format_id}+bestaudio/best',  # Select format with best audio
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'prefixes': ['ffmpeg'],
                'prettyname': 'FFmpeg',
            },
            {
                'key': 'FFmpegMergePostProcessor',
                'args': ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k'],
            }
        ] if check_ffmpeg() else [],
        'progress_hooks': [progress_hook],
    }
    
    try:
        print(f"\nDownloading video with format ID: {format_id}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"\n✓ Download completed successfully!")
            print(f"Saved to: {os.path.abspath(filename)}")
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")


def progress_hook(d):
    """
    Progress hook for yt-dlp download progress.
    
    Args:
        d: Dictionary with download progress information
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\rProgress: {percent} at {speed} ETA: {eta}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\n[download] Download completed, now converting...")


def main():
    """Main function to run the YouTube downloader."""
    print("=" * 80)
    print("YouTube Video Downloader")
    print("=" * 80)
    
    # Check if FFmpeg is available
    if not check_ffmpeg():
        print("\n⚠ Warning: FFmpeg is not installed or not found in PATH.")
        print("Audio/video merging may not work properly.")
        print("Install FFmpeg from: https://ffmpeg.org/download.html")
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(0)
    
    # Get YouTube URL from user
    while True:
        url = input("\nEnter YouTube URL: ").strip()
        
        if not url:
            print("Error: URL cannot be empty.")
            continue
        
        if not is_valid_youtube_url(url):
            print("Error: Invalid YouTube URL. Please enter a valid YouTube URL.")
            continue
        
        break
    
    # Fetch video information
    print("\nFetching video information...")
    try:
        info = get_video_info(url)
        title = info.get('title', 'Unknown')
        print(f"Video Title: {title}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    
    # Get available formats
    formats = list_available_formats(info)
    
    if not formats:
        print("Error: No video formats found for this video.")
        sys.exit(1)
    
    # Display available resolutions
    print(f"\nAvailable resolutions: {len(formats)}")
    display_available_resolutions(formats)
    
    # Select format
    selected_format_id = select_format(formats)
    
    # Download video
    try:
        download_video(url, selected_format_id)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("Thank you for using YouTube Video Downloader!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)
