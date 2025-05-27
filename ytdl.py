import os
import tkinter as tk
from tkinter import ttk, messagebox
from pytubefix import YouTube
from pydub import AudioSegment
import platform
import subprocess
import threading
import re

DOWNLOADS = "C:\\Users\\iljac\\Music\yt\\"

def download_audio():
    def task():
        progress["value"] = 10
        url = url_entry.get()
        filetype = filetype_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            filename = "temp_audio"
            status_label.config(text="Downloading...")
            temp_path = stream.download(filename=filename)
            progress["value"] = 40

            status_label.config(text="Converting...")
            audio = AudioSegment.from_file(temp_path)
            export_dir = DOWNLOADS
            os.makedirs(export_dir, exist_ok=True)
            safe_title = re.sub(r'[\\/*?:"<>|]', "_", yt.title)
            export_filename = os.path.join(DOWNLOADS, f"{safe_title}.{filetype}")
            audio.export(export_filename, format=filetype)
            progress["value"] = 80

            os.remove(temp_path)
            status_label.config(text="Done!")
            progress["value"] = 100
            messagebox.showinfo("Success", f"Saved as {export_filename} in {export_dir}")

        except Exception as e:
            status_label.config(text="Error")
            messagebox.showerror("Download Error", str(e))
        finally:
            progress["value"] = 0

    threading.Thread(target=task).start()

def open_downloads_folder():
    path = os.path.abspath(DOWNLOADS)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])

# GUI setup
root = tk.Tk()
root.title("YouTube to Audio Downloader")
root.geometry("400x250")

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

filetype_var = tk.StringVar(value='wav')
ttk.Label(root, text="Output Format:").pack(pady=5)
ttk.Combobox(root, textvariable=filetype_var, values=['wav', 'mp3'], state="readonly").pack()

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

ttk.Button(root, text="Download", command=download_audio).pack(pady=5)
ttk.Button(root, text="Open Downloads Folder", command=open_downloads_folder).pack()

root.mainloop()

# pyinstaller --noconsole --onefile ytdl.py
