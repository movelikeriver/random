import hashlib
from pytube import YouTube

def download_video(url):
    yt = YouTube(url)
    print(dir(yt))
    hash_file = hashlib.md5()
    #    print(yt.title)
    #    hash_file.update(yt.title.encode())
    file_name = f'{hash_file.hexdigest()}.mp4'
    yt.streams.first().download("", file_name)

    return {
        "file_name": file_name,
        "title": yt.title
    }
