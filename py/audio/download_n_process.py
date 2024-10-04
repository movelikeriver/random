
# pip install yt-dlp
# pip install ffmpeg-python
# brew install ffmpeg

import os
import sys

import whisper
import yt_dlp



class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')




def format_item(item):
    return {
        "time": item["start"],
        "text": item["text"]
    }

def transcribe(model, filename):
    # video = download_video(url)
    result = model.transcribe(filename, beam_size=5, fp16=False)
    # os.remove(video["file_name"])

    # result = model.transcribe("video/test.mp4", beam_size=5)

    print(result["text"])
    segments = []
    for item in result["segments"]:
        segments.append(format_item(item))

    print('------------------')    
    print(segments)



# main
print(sys.argv)
# 'https://www.youtube.com/watch?v=BjZXRs6fAkA'
urls = [sys.argv[1]]
filename = 'out/video1.mp4'

ydl_opts = {
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'format': 'best',
    # 'outtmpl': 'output',
    'output': filename,
}

print(f"downloading {urls} to {filename}")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)


model_name = "base.en"
model = whisper.load_model(model_name)


transcribe(model, filename)

