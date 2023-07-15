"""
usage:
yt-dlp -o video1.mp4 -f mp4 https://www.youtube.com/watch?v=Pl3AnYCeTrU
python transcribe.py video1.mp4

this will take a while.

make video with srt file.
`ffmpeg -i video1.mp4 -vf subtitles=video1.srt -y output1.mp4`


or you want to play the video with CC by yourself

open video1.mp4
python play_cc.py video1.mp4.csv 


one time setup:
```
brew install ffmpeg
pip install ffmpeg-python
pip install yt-dlp
```

"""

import os
import sys
import csv
from datetime import datetime

import whisper
from whisper.utils import get_writer

def format_item(item):
    return [item["start"], item["text"]]

def transcribe(model, filename):
    result = model.transcribe(filename, beam_size=5, fp16=False, verbose=True)
    # os.remove(video["file_name"])

    print(result["text"])

    # save SRT
    srt_writer = get_writer('srt', './')
    srt_writer(result, filename, {
        'word_timestamps': False,
        'max_line_width': 1000,
        'max_line_count': 100,
        'highlight_words': False})

    segments = []
    for item in result["segments"]:
        segments.append(format_item(item))

    return segments


# main
print(sys.argv)
input_fn = sys.argv[1]
csv_fn = input_fn + '.csv'

# https://github.com/openai/whisper
# model_name = "base.en"
model_name = "small.en"
# model_name = "medium.en"  # very slow

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

model = whisper.load_model(model_name)
segments = transcribe(model, input_fn)

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

# open the file in the write mode
f = open(csv_fn, 'w')

# create the csv writer
writer = csv.writer(f)

writer.writerow(['start', 'text'])

for row in segments:
    # write a row to the csv file
    writer.writerow(row)

# close the file
f.close()

print(f"saved to {csv_fn}")
