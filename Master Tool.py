import os
from PIL import Image
import argparse
import pywhatkit as kt
import sys
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
                print('Done!')


def mp3_to_wav(dir: str):
    """Converts all mp3s in a directory to wavs, stores them in a ./wav directory"""
    outputDir = dir + '/wavs'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".mp3" in f):
                print('Converting ' + filename + ' to wav')
                ffmpeg.input(f).output(outputDir + '/' + filename.replace('.mp3','.wav')).run()
                print("Done!")
                #sound = AudioSegment.from_mp3(f)
                #sound.export(outputDir + '/' + filename.replace('.mp3','.wav'), format="wav")


def flac_to_mp3(dir: str):
    """Converts all flacs in a directory to mp3s, stores them in a ./mp3 directory"""
    outputDir = dir + '/mp3s'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    bitrate = input("Enter bitrate [format: ###k] (leave blank for default): ")
    
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".flac" in f):
                print('Converting ' + filename + ' to mp3')
                ffmpeg.input(f).output(outputDir + '/' + filename.replace('.flac','.mp3')).run()
                print("Done!")
                #sound = AudioSegment.from_file(f,format='flac')
                #sound.export(outputDir + '/' + filename.replace('.flac','.mp3'), format="mp3")

    
def ascii_art_generator(dir: str):
    """Create an ascii art version of all jpgs and pngs in a directory, stored in ./ascii"""
    outputDir = dir + '/ascii'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    
    for file in os.listdir(dir):
        if file.endswith(".png"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(dir + '/' + file,outputDir + '/' + file.replace(".png",""))
        if file.endswith(".jpg"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(dir + '/' + file,outputDir + '/' + file.replace(".jpg",""))


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


def main():
    """Main method, uses argparse to parse commandline arguments to use the different tools"""
    #Mapping of terms to functions
    FUNCTION_MAP = {'webptopng' : webp_to_png,
                    'asciiart' : ascii_art_generator,
                    'flactomp3' : flac_to_mp3,
                    'mp3towav' : mp3_to_wav,
                    'mp4reencode' : mp4_reencode
                    }
    #Descriptions of each tool based on the docstring
    helpList = []
    for key in FUNCTION_MAP:
        helpList.append(key + ': ' + FUNCTION_MAP[key].__doc__)
    toolHelpString = 'Choose a tool from the provided list of tools: '
    for helpString in helpList:
        toolHelpString += helpString + ' | '

    #Description of the tools
    parser = argparse.ArgumentParser(description='Master tool, allows you to select the different tools I created')

    #Non optional argument, this is the specific tool that we wish to call
    parser.add_argument('tool',choices=FUNCTION_MAP.keys(), help=toolHelpString)
    #Directory the tool will operate on, defaults to current directory
    parser.add_argument('-d','--directory',nargs='?',type=str,default='./', help='Choose a directory for the tool to operate on, defaults to your current directory')

    args = parser.parse_args()

    chosenFunction = FUNCTION_MAP[args.tool]

    dir = args.directory
    if not os.path.isdir(dir):
        print("Invalid directory: \"" + dir + "\", defaulting to current directory...") 
        dir = './'
    chosenFunction(dir) #Call the function using the specified directory

    print('Done! Thank you for using the program, terminating.\n')
    sys.exit()


if __name__ == "__main__":
    main()