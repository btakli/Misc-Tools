from functions import *
import os
from PIL import Image
import argparse
import pywhatkit as kt
import sys
import ffmpeg

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