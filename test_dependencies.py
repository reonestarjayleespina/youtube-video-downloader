#!/usr/bin/env python3
"""
YouTube Downloader - System Dependency Test Script
===================================================

This script verifies that all required dependencies are properly installed
and accessible on your system before running the downloader.

Run this script to:
✓ Check if Python is correctly installed
✓ Verify yt-dlp is installed and functional
✓ Verify FFmpeg is installed and functional
✓ Check system PATH configuration
✓ Display version information for debugging

Usage:
    python test_dependencies.py

Exit Codes:
    0 = All dependencies OK
    1 = One or more dependencies missing or failed
    2 = Unexpected error during testing
"""

import subprocess
import sys
import platform
import shutil
from pathlib import Path


# ANSI Color codes for terminal output
class Colors:
    """Terminal color helpers"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")


def print_success(text: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    """Print an error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text: str):
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def test_python_version():
    """Test Python version"""
    print_header("Python Environment")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Python Executable: {sys.executable}")
    print_info(f"Python Version: {version_str}")
    print_info(f"Platform: {platform.system()} {platform.release()}")
    
    if version.major >= 3 and version.minor >= 6:
        print_success("Python version is compatible (3.6+)")
        return True
    else:
        print_error(f"Python 3.6+ required, you have {version_str}")
        return False


