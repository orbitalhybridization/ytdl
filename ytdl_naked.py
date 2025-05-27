import os
import sys
from pytubefix import YouTube
from pydub import AudioSegment
import re

DOWNLOADS = "C:\\Users\\iljac\\Music\\yt\\"  # Make sure this path exists or is writable

def download_audio(url, filetype='wav'):
    try:
        print(f"Downloading audio from: {url}")
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        filename = "temp_audio"
        temp_path = stream.download(filename=filename)
        print("Download complete.")

        print("Converting audio...")
        audio = AudioSegment.from_file(temp_path)
        os.makedirs(DOWNLOADS, exist_ok=True)
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", yt.title)
        export_filename = os.path.join(DOWNLOADS, f"{safe_title}.{filetype}")
        audio.export(export_filename, format=filetype)
        print(f"Saved as: {export_filename}")

        os.remove(temp_path)
        print("Temporary file removed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yt_audio_download.py <YouTube_URL> [filetype]")
        sys.exit(1)

    url = sys.argv[1]
    filetype = sys.argv[2] if len(sys.argv) > 2 else 'wav'
    download_audio(url, filetype)
