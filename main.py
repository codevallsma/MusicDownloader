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

DEVELOPER_KEY = 'REPLACE_ME'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DESTINATION = '/home/codevallsma/Documentos/Projectes_personals/MusicDownloader'


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def downloadMusic(video_id, destinationFolder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': destinationFolder + '/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + video_id])


if __name__ == '__main__':
    # asking the user which music wants to download
    print("Insert the song to download: ")
    song = input()
    print("Select the destination folder")
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    # creating the youtube search class
    ys = YoutubeSearchClass(DEVELOPER_KEY, YOUTUBE_API_VERSION, song)

    try:
        ys.youtube_search()
        downloadMusic(ys.videos[0].id, folder_selected)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
