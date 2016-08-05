'''
Created on Jul 26, 2016

@author: jack
'''

import youtube_dl
import errno
import os
from pydub.audio_segment import AudioSegment
import Parsers

class Entry:
    def __init__(self, name, artist, number, beginning, end):
        self.beginning = beginning
        self.end = end
        self.name = name
        self.artist = artist
        self.number = number
    
    def __repr__(self):
        return self.name + " {" +  str(self.beginning) + ", " + str(self.end) + "}"

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def split_export(entries, longsegment, yt_name):
    make_sure_path_exists(yt_name)
    for i in range(len(entries)):
        print("Writing " + str(i) + "/" + str(len(entries)))
        entry = entries[i]
        currentSoundSegment = longsegment[entry.beginning*1000:entry.end*1000]
        currentSoundSegment.export(yt_name + "/" + entry.name + ".mp3", format='mp3', tags={'title':entry.name, 'artist':entry.artist, 'album':yt_name, 'track':entry.number, 'comments':""}, bitrate="192k", id3v2_version='3')

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download(url):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'largeout.webm',        # name the file the ID of the video
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)  # don't download, much faster
        description = info['description']
        totalDuration = info['duration']
        yt_name = info['title']
        ydl.download([url])
    entries = Parsers.catalystTextParse("catalystdesc.txt", totalDuration)
    #entries = Parsers.dubstepParse(description, totalDuration)
    print("Loading file...")
    # load sound
    sound = AudioSegment.from_mp3("largeout.mp3")
    split_export(entries, sound, yt_name)
    
    