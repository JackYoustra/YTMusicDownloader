'''
Created on Jul 27, 2016

@author: jack
'''
import re
import FileDownloader
def timestring_to_seconds(timestring):
    seconds = 0
    timesections = timestring.split(":")
    seconds += int(timesections[len(timesections)-1])
    seconds += int(timesections[len(timesections)-2]) * 60
    if len(timesections) == 3:
        # runs if an hour component exists
        seconds += int(timesections[len(timesections)-3])*60*60
    return seconds

#https://www.youtube.com/watch?v=fWRISvgAygU
def dubstepParse(description, overallTime):
    entryList = []
    
    validLines = []
    lines = description.splitlines()
    pattern = re.compile("[a-zA-Z]\s([0-9]:)?[0-9]{1,2}:[0-9]{1,2}$") #Killigrew - Timeless As The Waves 1:44:58
    for line in lines:
        matchobj = pattern.search(line)
        if matchobj != None:
            validLines.append(line)
    
    nameList = []
    artistList = []
    secondsList = []
    for line in validLines:
        index = line.rindex(' ')
        prefixBlob = line[:index].split(' - ')
        name = prefixBlob[1]
        artist = prefixBlob[0]
        timeString = line[index:]
        seconds = timestring_to_seconds(timeString)
        nameList.append(name)
        artistList.append(artist)
        secondsList.append(seconds)
    
    assert len(nameList) == len(secondsList)
    startTime = 0
    ## add last time
    secondsList.append(overallTime)
    for index in range(1, len(secondsList)):
        # will go through end times for all if last time appended
        currentEnd = secondsList[index]
        name = nameList[index-1]
        artist = artistList[index-1]
        entry = FileDownloader.Entry(name, artist, index, startTime, currentEnd)
        entryList.append(entry)
        startTime = currentEnd
    
    return entryList

def catalystTextParse(path, overallTime):
    with open (path,"r") as catalystDescFile:
        lines = catalystDescFile.readlines()
    entryList = []
    
    nameList = []
    secondsList = []
    for line in lines:
        sections = line.split(' - ')
        timeString = sections[0]
        name = sections[1]
        name = name.replace("\n", "")
        seconds = timestring_to_seconds(timeString)
        nameList.append(name)
        secondsList.append(seconds)
    
    assert len(nameList) == len(secondsList)
    startTime = 0
    ## add last time
    secondsList.append(overallTime)
    for index in range(1, len(secondsList)):
        # will go through end times for all if last time appended
        currentEnd = secondsList[index]
        name = nameList[index-1]
        artist = "Solar Fields"
        entry = FileDownloader.Entry(name, artist, index, startTime, currentEnd)
        entryList.append(entry)
        startTime = currentEnd
    
    return entryList
    
    