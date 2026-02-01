# Quick ffmpeg Installation Guide

## The Issue
MP4 video downloads require **ffmpeg** to merge video and audio streams. Without ffmpeg:
- ✅ Audio downloads (M4A) work fine
- ✅ Video downloads (WEBM) work fine  
- ❌ Audio downloads (MP3) fail
- ❌ Video downloads (MP4) fail or have no audio

## Solution: Install ffmpeg

### Ubuntu/Debian (Linux)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Verify Installation
```bash
ffmpeg -version
```

You should see ffmpeg version information. If successful, **restart the YouTube downloader application** and you'll see:
- Footer will show: `✅ ffmpeg available`
- MP3 and MP4 options will work properly

## Alternative: Use Formats That Don't Need ffmpeg

If you can't install ffmpeg right now:

**For Audio:**
- Use **M4A** format instead of MP3
- M4A has excellent quality and works everywhere

**For Video:**
- Use **WEBM** format instead of MP4
- WEBM works in most modern players (VLC, Chrome, Firefox)

## Testing

After installing ffmpeg:
1. Close the YouTube downloader app
2. Reopen it: `python3 youtube_downloader_modern.py`
3. Check the footer - should show `✅ ffmpeg available`
4. Try downloading MP4 video - should work now!

---

**Note:** The app will now automatically warn you if you try to download MP3/MP4 without ffmpeg and offer to switch to M4A/WEBM instead.
