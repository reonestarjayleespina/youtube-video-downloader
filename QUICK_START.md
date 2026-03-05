# 🚀 Quick Start Commands

## Windows Users

### Setup (Run Once)
```bash
setup.bat
```

### Run Application (Every Time)

**Terminal 1:**
```bash
start_backend.bat
```

**Terminal 2:**
```bash
start_frontend.bat
```

**Browser:**
```
http://127.0.0.1:5173
```

---

## macOS/Linux Users

### Setup (Run Once)
```bash
chmod +x setup.sh
./setup.sh
```

### Run Application (Every Time)

**Terminal 1:**
```bash
chmod +x start_backend.sh
./start_backend.sh
```

**Terminal 2:**
```bash
chmod +x start_frontend.sh
./start_frontend.sh
```

**Browser:**
```
http://127.0.0.1:5173
```

---

## What You'll See

### Backend Console
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Frontend Console
```
  VITE v5.0.0  ready in 234 ms
  ➜  Local:   http://127.0.0.1:5173/
```

### Browser (http://127.0.0.1:5173)
- Beautiful glassmorphism UI
- Paste YouTube URL
- Select video quality
- Download with progress bar
- View download history

---

## Files Summary

| File | Purpose |
|------|---------|
| `setup.bat` | Windows one-click setup |
| `setup.sh` | macOS/Linux setup |
| `start_backend.bat` | Launch backend (Windows) |
| `start_frontend.bat` | Launch frontend (Windows) |
| `start_backend.sh` | Launch backend (macOS/Linux) |
| `start_frontend.sh` | Launch frontend (macOS/Linux) |
| `backend/main.py` | FastAPI server code |
| `frontend/src/App.vue` | Vue 3 component |
| `frontend/src/style.css` | Tailwind CSS styles |
| `FULL_SETUP_GUIDE.md` | Complete documentation |

---

## Troubleshooting

### Port Already in Use?
Kill process on port 8000/5173 and try again

### Backend not responding?
- Ensure `start_backend.bat/sh` is running
- Check terminal for errors
- Try restarting both

### Frontend not loading?
- Check browser console (F12)
- Verify backend is running
- Clear browser cache

### Can't download video?
- Ensure FFmpeg is installed
- Verify YouTube URL is correct
- Check video isn't private/restricted

---

## Endpoints

```
Backend: http://127.0.0.1:8000
Frontend: http://127.0.0.1:5173

API Endpoints:
  GET  /
  POST /get-formats
  POST /download
  GET  /downloads/{filename}
  GET  /status
```

---

## Next Time You Run It

1. Open two terminals
2. Run `start_backend.bat` (or `.sh`)
3. Run `start_frontend.bat` (or `.sh`)
4. Open `http://127.0.0.1:5173`
5. Start downloading!

That's it! No more setup needed. Enjoy! 🎉

