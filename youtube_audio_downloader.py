import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# -----------------------------
# Environment setup
# -----------------------------
load_dotenv()

"""
Install ffmpeg 
  step 1 : winget install "FFmpeg (Essentials Build)" 
  step 2 : check using "ffmpeg -version" 
  step 3 : Get path "where ffmpeg" and copy it 
  step 3 : update the path in command list 
"""

# DOWNLOAD_FOLDER = "youtube-downloaded-songs"
DOWNLOAD_FOLDER = "Random-Song"
ffmpeg_location = os.getenv("FFMPEG_LOCATION")

if ffmpeg_location:
    ffmpeg_location = ffmpeg_location.strip().strip('"').strip("'")

if not ffmpeg_location:
    raise SystemExit(
        "Missing FFMPEG_LOCATION in .env. "
        "Set it to your ffmpeg bin folder or ffmpeg.exe path."
    )

ffmpeg_location = os.path.normpath(
    os.path.expandvars(os.path.expanduser(ffmpeg_location))
)

# Validate ffmpeg location
if os.path.isdir(ffmpeg_location):
    ffmpeg_exe = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    ffmpeg_candidate = os.path.join(ffmpeg_location, ffmpeg_exe)
    if not os.path.exists(ffmpeg_candidate):
        raise SystemExit(
            f"FFMPEG_LOCATION points to a folder but {ffmpeg_exe} was not found: {ffmpeg_location}"
        )
elif not os.path.isfile(ffmpeg_location):
    raise SystemExit(
        f"FFMPEG_LOCATION does not exist or is not a file/folder: {ffmpeg_location}"
    )

# -----------------------------
# Core download logic
# -----------------------------
def download_audio(youtube_url: str):
    if not youtube_url.strip():
        raise ValueError("YouTube URL is empty.")

    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-f", "bestaudio/best",
        "--ffmpeg-location", ffmpeg_location,
        # "--cookies", "cookies.txt",
        "-o", f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        youtube_url
    ]

    subprocess.run(command, check=True)

# -----------------------------
# GUI logic
# -----------------------------
def on_download(entry, status_label, button):
    url = entry.get().strip()

    if not url:
        messagebox.showwarning("Input required", "Please paste a YouTube link")
        return

    status_label.config(text="Downloading...")
    button.config(state="disabled")
    window.update_idletasks()

    try:
        download_audio(url)
        status_label.config(text="Done 🎵")

        # Clear input ONLY on success
        entry.delete(0, tk.END)
        entry.focus()

    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Download failed")
        status_label.config(text="Failed ❌")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Failed ❌")

    finally:
        button.config(state="normal")

# -----------------------------
# Tkinter UI
# -----------------------------
window = tk.Tk()
window.title("YouTube Audio Downloader")
window.geometry("420x150")
window.resizable(False, False)

tk.Label(window, text="Paste YouTube link:").pack(pady=8)

url_entry = tk.Entry(window, width=55)
url_entry.pack()
url_entry.focus()

status_label = tk.Label(window, text="", fg="green")
status_label.pack(pady=5)

download_btn = tk.Button(
    window,
    text="Download Audio",
    command=lambda: on_download(url_entry, status_label, download_btn)
)
download_btn.pack(pady=5)

window.mainloop()
