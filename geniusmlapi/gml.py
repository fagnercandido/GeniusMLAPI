import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import re

class GeniusLM:

    def __init__(self, token):
        self.token = token

    def search(self, value):
        page_number = 1
        songs = []
        while True:
            genius_search_url = f"http://api.genius.com/search?q={value}&access_token={self.token}&page={page_number}"
            response = requests.get(genius_search_url)
            hits = response.json()['response']['hits']
            if hits:
                for song in hits:
                    songs.append(GeniusSongLM(song["result"]["id"],
                                              song["result"]["title"],
                                              song["result"]["url"],
                                              song["result"]["path"],
                                              song["result"]["header_image_url"],
                                              song["result"]["annotation_count"],
                                              song["result"]["pyongs_count"],
                                              song["result"]["primary_artist"]["id"],
                                              song["result"]["primary_artist"]["name"],
                                              song["result"]["primary_artist"]["url"],
                                              song["result"]["primary_artist"]["image_url"]
                                              ))
                page_number = page_number + 1
            else:
                break
        return songs

    def get_dataframe(self, songs):
        return pd.DataFrame([s.__dict__ for s in songs])

    def search_songs_by_artists_id(self, value):
        page_number = 1
        songs = []
        while True:
            genius_search_url = f"http://api.genius.com/artists/{value}/songs?&access_token={self.token}&page={page_number}"
            response = requests.get(genius_search_url)
            songs_by_artist = response.json()['response']['songs']
            if songs_by_artist:
                for song in songs_by_artist:
                    songs.append(GeniusSongLM(song["id"],
                                              song["title"],
                                              song["url"],
                                              song["path"],
                                              song["header_image_url"],
                                              song["annotation_count"],
                                              song["pyongs_count"],
                                              song["primary_artist"]["id"],
                                              song["primary_artist"]["name"],
                                              song["primary_artist"]["url"],
                                              song["primary_artist"]["image_url"]
                                              ))
                page_number = page_number + 1
            else:
                break
        return songs

class GeniusSongLM:

    def __init__(self, id_song, title, url, path, header_image_url, annotation_count, pyongs_count, primary_artist_id,
                 primary_artits_name, primary_artits_url, primary_artits_imageurl):
        self.id_song = id_song
        self.title = title
        self.url = url
        self.path = path
        self.song = Utils().get_song(self.path)
        self.header_image_url = header_image_url,
        self.annotation_count = annotation_count
        self.pyongs_count = pyongs_count
        self.primary_artist_id = primary_artist_id
        self.primary_artits_name = primary_artits_name
        self.primary_artits_url = primary_artits_url
        self.primary_artits_imageurl = primary_artits_imageurl


class Utils:
    def get_song(self, path):
        url = "https://genius.com" + path
        response_song = requests.get(url)
        html = BeautifulSoup(response_song.content, "lxml")
        lyrics = html.select('div[class^="Lyrics__Container"], .song_body-lyrics p')
        REGEX_TO_CLEAN = re.compile('<.*?>|\[.*?\]')
        song = ''
        for div in lyrics:
            song = song + ' '
            song = song + re.sub(REGEX_TO_CLEAN, ' ', ' '.join([item.decode() if type(item) is Tag else item for item in div.contents]))
        return song