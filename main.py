#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..
from __future__ import unicode_literals
import youtube_dl
from googleapiclient.errors import HttpError
from YoutubeSearch import YoutubeSearchClass
from tkinter import filedialog
from tkinter import *
import argparse
import os

DEVELOPER_KEY = 'YOUR_DEV_KEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def downloadMusic(video_id, destinationFolder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': destinationFolder + '/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + video_id])


def checkParameters(textToPrint, variable):
    if variable is None:
        print(textToPrint)
        return input()
    return variable


def checkAllParameters(args):
    #if -f present do not ask to select directory
    if not args.f:
        root = Tk()
        root.withdraw()
        filePath = filedialog.askdirectory()
    else:
        filePath = args.f
    song = checkParameters("Insert the song to download: ", args.s)
    return song, filePath


def argumentParser():
    parser = argparse.ArgumentParser("musicDownloader")
    parser.add_argument("-f", help="Destination path to download the music")
    parser.add_argument("-s", help="Name of the song to be downloaded, if it contains spaces use quotation marks.\n "
                                   "Example -s \"name of the song\"")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    argument = argumentParser()
    song , folder_selected = checkAllParameters(argument)
    # creating the youtube search class
    ys = YoutubeSearchClass(DEVELOPER_KEY, YOUTUBE_API_VERSION, song)

    try:
        ys.youtube_search()
        downloadMusic(ys.videos[0].id, folder_selected)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
