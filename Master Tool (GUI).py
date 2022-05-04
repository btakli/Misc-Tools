import os
from PIL import Image
import pywhatkit as kt
import sys
import ffmpeg
import PySimpleGUI as sg

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
                print("Converting " + filename + " to mp3")
                ffmpeg.input(f).output(outputDir + '/' + filename.replace('.flac','.mp3')).run()
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
    #Mapping of terms to functions
    FUNCTION_MAP = {'webptopng' : webp_to_png,
                    'asciiart' : ascii_art_generator,
                    'flactomp3' : flac_to_mp3,
                    'mp3towav' : mp3_to_wav,
                    'mp4reencode' : mp4_reencode
                    }
    
    #Column showing files and allowing you to select a folder
    file_list_column = [
    [
        sg.Text("Choose folder to operate on"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(initial_folder='./'),
    ],
    ]

    toolList = []
    for key in FUNCTION_MAP:
            toolList.append(sg.Button(button_text=key,tooltip=FUNCTION_MAP[key].__doc__))
    
    #Column listing tools
    tools_column = [
        [sg.Text("Choose a tool to use on the selected folder")]
    ]
    tools_column.append(toolList)

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(tools_column),
            sg.VSeperator(),
            sg.Output(background_color='black',text_color='green', size=(200,400))
        ]
    ]

    window = sg.Window("Tool Selector", layout,size=(1200, 300))

    folder = './'
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
        elif event == '-FOLDER-':
            folder = values["-FOLDER-"]
        elif event in FUNCTION_MAP:
            toolCalled = FUNCTION_MAP[event]
            toolCalled(folder)
        

    window.close()

if __name__ == "__main__":
    main()