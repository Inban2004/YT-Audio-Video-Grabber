# 🎬 Modern YouTube Downloader

A beautiful, feature-rich YouTube downloader with a modern GUI built using Python and Tkinter. updated with Download both audio and video from YouTube with **no mandatory ffmpeg dependency** for basic formats.

---

## ✨ Features

### 🎨 Modern GUI
- **Dark/Light Theme Toggle** - Beautiful gradient-based design
- **Real-time Progress Bar** - Visual feedback during downloads
- **Thumbnail Preview** - See video thumbnail before downloading
- **Download History** - Track your last 10 downloads
- **Custom Folder Selection** - Choose where to save files

### 📥 Download Options

**Audio Formats:**
- 🎵 **M4A** - No ffmpeg required, excellent quality
- 🎵 **MP3** - Requires ffmpeg, universal compatibility
- 🎵 **WAV** - Requires ffmpeg, lossless quality

**Video Formats:**
- 🎬 **MP4** - Standard video format
- 🎬 **WEBM** - No ffmpeg required

**Quality Levels:**
- **Best** - Highest available quality
- **High** - 1080p video / 320kbps audio
- **Medium** - 720p video / 256kbps audio
- **Low** - 480p video / 128kbps audio

### 🚀 Technical Features
- ✅ Threading for non-blocking UI
- ✅ Automatic thumbnail fetching
- ✅ URL validation
- ✅ Detailed error messages
- ✅ Optional ffmpeg support
- ✅ Cross-platform compatibility

---

## 📸 UI Preview

```
┌─────────────────────────────────────────────────────┐
│  🎬 YouTube Downloader              🌓 (Theme)      │
├─────────────────────────────────────────────────────┤
│  📎 YouTube URL:                                    │
│  [________________________________]                 │
├─────────────────────────────────────────────────────┤
│  🖼️ [    Thumbnail Preview Area    ]                │
├─────────────────────────────────────────────────────┤
│  📥 Download Mode:  ⚪ 🎵 Audio  ⚪ 🎬 Video        │
│  📄 Format:  ⚪ M4A  ⚪ MP3  ⚪ WAV                 |
│  ⚙️ Quality:  ⚪ Best  ⚪ High  ⚪ Medium  ⚪ Low   │
│  📁 Save to: /path/to/folder        [Change]        │
├─────────────────────────────────────────────────────┤
│  Status: Ready to download                          │
│  [████████████████████████] 0%                      │
├─────────────────────────────────────────────────────┤
│              [  ⬇️ Download  ]                      │
├─────────────────────────────────────────────────────┤
│  📜 Download History:                               │
│  ┌───────────────────────────────────────────────┐  │
│  │ [2026-01-01 12:00] AUDIO - Success: video... │   │
│  └───────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  yt-dlp ready | ✅ ffmpeg available                 │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Clone or download this repository
cd YT-Audio-Video-Grabber

# Create virtual environment (recommended)
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

**Required:**
- `yt-dlp` - Core download functionality

**Optional (for enhanced features):**
- `Pillow` - Enables thumbnail preview
- `requests` - Required for thumbnail downloading

### 2. Install ffmpeg (Required for MP4 Videos & MP3 Audio)

> [!IMPORTANT]
> **ffmpeg is REQUIRED for:**
> - 🎬 **MP4 video downloads** (to merge video + audio streams)
> - 🎵 **MP3 audio downloads** (for format conversion)
> 
> **ffmpeg is NOT needed for:**
> - ✅ M4A audio downloads (works without ffmpeg)
> - ✅ WEBM video downloads (works without ffmpeg)

**Ubuntu/Debian (Linux):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to PATH environment variable

**Verify Installation:**
```bash
ffmpeg -version
```

You should see version information. If successful, restart the app and the footer will show `✅ ffmpeg available`.

### 3. Run the Application

```bash
python youtube_downloader_modern.py
```

### Download fails
**Possible causes:**
- Invalid URL
- Video is private/unavailable
- No internet connection

### 🔄 Updatation
### 🔄 Updatation
- Complete GUI overhaul
- Better error handling
- URL validation
- Graceful ffmpeg fallback
- Detailed status messages

---

## 📋 Requirements

**System Requirements:**
- Python 3.7 or higher
- Internet connection

**Python Dependencies:**
- `yt-dlp` (required)
- `Pillow` (optional, for thumbnails)
- `requests` (optional, for thumbnails)

**External Dependencies:**
- `ffmpeg` (required for MP4 videos and MP3 audio)
  - Not needed for M4A audio or WEBM video
  - See installation instructions above

---

## 🔮 Future Enhancements

Possible future features:
- Playlist download support
- Batch URL processing
- Download queue management
- Subtitle download
- Custom filename templates
- Settings persistence
- Keyboard shortcuts

---

## 📝 Version History LOG : 

### v1.0 (Legacy Version)
- Basic audio-only downloader
- Simple tkinter GUI
- Required ffmpeg
- MP3 format only

### v2.0 (Modern Version) - 2026-02-01
- Complete GUI redesign with modern aesthetics
- Added video download support
- Added multiple format options
- Removed mandatory ffmpeg dependency
- Added thumbnail preview
- Added download history
- Added theme toggle
- Improved error handling

### v1.0 (Legacy Version)
- Basic audio-only downloader
- Simple tkinter GUI
- Required ffmpeg
- MP3 format only

---
