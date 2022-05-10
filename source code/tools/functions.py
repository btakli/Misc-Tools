import os

import ffmpeg
import pywhatkit as kt
from PIL import Image
from pytube import YouTube
import PySimpleGUI as sg

def youtube_to_mp4(dir: str, isGui : bool = False):
    """Download a YouTube video as an mp4 (and mp3) to the selected directory"""
    outputDir = dir + '/Youtube to MP4'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    #If it is the GUI version, take the input from a popup    
    if not isGui:
        link = input("Please provide a YouTube link:")
    else:
        link = sg.popup_get_text("Please provide a YouTube link:") #I would have liked to have abstracted this better...
    yt = YouTube(link)
    yt_title = yt.title
    print(f"Downloading video \"{yt_title}\" as an mp4 AND mp3 in the folder {outputDir}")
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    yt.download(outputDir)
    filePath = f"{outputDir}/{yt_title}.mp4"
    ffmpeg.input(filePath).output(filePath.replace('.mp4','.mp3')).run()
    print("Done!")
    
    

def mp4_reencode(dir: str, isGui : bool = False):
    """Reencode all mp4s in directory in case there are issues"""
    outputDir = dir + '/reencoded_mp4s'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".mp4" in f):
                print('Reincoding ' + filename)
                ffmpeg.input(f).output(outputDir + '/' + filename).run()
                print("Done!")


def mp3_to_wav(dir: str, isGui : bool = False):
    """Converts all mp3s in a directory to wavs, stores them in a ./wav directory"""
    outputDir = dir + '/wavs'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".mp3" in f):
                print("Converting " + filename + " to wav")
                ffmpeg.input(f).output(outputDir + '/' + filename.replace('.mp3','.wav')).run()
                print("Done!")


def flac_to_mp3(dir: str, isGui : bool = False):
    """Converts all flacs in a directory to mp3s, stores them in a ./mp3 directory"""
    outputDir = dir + '/mp3s'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".flac" in f):
                print("Converting " + filename + " to mp3")
                ffmpeg.input(f).output(outputDir + '/' + filename.replace('.flac','.mp3')).run()

    
def ascii_art_generator(dir: str, isGui : bool = False):
    """Create an ascii art version of all jpgs and pngs in a directory, stored in ./ascii"""
    outputDir = dir + '/ascii'
    fileCount = 0
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    
    for file in os.listdir(dir):
        if file.endswith(".png"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(dir + '/' + file,outputDir + '/' + file.replace(".png",""))
            fileCount += 1
        elif file.endswith(".jpg"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(dir + '/' + file,outputDir + '/' + file.replace(".jpg",""))
            fileCount += 1
        elif file.endswith(".jpeg"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(dir + '/' + file,outputDir + '/' + file.replace(".jpeg",""))
            fileCount += 1
    print(f"Finished generating ASCII art for {fileCount} files.")


def webp_to_png(dir: str, isGui : bool = False):
    """Convert all webp files in a directory to pngs"""
    fileCount = 0
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            
            if (".webp" in f):
                print(f)
                im = Image.open(f).convert("RGBA")
                im.save(f.replace(".webp",".png"),"png")
                fileCount+=1
                os.remove(f)
    print(f"Finished converting {fileCount} files from .webp to .png")

#Mapping of terms to functions
FUNCTION_MAP = {'webptopng' : webp_to_png,
                'asciiart' : ascii_art_generator,
                'flactomp3' : flac_to_mp3,
                'mp3towav' : mp3_to_wav,
                'mp4reencode' : mp4_reencode,
                'youtubetomp4' : youtube_to_mp4
                }
