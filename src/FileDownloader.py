'''
Created on Jul 26, 2016

@author: jack
'''

import youtube_dl

def download(url):
    options = {
        'format': 'bestaudio/best', # choice of quality
        'extractaudio' : True,      # only keep the audio
        'audioformat' : "mp3",      # convert to mp3 
        'outtmpl': '%(id)s',        # name the file the ID of the video
        'noplaylist' : True,        # only download single song, not playlist
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)  # don't download, much faster
        description = info['description']
        print(description)
        #ydl.download([url])