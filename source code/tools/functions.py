import os
import re

import ffmpeg
import natsort
import PySimpleGUI as sg
import pywhatkit as kt
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from pytube import YouTube


def youtube_to_mp4(dir: str, isGui: bool = False):
    """Download a YouTube video as an mp4 (and mp3) to the selected directory"""
    outputDir = dir + '/Youtube to MP4'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    # If it is the GUI version, take the input from a popup
    if not isGui:
        link = input("Please provide a YouTube link:")
    else:
        # I would have liked to have abstracted this better...
        link = sg.popup_get_text("Please provide a YouTube link:")
    yt = YouTube(link)
    yt_title = yt.title
    print(
        f"Downloading video \"{yt_title}\" as an mp4 AND mp3 in the folder {outputDir}")
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()
    yt.download(outputDir)

    # Stripped of invalid chars (emojis, etc.)
    yt_titleStripped = re.sub('[#%&{}\<>*?/$!\'":@+`|=]', '', yt_title)
    filePath = f"{outputDir}/{yt_titleStripped}.mp4"

    print(f"file name {yt_titleStripped}")
    ffmpeg.input(filePath).output(filePath.replace('.mp4', '.mp3')).run()
    print("Done!")


def mp4_reencode(dir: str, isGui: bool = False):
    """Reencode all mp4s in directory in case there are issues"""
    outputDir = dir + '/reencoded_mp4s'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    # Check for any mp4s in the directory
    mp4s = []
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".mp4" in f):
                mp4s.append(f)
    print(f"Found {len(mp4s)} mp4s in the directory {dir}")
    if len(mp4s) == 0:
        print("No mp4s found, terminating...")
        return

    for mp4 in mp4s:
        print(f"Reencoding {mp4}")
        ffmpeg.input(mp4).output(mp4.replace(dir, outputDir)).run()
        print("Done!")


def mp3_to_wav(dir: str, isGui: bool = False):
    """Converts all mp3s in a directory to wavs, stores them in a ./wav directory"""
    outputDir = dir + '/wavs'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    # Check for any mp3s in the directory
    mp3s = []
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".mp3" in f):
                mp3s.append(f)

    print(f"Found {len(mp3s)} mp3s in the directory {dir}")
    if len(mp3s) == 0:
        print("No mp3s found, terminating...")
        return

    for mp3 in mp3s:
        print(f"Converting {mp3} to wav")
        ffmpeg.input(mp3).output(mp3.replace(
            dir, outputDir).replace(".mp3", ".wav")).run()
        print("Done!")


def flac_to_mp3(dir: str, isGui: bool = False):
    """Converts all flacs in a directory to mp3s, stores them in a ./mp3 directory"""
    outputDir = dir + '/mp3s'
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    # Check for any flacs in the directory
    flacs = []
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            if (".flac" in f):
                flacs.append(f)

    print(f"Found {len(flacs)} flacs in the directory {dir}")
    if len(flacs) == 0:
        print("No flacs found, terminating...")
        return

    for flac in flacs:
        print(f"Converting {flac} to mp3")
        ffmpeg.input(flac).output(flac.replace(
            dir, outputDir).replace(".flac", ".mp3")).run()
        print("Done!")


