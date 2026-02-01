#!/usr/bin/env python3
"""
Modern YouTube Downloader
A beautiful, feature-rich YouTube downloader with audio/video options
No ffmpeg dependency required (optional for MP3 conversion)
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import subprocess
import json
from datetime import datetime
from typing import Optional, Dict, List
import shutil

# Optional imports
try:
    from PIL import Image, ImageTk
    import requests
    from io import BytesIO
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Note: Install Pillow for thumbnail preview: pip install Pillow requests")


class ModernYouTubeDownloader:
    """Modern YouTube Downloader with beautiful GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("700x850")
        self.root.resizable(False, False)
        
        # Configuration
        self.download_folder = str(Path.home() / "Downloads" / "YouTube")
        self.download_mode = tk.StringVar(value="audio")  # audio or video
        self.audio_format = tk.StringVar(value="m4a")  # m4a, mp3, wav
        self.video_format = tk.StringVar(value="mp4")  # mp4, webm
        self.quality = tk.StringVar(value="best")  # best, high, medium, low
        self.theme = tk.StringVar(value="dark")  # dark or light
        self.download_history: List[Dict] = []
        self.is_downloading = False
        self.current_thumbnail = None
        
        # Check for yt-dlp
        if not self._check_ytdlp():
            messagebox.showerror(
                "Missing Dependency",
                "yt-dlp is not installed!\n\n"
                "Install it with:\npip install yt-dlp"
            )
            sys.exit(1)
        
        # Check for ffmpeg (optional)
        self.ffmpeg_available = self._check_ffmpeg()
        
        # Setup UI
        self._setup_styles()
        self._create_ui()
        self._apply_theme()
        
    def _check_ytdlp(self) -> bool:
        """Check if yt-dlp is installed"""
        return shutil.which("yt-dlp") is not None
    
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available (optional)"""
        return shutil.which("ffmpeg") is not None
    
    def _setup_styles(self):
        """Setup custom styles for widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.colors = {
            'dark': {
                'bg': '#1a1a2e',
                'secondary_bg': '#16213e',
                'accent': '#0f3460',
                'primary': '#e94560',
                'text': '#eee',
                'secondary_text': '#aaa',
                'success': '#2ecc71',
                'warning': '#f39c12',
                'error': '#e74c3c'
            },
            'light': {
                'bg': '#f5f5f5',
                'secondary_bg': '#ffffff',
                'accent': '#e3e3e3',
                'primary': '#3498db',
                'text': '#2c3e50',
                'secondary_text': '#7f8c8d',
                'success': '#27ae60',
                'warning': '#f39c12',
                'error': '#e74c3c'
            }
        }
    
    def _apply_theme(self):
        """Apply current theme colors"""
        theme = self.theme.get()
        colors = self.colors[theme]
        
        # Main window
        self.root.configure(bg=colors['bg'])
        
        # Update all frames
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=colors['bg'])
                self._update_widget_colors(widget, colors)
    
    def _update_widget_colors(self, parent, colors):
        """Recursively update widget colors"""
        for widget in parent.winfo_children():
            widget_type = widget.winfo_class()
            
            if widget_type == 'Frame':
                widget.configure(bg=colors['bg'])
                self._update_widget_colors(widget, colors)
            elif widget_type == 'Label':
                widget.configure(bg=colors['bg'], fg=colors['text'])
            elif widget_type == 'Entry':
                widget.configure(bg=colors['secondary_bg'], fg=colors['text'], 
                               insertbackground=colors['text'])
    
    def _create_ui(self):
        """Create the main UI"""
        # Header
        self._create_header()
        
        # URL Input Section
        self._create_url_section()
        
        # Thumbnail Preview
        if PILLOW_AVAILABLE:
            self._create_thumbnail_section()
        
        # Download Options
        self._create_options_section()
        
        # Progress Section
        self._create_progress_section()
        
        # Download Button
        self._create_download_button()
        
        # History Section
        self._create_history_section()
        
        # Footer
        self._create_footer()
    
    def _create_header(self):
        """Create header with title and theme toggle"""
        header_frame = tk.Frame(self.root, bg=self.colors['dark']['bg'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title = tk.Label(
            header_frame,
            text="🎬 YouTube Downloader",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['primary']
        )
        title.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Theme toggle
        theme_btn = tk.Button(
            header_frame,
            text="🌓",
            font=("Helvetica", 16),
            command=self._toggle_theme,
            bg=self.colors['dark']['accent'],
            fg=self.colors['dark']['text'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=5
        )
        theme_btn.pack(side=tk.RIGHT, padx=20, pady=20)
    
    def _create_url_section(self):
        """Create URL input section"""
        frame = tk.Frame(self.root, bg=self.colors['dark']['bg'])
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        label = tk.Label(
            frame,
            text="📎 YouTube URL:",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text']
        )
        label.pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = tk.Entry(
            frame,
            font=("Helvetica", 11),
            bg=self.colors['dark']['secondary_bg'],
            fg=self.colors['dark']['text'],
            insertbackground=self.colors['dark']['text'],
            relief=tk.FLAT,
            bd=0
        )
        self.url_entry.pack(fill=tk.X, ipady=10, ipadx=10)
        self.url_entry.bind('<Return>', lambda e: self._start_download())
        self.url_entry.bind('<KeyRelease>', self._on_url_change)
    
    def _create_thumbnail_section(self):
        """Create thumbnail preview section"""
        self.thumbnail_frame = tk.Frame(
            self.root,
            bg=self.colors['dark']['secondary_bg'],
            height=150
        )
        self.thumbnail_frame.pack(fill=tk.X, padx=20, pady=10)
        self.thumbnail_frame.pack_propagate(False)
        
        self.thumbnail_label = tk.Label(
            self.thumbnail_frame,
            text="🖼️ Thumbnail preview will appear here",
            font=("Helvetica", 10),
            bg=self.colors['dark']['secondary_bg'],
            fg=self.colors['dark']['secondary_text']
        )
        self.thumbnail_label.pack(expand=True)
    
    def _create_options_section(self):
        """Create download options section"""
        frame = tk.Frame(self.root, bg=self.colors['dark']['bg'])
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Mode Selection (Audio/Video)
        mode_frame = tk.Frame(frame, bg=self.colors['dark']['bg'])
        mode_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            mode_frame,
            text="📥 Download Mode:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        audio_radio = tk.Radiobutton(
            mode_frame,
            text="🎵 Audio",
            variable=self.download_mode,
            value="audio",
            font=("Helvetica", 10),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text'],
            selectcolor=self.colors['dark']['accent'],
            activebackground=self.colors['dark']['bg'],
            activeforeground=self.colors['dark']['primary'],
            command=self._on_mode_change
        )
        audio_radio.pack(side=tk.LEFT, padx=5)
        
        video_radio = tk.Radiobutton(
            mode_frame,
            text="🎬 Video",
            variable=self.download_mode,
            value="video",
            font=("Helvetica", 10),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text'],
            selectcolor=self.colors['dark']['accent'],
            activebackground=self.colors['dark']['bg'],
            activeforeground=self.colors['dark']['primary'],
            command=self._on_mode_change
        )
        video_radio.pack(side=tk.LEFT, padx=5)
        
        # Format Selection
        format_frame = tk.Frame(frame, bg=self.colors['dark']['bg'])
        format_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            format_frame,
            text="📄 Format:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Audio formats
        self.audio_format_frame = tk.Frame(format_frame, bg=self.colors['dark']['bg'])
        self.audio_format_frame.pack(side=tk.LEFT)
        
        for fmt in [("M4A (No ffmpeg)", "m4a"), ("MP3", "mp3"), ("WAV", "wav")]:
            tk.Radiobutton(
                self.audio_format_frame,
                text=fmt[0],
                variable=self.audio_format,
                value=fmt[1],
                font=("Helvetica", 9),
                bg=self.colors['dark']['bg'],
                fg=self.colors['dark']['text'],
                selectcolor=self.colors['dark']['accent'],
                activebackground=self.colors['dark']['bg'],
                activeforeground=self.colors['dark']['primary']
            ).pack(side=tk.LEFT, padx=3)
        
        # Video formats
        self.video_format_frame = tk.Frame(format_frame, bg=self.colors['dark']['bg'])
        
        for fmt in [("MP4", "mp4"), ("WEBM (No ffmpeg)", "webm")]:
            tk.Radiobutton(
                self.video_format_frame,
                text=fmt[0],
                variable=self.video_format,
                value=fmt[1],
                font=("Helvetica", 9),
                bg=self.colors['dark']['bg'],
                fg=self.colors['dark']['text'],
                selectcolor=self.colors['dark']['accent'],
                activebackground=self.colors['dark']['bg'],
                activeforeground=self.colors['dark']['primary']
            ).pack(side=tk.LEFT, padx=3)
        
        # Quality Selection
        quality_frame = tk.Frame(frame, bg=self.colors['dark']['bg'])
        quality_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            quality_frame,
            text="⚙️ Quality:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        for qual in [("Best", "best"), ("High", "high"), ("Medium", "medium"), ("Low", "low")]:
            tk.Radiobutton(
                quality_frame,
                text=qual[0],
                variable=self.quality,
                value=qual[1],
                font=("Helvetica", 9),
                bg=self.colors['dark']['bg'],
                fg=self.colors['dark']['text'],
                selectcolor=self.colors['dark']['accent'],
                activebackground=self.colors['dark']['bg'],
                activeforeground=self.colors['dark']['primary']
            ).pack(side=tk.LEFT, padx=3)
        
        # Download Folder
        folder_frame = tk.Frame(frame, bg=self.colors['dark']['bg'])
        folder_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            folder_frame,
            text="📁 Save to:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.folder_label = tk.Label(
            folder_frame,
            text=self.download_folder,
            font=("Helvetica", 9),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['secondary_text'],
            anchor=tk.W
        )
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        folder_btn = tk.Button(
            folder_frame,
            text="Change",
            command=self._select_folder,
            bg=self.colors['dark']['accent'],
            fg=self.colors['dark']['text'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=3
        )
        folder_btn.pack(side=tk.RIGHT)
        
        self._on_mode_change()  # Initialize format visibility
    
    def _create_progress_section(self):
        """Create progress bar and status section"""
        frame = tk.Frame(self.root, bg=self.colors['dark']['bg'])
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = tk.Label(
            frame,
            text="Ready to download",
            font=("Helvetica", 10),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['secondary_text']
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(fill=tk.X, pady=5)
        
        self.progress_label = tk.Label(
            frame,
            text="0%",
            font=("Helvetica", 9),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['secondary_text']
        )
        self.progress_label.pack(anchor=tk.E)
    
    def _create_download_button(self):
        """Create main download button"""
        self.download_btn = tk.Button(
            self.root,
            text="⬇️ Download",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['dark']['primary'],
            fg='white',
            relief=tk.FLAT,
            cursor="hand2",
            command=self._start_download,
            padx=30,
            pady=15
        )
        self.download_btn.pack(pady=20)
    
    def _create_history_section(self):
        """Create download history section"""
        frame = tk.Frame(self.root, bg=self.colors['dark']['bg'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            frame,
            text="📜 Download History:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark']['bg'],
            fg=self.colors['dark']['text']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # History listbox
        history_container = tk.Frame(frame, bg=self.colors['dark']['secondary_bg'])
        history_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(history_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            history_container,
            font=("Helvetica", 9),
            bg=self.colors['dark']['secondary_bg'],
            fg=self.colors['dark']['text'],
            relief=tk.FLAT,
            yscrollcommand=scrollbar.set,
            height=6
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
    
    def _create_footer(self):
        """Create footer with info"""
        footer = tk.Frame(self.root, bg=self.colors['dark']['accent'], height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        ffmpeg_status = "✅ ffmpeg available" if self.ffmpeg_available else "⚠️ ffmpeg not found (MP3/MP4 unavailable)"
        
        tk.Label(
            footer,
            text=f"yt-dlp ready | {ffmpeg_status}",
            font=("Helvetica", 8),
            bg=self.colors['dark']['accent'],
            fg=self.colors['dark']['secondary_text']
        ).pack(pady=7)
    
    def _toggle_theme(self):
        """Toggle between dark and light theme"""
        current = self.theme.get()
        self.theme.set("light" if current == "dark" else "dark")
        self._apply_theme()
    
    def _on_mode_change(self):
        """Handle download mode change"""
        mode = self.download_mode.get()
        
        if mode == "audio":
            self.audio_format_frame.pack(side=tk.LEFT)
            self.video_format_frame.pack_forget()
        else:
            self.video_format_frame.pack(side=tk.LEFT)
            self.audio_format_frame.pack_forget()
    
    def _on_url_change(self, event=None):
        """Handle URL entry change"""
        url = self.url_entry.get().strip()
        
        if url and PILLOW_AVAILABLE:
            # Try to fetch thumbnail in background
            threading.Thread(target=self._fetch_thumbnail, args=(url,), daemon=True).start()
    
    def _fetch_thumbnail(self, url: str):
        """Fetch video thumbnail"""
        try:
            # Get video info
            result = subprocess.run(
                ["yt-dlp", "--dump-json", "--no-playlist", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                thumbnail_url = info.get('thumbnail')
                
                if thumbnail_url:
                    # Download thumbnail
                    response = requests.get(thumbnail_url, timeout=5)
                    img = Image.open(BytesIO(response.content))
                    
                    # Resize to fit
                    img.thumbnail((400, 150), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update UI (must be in main thread)
                    self.root.after(0, self._update_thumbnail, photo)
        except Exception:
            pass  # Silently fail for thumbnail
    
    def _update_thumbnail(self, photo):
        """Update thumbnail in UI"""
        self.current_thumbnail = photo  # Keep reference
        self.thumbnail_label.configure(image=photo, text="")
    
    def _select_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_label.config(text=folder)
    
    def _start_download(self):
        """Start download in background thread"""
        if self.is_downloading:
            messagebox.showwarning("Download in Progress", "Please wait for current download to finish")
            return
        
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("URL Required", "Please enter a YouTube URL")
            return
        
        # Validate URL
        if not ("youtube.com" in url or "youtu.be" in url):
            messagebox.showwarning("Invalid URL", "Please enter a valid YouTube URL")
            return
        
        # Check ffmpeg for MP3
        if self.download_mode.get() == "audio" and self.audio_format.get() == "mp3" and not self.ffmpeg_available:
            response = messagebox.askyesno(
                "ffmpeg Not Found",
                "MP3 conversion requires ffmpeg, which is not installed.\n\n"
                "Would you like to download as M4A instead?"
            )
            if response:
                self.audio_format.set("m4a")
            else:
                return
        
        # Check ffmpeg for MP4 video
        if self.download_mode.get() == "video" and self.video_format.get() == "mp4" and not self.ffmpeg_available:
            response = messagebox.askyesno(
                "ffmpeg Not Found",
                "MP4 video requires ffmpeg to merge video and audio streams.\n"
                "ffmpeg is not installed.\n\n"
                "Would you like to download as WEBM instead?\n"
                "(WEBM works without ffmpeg)"
            )
            if response:
                self.video_format.set("webm")
            else:
                return
        
        # Start download thread
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED, text="⏳ Downloading...")
        self.progress.start(10)
        self.status_label.config(text="Starting download...", fg=self.colors[self.theme.get()]['warning'])
        
        thread = threading.Thread(target=self._download_worker, args=(url,), daemon=True)
        thread.start()
    
    def _download_worker(self, url: str):
        """Worker thread for downloading"""
        try:
            os.makedirs(self.download_folder, exist_ok=True)
            
            mode = self.download_mode.get()
            quality = self.quality.get()
            
            # Build command
            command = ["yt-dlp"]
            
            if mode == "audio":
                fmt = self.audio_format.get()
                command.extend(["-x", "--audio-format", fmt])
                
                # Quality mapping for audio
                if quality == "best":
                    command.extend(["--audio-quality", "0"])
                elif quality == "high":
                    command.extend(["--audio-quality", "2"])
                elif quality == "medium":
                    command.extend(["--audio-quality", "5"])
                else:  # low
                    command.extend(["--audio-quality", "9"])
                
                command.extend(["-f", "bestaudio/best"])
            else:  # video
                fmt = self.video_format.get()
                
                # Quality mapping for video
                if quality == "best":
                    format_str = "bestvideo+bestaudio/best"
                elif quality == "high":
                    format_str = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
                elif quality == "medium":
                    format_str = "bestvideo[height<=720]+bestaudio/best[height<=720]"
                else:  # low
                    format_str = "bestvideo[height<=480]+bestaudio/best[height<=480]"
                
                command.extend(["-f", format_str])
                
                if fmt == "mp4":
                    command.extend(["--merge-output-format", "mp4"])
                else:  # webm
                    command.extend(["--merge-output-format", "webm"])
            
            # Add ffmpeg location if available
            if self.ffmpeg_available:
                command.extend(["--ffmpeg-location", shutil.which("ffmpeg")])
            
            # Output template
            command.extend(["-o", f"{self.download_folder}/%(title)s.%(ext)s"])
            command.append(url)
            
            # Execute download
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Success
                self.root.after(0, self._download_success, url)
            else:
                # Error
                error_msg = result.stderr or "Unknown error"
                self.root.after(0, self._download_error, error_msg)
        
        except Exception as e:
            self.root.after(0, self._download_error, str(e))
    
    def _download_success(self, url: str):
        """Handle successful download"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL, text="⬇️ Download")
        self.progress.stop()
        self.progress_label.config(text="100%")
        self.status_label.config(
            text="✅ Download completed successfully!",
            fg=self.colors[self.theme.get()]['success']
        )
        
        # Add to history
        self._add_to_history(url, "Success")
        
        # Clear URL
        self.url_entry.delete(0, tk.END)
        
        # Reset thumbnail
        if PILLOW_AVAILABLE:
            self.thumbnail_label.configure(
                image='',
                text="🖼️ Thumbnail preview will appear here"
            )
        
        messagebox.showinfo("Success", f"Downloaded successfully!\n\nSaved to: {self.download_folder}")
    
    def _download_error(self, error: str):
        """Handle download error"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL, text="⬇️ Download")
        self.progress.stop()
        self.progress_label.config(text="0%")
        self.status_label.config(
            text="❌ Download failed",
            fg=self.colors[self.theme.get()]['error']
        )
        
        # Add to history
        self._add_to_history(self.url_entry.get(), "Failed")
        
        messagebox.showerror("Download Failed", f"Error: {error[:200]}")
    
    def _add_to_history(self, url: str, status: str):
        """Add download to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mode = self.download_mode.get().upper()
        
        history_item = f"[{timestamp}] {mode} - {status}: {url[:50]}..."
        
        self.download_history.insert(0, {
            'url': url,
            'status': status,
            'timestamp': timestamp,
            'mode': mode
        })
        
        # Keep only last 10
        if len(self.download_history) > 10:
            self.download_history.pop()
        
        # Update listbox
        self.history_listbox.insert(0, history_item)
        if self.history_listbox.size() > 10:
            self.history_listbox.delete(10)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernYouTubeDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
