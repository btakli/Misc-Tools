import os
from PIL import Image
import pywhatkit as kt
import ffmpeg

def mp4_reencode(dir: str):
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


def mp3_to_wav(dir: str):
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


def flac_to_mp3(dir: str):
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

    
def ascii_art_generator(dir: str):
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
        if file.endswith(".jpg"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(dir + '/' + file,outputDir + '/' + file.replace(".jpg",""))
            fileCount += 1
    print(f"Finished generating ASCII art for {fileCount} files.")


def webp_to_png(dir: str):
    """Convert all webp files in a directory to pngs"""
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            if (".webp" in f):
                im = Image.open(f).convert("RGBA")
                im.save(f.replace(".webp",".png"),"png")
                os.remove(f)

#Mapping of terms to functions
FUNCTION_MAP = {'webptopng' : webp_to_png,
                'asciiart' : ascii_art_generator,
                'flactomp3' : flac_to_mp3,
                'mp3towav' : mp3_to_wav,
                'mp4reencode' : mp4_reencode
                }