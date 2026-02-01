# 🎬 Modern YouTube Downloader

A beautiful, feature-rich YouTube downloader with a modern GUI built using Python and Tkinter. Download both audio and video from YouTube with **no mandatory ffmpeg dependency** for basic formats.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

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

### 2. Install ffmpeg (Optional)

ffmpeg is **optional** but recommended for MP3 and high-quality MP4 downloads.

**Ubuntu/Debian:**
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

### 3. Run the Application

```bash
python youtube_downloader_modern.py
```

---

## 📖 Usage Guide

### Download Audio (No ffmpeg needed)

1. **Paste YouTube URL** in the input field
2. **Select "Audio" mode** (default)
3. **Choose "M4A" format** (no conversion needed)
4. **Select quality** (Best recommended)
5. **Click "Download"**
6. **Wait for completion** - File saved to download folder

### Download Video (No ffmpeg needed)

1. **Paste YouTube URL**
2. **Select "Video" mode**
3. **Choose "WEBM" format** (no ffmpeg required)
4. **Select quality** (Best, High, Medium, or Low)
5. **Click "Download"**
6. **Wait for completion**

### Advanced Features

**Change Download Folder:**
- Click "Change" button next to folder path
- Select your desired folder

**Toggle Theme:**
- Click 🌓 button in top-right corner
- Switches between dark and light theme

**View Download History:**
- Automatically tracks last 10 downloads
- Shows timestamp, mode, and status

---

## 🔧 Troubleshooting

### "yt-dlp is not installed"
```bash
pip install yt-dlp
```

### "MP3 conversion requires ffmpeg"
**Option 1:** Install ffmpeg (see installation instructions above)  
**Option 2:** Use M4A format instead (no ffmpeg needed)

### Thumbnail not showing
```bash
pip install Pillow requests
```

### Download fails
**Possible causes:**
- Invalid URL
- Video is private/unavailable
- No internet connection

**Solutions:**
- Verify URL is correct
- Check internet connection
- Update yt-dlp: `pip install -U yt-dlp`

---

## 💡 Tips & Best Practices

### For Best Audio Quality
- Use **M4A format** with **Best quality**
- M4A is often higher quality than MP3
- No conversion = faster + better quality

### For Best Video Quality
- Use **MP4 format** with **Best quality**
- Ensure ffmpeg is installed for proper merging
- Automatically selects highest available resolution

### For Fastest Downloads
- Use **M4A** for audio (no conversion)
- Use **WEBM** for video (no merging)
- Select **Medium** or **Low** quality

### For Maximum Compatibility
- Use **MP3** for audio (requires ffmpeg)
- Use **MP4** for video (requires ffmpeg)
- These formats work on all devices

---

## 📁 Project Structure

```
YT-Audio-Video-Grabber/
├── youtube_downloader_modern.py    # Main application (NEW)
├── youtube_audio_downloader.py     # Old version (legacy)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── CHANGELOG.md                    # Detailed changelog
├── .env                            # Optional config
└── env/                            # Virtual environment
```

---

## 🎯 What's New in Modern Version

### ✅ Added Features
- Modern GUI with dark/light themes
- Video download support (not just audio)
- Multiple format options (5 total)
- Quality selection (4 levels)
- Real-time progress bar
- Thumbnail preview
- Download history
- Custom folder selection
- Threading for non-blocking UI

### ❌ Removed Requirements
- Mandatory ffmpeg dependency (now optional)
- `.env` file requirement (no longer needed)
- Fixed download folder (now customizable)

### 🔄 Improvements
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
- ~10MB disk space

**Python Dependencies:**
- `yt-dlp` (required)
- `Pillow` (optional, for thumbnails)
- `requests` (optional, for thumbnails)

**Optional:**
- `ffmpeg` (for MP3/MP4 conversion)

---

## ❓ FAQ

**Q: Do I need ffmpeg?**  
A: No, but it's recommended. M4A and WEBM formats work without ffmpeg.

**Q: Can I download playlists?**  
A: Not yet. Currently supports single videos only.

**Q: Where are downloads saved?**  
A: Default: `~/Downloads/YouTube/` - Customizable via "Change" button

**Q: Can I cancel a download?**  
A: Not currently. Close the app to cancel (file may be incomplete).

**Q: Why is MP3 unavailable?**  
A: ffmpeg is not installed. Install ffmpeg or use M4A format.

**Q: Does this work on Windows/Mac/Linux?**  
A: Yes! Works on all platforms with Python 3.7+

**Q: Is this legal?**  
A: Only download content you have rights to. Respect copyright laws.

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

## 📝 Version History

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

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🆘 Support

For detailed documentation, see [CHANGELOG.md](CHANGELOG.md)

If you encounter issues:
1. Check the Troubleshooting section above
2. Ensure all dependencies are installed
3. Update yt-dlp: `pip install -U yt-dlp`
4. Check yt-dlp GitHub for known issues

---

## 🙏 Acknowledgments

- **yt-dlp** - Powerful YouTube downloader library
- **Tkinter** - Python's standard GUI framework
- **Pillow** - Python Imaging Library
- **ffmpeg** - Multimedia framework

---

**Made with ❤️ for easy YouTube downloads**

**Enjoy your modern YouTube downloader! 🎉**