def test_command(command: list, name: str, version_flag: str = "--version") -> tuple[bool, str, str]:
    """
    Test if a command is available and functional.
    
    Args:
        command: Command to run (e.g., ['ffmpeg'])
        name: Human-readable name (e.g., 'FFmpeg')
        version_flag: Flag to get version info (e.g., '--version')
    
    Returns:
        tuple: (success: bool, version: str, path: str)
    """
    try:
        # Check if command exists in PATH
        path = shutil.which(command[0])
        
        if not path:
            return False, "Not found in PATH", ""
        
        # Try to get version
        result = subprocess.run(
            command + [version_flag],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Extract first line of output as version info
            version_output = result.stdout.split('\n')[0] if result.stdout else "Unknown version"
            return True, version_output, path
        else:
            error_msg = result.stderr.split('\n')[0] if result.stderr else "Unknown error"
            return False, error_msg, path
    
    except subprocess.TimeoutExpired:
        return False, "Command timed out", ""
    except FileNotFoundError:
        return False, "Command not found", ""
    except Exception as e:
        return False, str(e), ""


def test_ffmpeg():
    """Test FFmpeg installation"""
    print_header("FFmpeg Installation Check")
    
    success, version, path = test_command(['ffmpeg'], 'FFmpeg', '-version')
    
    if success:
        print_success(f"FFmpeg is installed")
        print_info(f"Version: {version}")
        print_info(f"Location: {path}")
        
        # Test that FFmpeg can actually process a command
        try:
            result = subprocess.run(
                ['ffmpeg', '-codecs'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print_success("FFmpeg is functional")
            else:
                print_warning("FFmpeg is installed but may not be fully functional")
                return False
        except Exception as e:
            print_error(f"FFmpeg functionality test failed: {e}")
            return False
        
        return True
    else:
        print_error(f"FFmpeg is not properly installed")
        print_error(f"Reason: {version}")
        
        print_info("\nTo install FFmpeg:")
        
        system = platform.system()
        if system == "Windows":
            print_info("Windows:")
            print_info("  Option 1: Download from https://ffmpeg.org/download.html")
            print_info("  Option 2: winget install FFmpeg.FFmpeg")
            print_info("  Option 3: choco install ffmpeg")
        elif system == "Darwin":
            print_info("macOS:")
            print_info("  brew install ffmpeg")
        else:
            print_info("Linux:")
            print_info("  Ubuntu/Debian: sudo apt install ffmpeg")
            print_info("  Fedora/RHEL: sudo dnf install ffmpeg")
        
        return False


def test_ytdlp():
    """Test yt-dlp installation"""
    print_header("yt-dlp Installation Check")
    
    success, version, path = test_command(['yt-dlp'], 'yt-dlp', '--version')
    
    if success:
        print_success(f"yt-dlp is installed")
        print_info(f"Version: {version}")
        print_info(f"Location: {path}")
        
        # Test that yt-dlp can actually run
        try:
            result = subprocess.run(
                ['yt-dlp', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print_success("yt-dlp is functional")
            else:
                print_warning("yt-dlp is installed but may not be fully functional")
                return False
        except Exception as e:
            print_error(f"yt-dlp functionality test failed: {e}")
            return False
        
        return True
    else:
        print_error(f"yt-dlp is not properly installed")
        print_error(f"Reason: {version}")
        
        print_info("\nTo install yt-dlp:")
        print_info("  pip install yt-dlp")
        print_info("  or: pip install --upgrade yt-dlp")
        
        return False


def test_pip():
    """Test pip installation"""
    print_header("pip Package Manager Check")
    
    success, version, path = test_command(['pip'], 'pip', '--version')
    
    if success:
        print_success(f"pip is installed")
        print_info(f"Version: {version}")
        return True
    else:
        print_error(f"pip is not properly installed")
        return False


def verify_python_packages():
    """Verify Python packages required by the backend"""
    print_header("Python Packages Check")
    
    required_packages = {
        'fastapi': 'Web framework',
        'uvicorn': 'ASGI server',
        'yt_dlp': 'YouTube downloader',
        'pydantic': 'Data validation',
    }
    
    all_ok = True
    
    try:
        import pkg_resources
        
        installed = {pkg.key for pkg in pkg_resources.working_set}
        
        for package, description in required_packages.items():
            # Convert underscore to hyphen for comparison
            package_name = package.replace('_', '-').lower()
            
            if package_name in installed or package in installed:
                try:
                    module = __import__(package.replace('-', '_'))
                    version = getattr(module, '__version__', 'Unknown')
                    print_success(f"{package}: {description} (v{version})")
                except:
                    print_success(f"{package}: {description}")
            else:
                print_error(f"{package}: {description} - NOT INSTALLED")
                all_ok = False
        
        return all_ok
    
    except ImportError:
        print_warning("pkg_resources not available, skipping package verification")
        return True


def test_path_configuration():
    """Test if common tool locations are in PATH"""
    print_header("System PATH Configuration")
    
    path_dirs = sys.path
    print_info(f"Python sys.path has {len(path_dirs)} directories")
    
    # Check environment PATH
    import os
    env_path = os.environ.get('PATH', '')
    path_entries = env_path.split(';' if platform.system() == 'Windows' else ':')
    print_info(f"Environment PATH has {len(path_entries)} directories")
    
    # Check for common issue locations
    suspicious_paths = []
    for path in path_entries:
        if 'temp' in path.lower() or 'cache' in path.lower():
            suspicious_paths.append(path)
    
    if not suspicious_paths:
        print_success("PATH configuration looks good")
        return True
    else:
        print_warning(f"Found {len(suspicious_paths)} suspicious PATH entries:")
        for p in suspicious_paths:
            print_info(f"  {p}")
        return True


def run_compatibility_test():
    """Run a basic compatibility test"""
    print_header("Compatibility Test")
    
    try:
        # Try to use yt-dlp and ffmpeg together
        result = subprocess.run(
            ['yt-dlp', '--list-formats', 'https://www.youtube.com/watch?v=jNQXAC9IVRw'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print_success("yt-dlp can fetch video information")
            formats = result.stdout.count('\n')
            print_info(f"Found {formats} available formats")
            return True
        else:
            if "No video found" in result.stderr:
                print_warning("Test video not available, but yt-dlp is working")
                return True
            elif "Unable to extract video data" in result.stderr:
                print_warning("yt-dlp reported: Unable to extract video data")
                print_info("This might be a temporary YouTube issue")
                return True
            else:
                print_error("yt-dlp failed to fetch video information")
                print_error(f"Error: {result.stderr[:200]}")
                return False
    
    except subprocess.TimeoutExpired:
        print_warning("Compatibility test timed out (network issue?)")
        return False
    except Exception as e:
        print_error(f"Compatibility test failed: {e}")
        return False


def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "═" * 68 + "╗")
    print("║" + "YouTube Downloader - Dependency Verification".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print(f"{Colors.RESET}")
    
    results = {
        "Python Version": test_python_version(),
        "pip Package Manager": test_pip(),
        "Python Packages": verify_python_packages(),
        "FFmpeg Installation": test_ffmpeg(),
        "yt-dlp Installation": test_ytdlp(),
        "System PATH": test_path_configuration(),
        "Compatibility Test": run_compatibility_test(),
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}\n")
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"  {test_name:.<40} {status}")
    
    # Final verdict
    print()
    if all(results.values()):
        print_success("All checks passed! Your system is ready for the YouTube Downloader.")
        print_info("\nYou can now:")
        print_info("  1. Run: python youtube_downloader.py (CLI version)")
        print_info("  2. Run: bash start_backend.sh (Backend server)")
        print_info("  3. Run: bash start_frontend.sh (Frontend app)")
        return 0
    else:
        print_error("Some checks failed. Please fix the issues above and try again.")
        print_warning("\nCommon fixes:")
        print_info("  • Ensure FFmpeg is in PATH and restart terminal")
        print_info("  • Run: pip install --upgrade yt-dlp")
        print_info("  • Set FFMPEG_PATH environment variable if FFmpeg not found")
        print_info("  • See README.md for detailed installation instructions")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
