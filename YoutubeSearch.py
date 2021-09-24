# We use the "class" statement to create a class
from googleapiclient.discovery import build


class searchResultClass():
    def __init__(self, id, title):
        self.id = id
        self.title = title


class YoutubeSearchClass:
    # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
    # tab of
    #   https://cloud.google.com/console
    # Please ensure that you have enabled the YouTube Data API for your project.

    # INIT METHOD
    def __init__(self, DEVELOPER_KEY, YOUTUBE_API_VERSION, song):
        self.DEVELOPER_KEY = DEVELOPER_KEY
        self.YOUTUBE_API_VERSION = YOUTUBE_API_VERSION
        self.songName = song
        self.youtube = build('youtube', YOUTUBE_API_VERSION,
                             developerKey=DEVELOPER_KEY)

    def youtube_search(self):

        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = self.youtube.search().list(
            q=self.songName,
            part='id,snippet',
            maxResults=25
        ).execute()

        self.videos = []
        self.channels = []
        self.playlists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                self.videos.append(searchResultClass(search_result['id']['videoId'],
                                                     search_result['snippet']['title']))
            elif search_result['id']['kind'] == 'youtube#channel':
                self.channels.append('%s (%s)' % (search_result['snippet']['title'],
                                                  search_result['id']['channelId']))
            elif search_result['id']['kind'] == 'youtube#playlist':
                self.playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                                   search_result['id']['playlistId']))

        print('Videos:\n', self.videos[0].title, '\n')
        print('Channels:\n', '\n'.join(self.channels), '\n')
        print('Playlists:\n', '\n'.join(self.playlists), '\n')
