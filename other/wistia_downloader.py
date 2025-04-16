# Wistia video downloader
# Optional Whisper subtitle generation via CLI
#
# Requirements:
# - For download only: requests package
# - For subtitle generation: ffmpeg and whisper
#
# How to get the video ID: https://gist.github.com/szepeviktor/2a8a3ce8b32e2a67ca416ffd077553c5

import subprocess
import requests
import sys
import re

usage = "Usage: python wistia_downloader.py <id> <optional:whisper>"

if len(sys.argv) > 3 or len(sys.argv) < 2:
    print(usage)
    sys.exit(1)

whisper = False

if len(sys.argv) == 3:
    if sys.argv[2] == "whisper":
        whisper = True
    else:
        print(usage)

char_limit_name = 38

wistia_url = "https://fast.wistia.net/embed/iframe/"
wistia_id = sys.argv[1]


wistia_download = wistia_url + wistia_id

try:
    res = requests.get(wistia_download)
    res.raise_for_status()
    html_res = res.text

    match_video = re.search(
        r'"type":"original".*?"url":"(https://[^"]+\.bin)"', html_res)
    match_video_name = re.search(r'<title>(.*?[^<]+)', html_res)

    video_name = re.sub(r'[<>:"/\\|?*]', "",
                        match_video_name.group(1)).strip() + ".mp4"
    if len(video_name) > char_limit_name:
        video_name = video_name[-char_limit_name:]

    url = match_video.group(1)
    video_res = requests.get(url, stream=True)
    video_res.raise_for_status()

    with open(video_name, "wb") as f:
        for chunk in video_res.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Download completed.")

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)
except requests.exceptions.RequestException as e:
    print("Request error:", e)
except Exception as e:
    print("Unexpected error:", e)

if whisper:
    try:
        audio_name = video_name.replace(".mp4", ".wav")
        subprocess.run(
            f"ffmpeg -i .\\{video_name} -vn -ar 16000 -ac 1 -c:a pcm_s16le .\\{audio_name}", shell=True, check=True)
    except:
        print("FFmpeg Conversion Error.")

    try:
        subprocess.run(
            f"whisper .\\{audio_name} --model base --output_format srt", shell=True, check=True)
    except:
        print("Unexpected FFmpeg Processing Error.")
