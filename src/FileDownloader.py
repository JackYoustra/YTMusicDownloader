'''
Created on Jul 26, 2016

@author: jack
'''

import youtube_dl
import errno
import os
from pydub.audio_segment import AudioSegment
import regex as re

class Entry:
    def __init__(self, name, beginning, end):
        self.beginning = beginning
        self.end = end
        self.name = name

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def timestring_to_seconds(timestring):
    seconds = 0
    timesections = timestring.split(":")
    seconds += int(timesections[len(timesections)-1])
    seconds += int(timesections[len(timesections)-2]) * 60
    if len(timesections) == 3:
        # runs if an hour component exists
        seconds += int(timesections[len(timesections)-3])*60*60
    return seconds

def parse(description, overallTime):
    entryList = []
    
    validLines = []
    lines = description.splitlines()
    pattern = re.compile("[A-Z]\s[0-9]?:[0-9]{1,2}:[0-9]{1,2}$") #Killigrew - Timeless As The Waves 1:44:58
    for line in lines:
        matchobj = pattern.search(line)
        if matchobj == None:
            validLines.append(line)
    
    nameList = []
    secondsList = []
    for line in validLines:
        index = line.rindex('\s')
        name = line[:index]
        timeString = line[index:]
        seconds = timestring_to_seconds(timeString)
        nameList.append(name)
        secondsList.append(seconds)
    
    assert len(nameList) == len(secondsList)
    startTime = 0
    ## add last time
    secondsList.append(overallTime)
    for index in range(len(1, secondsList)):
        # will go through end times for all if last time appended
        currentEnd = secondsList[index]
        entry = Entry(name, startTime, currentEnd)
        entryList.append(entry)
        startTime = currentEnd
    
    return entryList

def download(url):
    options = {
        'format': 'bestaudio/best', # choice of quality
        'extractaudio' : True,      # only keep the audio
        'audioformat' : "mp3",      # convert to mp3 
        'outtmpl': 'largeout',        # name the file the ID of the video
        'noplaylist' : True,        # only download single song, not playlist
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)  # don't download, much faster
        description = info['description']
        #ydl.download([url])
    print(description)
    # load sound
    AudioSegment.from_mp3("largeout.mp3")
    make_sure_path_exists("music/")
    
    
    