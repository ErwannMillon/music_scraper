import ssl
from ytmusicapi import YTMusic
from pytube import YouTube
import json
import re
import asyncio
import aiofiles
from os import remove
import pprint 
pp = pprint.PrettyPrinter(indent=4)
from pytube import Playlist
base_url = "https://music.youtube.com/watch?v="
ssl._create_default_https_context = ssl._create_unverified_context
test_playlist = "https://music.youtube.com/playlist?list=RDCLAK5uy_lRr2S1Nmk-a4qeSFpU0WoLuVETphGyBP8"
test_playlist2 = "https://www.youtube.com/playlist?list=PLxI6IWh7Z6bqIMMIzWyVMcgrfEj6K43i5"
# playlist_id = "RDCLAK5uy_lRr2S1Nmk-a4qeSFpU0WoLuVETphGyBP8"

def scrape_playlist_links(playlist_link=test_playlist):
    ytmusic = YTMusic()
    playlist_id = playlist_link[playlist_link.find("=") + 1:]
    playlist_tracks = ytmusic.get_watch_playlist(playlistId=playlist_id, limit=60)['tracks']
    # print(pl[0])
    with open("songs.txt", "w+") as file:
        current_list = file.readlines()
    with open("songs.txt", "a") as file:
        for track in playlist_tracks:
            track_url = base_url + track["videoId"] + "\n"
            if track_url not in current_list:
                file.write(track_url)
                current_list.append(track_url)
    return current_list

def pytube_playlist():
    p = Playlist(test_playlist2)
    print(p)
    print()
    print(p.videos)
    for song in p.videos:
        print(song)
        streams = song.streams
        stream = streams.filter(type="audio").first()
        path = stream.download()
if __name__ == "__main__":
    # scrape_playlist_links()
    pytube_playlist()