def ascii_art_generator(dir: str, isGui: bool = False):
    """Create an ascii art version of all jpgs and pngs in a directory, stored in ./ascii"""
    outputDir = dir + '/ascii'
    fileCount = 0
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    for file in os.listdir(dir):
        if file.endswith(".png"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(
                dir + '/' + file, outputDir + '/' + file.replace(".png", ""))
            fileCount += 1
        elif file.endswith(".jpg"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(
                dir + '/' + file, outputDir + '/' + file.replace(".jpg", ""))
            fileCount += 1
        elif file.endswith(".jpeg"):
            print("Converting " + file + " to ascii art\n")
            kt.image_to_ascii_art(
                dir + '/' + file, outputDir + '/' + file.replace(".jpeg", ""))
            fileCount += 1
    print(f"Finished generating ASCII art for {fileCount} files.")


def webp_to_png(dir: str, isGui: bool = False):
    """Convert all webp files in a directory to pngs"""
    fileCount = 0
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        # checking if it is a file
        if os.path.isfile(f):

            if (".webp" in f):
                print(f)
                im = Image.open(f).convert("RGBA")
                im.save(f.replace(".webp", ".png"), "png")
                fileCount += 1
                os.remove(f)
    print(f"Finished converting {fileCount} files from .webp to .png")


def add_images_to_pdf(dir: str, isGui: bool = False):
    """Add all images (.png, .jpg, .jpeg) to a PDF bearing the name of the folder.
    Puts it in the parent directory."""
    folder_name = dir.split("\\")[-1]

    if os.path.isdir(dir):
        print(f"Examining if PDF should be created for folder {folder_name}")
        image_list = []

        for file in natsort.natsorted(os.listdir(dir)):
            print(file)
            file = os.path.join(dir, file)

            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                image_list.append(Image.open(file).convert("RGB"))

        print(f"{len(image_list)} images found...")

        if len(image_list) > 1:
            print("Creating PDF...")

            pdf_name = f"{folder_name}.pdf"
            parent_directory = os.path.join(dir, "../")
            pdf_path = os.path.join(parent_directory, pdf_name)

            image_list[0].save(pdf_path, resolution=100.0,
                               save_all=True, append_images=image_list[1:])

            print(f"PDF {pdf_path} created.")
        else:
            print("Not enough images to warrant PDF creation, exiting...")
            return


def order_double_sided_scan(dir: str, isGui: bool = False):
    """Takes PDFs of a double sided scan, where you do one pass of the front and then one pass of the back (just flip the stack over)
    and save it in the same PDF. orders the pages so that they are in the correct order.

    NOTE: If there are multiple PDFs in the directory, it will do all of them.

    Files are saved as <original filename>_ordered.pdf"""
    folder_name = dir.split("\\")[-1]
    if os.path.isdir(dir):
        # Scan for PDFs
        pdf_list = []
        for file in os.listdir(dir):
            file = os.path.join(dir, file)
            if file.lower().endswith((".pdf")) and not file.lower().endswith(("_ordered.pdf")):  # Ignore already ordered PDFs
                pdf_list.append(file)

        print(f"Found {len(pdf_list)} PDFs in directory {folder_name}...")
        for pdf in pdf_list:
            print(pdf)

        if len(pdf_list) > 0:
            # If there are multiple PDFs, ask the user which one to use
            for pdf in pdf_list:
                print(f"Performing operation on {pdf}")
                # Open the PDF
                pdf_file = open(pdf, 'rb')
                pdf_reader = PdfReader(pdf_file)
                pdf_writer = PdfWriter()

                # Get the number of pages in the PDF
                num_pages = len(pdf_reader.pages)

                # If the number of pages is odd, It was scanned incorrectly
                if num_pages % 2 != 0:
                    print(
                        f"Odd number of pages for PDF {pdf}, meaning it cannot be a true double sided scan! Skipping...")
                    continue

                # Order the pages so that they are in the correct order. The scan order is all the front pages, then all the back pages, so we need to reorder them so that they are in the correct order.
                for i in range(0, num_pages // 2):
                    pdf_writer.add_page(pdf_reader.pages[i])
                    pdf_writer.add_page(pdf_reader.pages[num_pages - i - 1])

                # Save the PDF
                output_filename = f'{pdf.split(".")[0]}_ordered.pdf'
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
                print(f"PDF saved as {output_filename}")
        else:
            print("No PDFs found, exiting...")
            return


# Mapping of terms to functions
FUNCTION_MAP = {'webptopng': webp_to_png,
                'asciiart': ascii_art_generator,
                'flactomp3': flac_to_mp3,
                'mp3towav': mp3_to_wav,
                'mp4reencode': mp4_reencode,
                'youtubetomp4': youtube_to_mp4,
                'addimagestopdf': add_images_to_pdf,
                'orderdoublesidedscan': order_double_sided_scan
                }
