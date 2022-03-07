from ytmusicapi import YTMusic
import json
import asyncio
import aiofiles
from ppadb.client_async import ClientAsync as AdbClient
# 117564047350972400176
# YTMusic.setup(filepath="headers_auth.json")
from ppadb.client import Client as AdbClient
from tinytag import TinyTag
from os import remove
pl = open("new.txt", "r")
log = open("log.txt", "w")
lines = pl.readlines()
pl.close()
async def main():
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device("19291FDF600G8R")


    ytmusic = YTMusic('headers_auth.json', "117564047350972400176")
    # tag = TinyTag.get("n/Dave Freestyle With The LA Leakers   #Freestyle007 - Copy.m4a")
    zzplaylist = ytmusic.get_playlist("PLF_jnIDK_v9mf26vqOGJs2xjYYLmIvUPw")
    playlist = "PLF_jnIDK_v9mf26vqOGJs2xjYYLmIvUPw"
    # createdpl = ytmusic.create_playlist(title = "test_playlist", description = "test")
    for path in lines:
        filename = path.split("/")[-1].strip('\n')
        path = path.strip('\n')
        # print(path)
        # print(filename)
        # print()

        device.pull(path, f'tmp/{filename}')
        tag = TinyTag.get(f'tmp/{filename}')
        print(f'title {tag.title} by {tag.artist}.')
        query = tag.title + tag.artist
        list = ytmusic.search(query, limit=1, filter = "songs", ignore_spelling=True)
        if list:    
            add = [list[0]["videoId"]]
            print(add)
            ytmusic.add_playlist_items(playlist, add)
            # for item in list:
                # print(item["videoId"])
                # print("\n")
        else:
            log.write(path.split("/")[-1])
            log.write("\n")

        # remove(f'tmp/{filename}')
    log.close()
    log = open("log.txt", "r")
    loglines = log.readlines()
    for line in loglines:
        query = line.strip("\n")
        list = ytmusic.search(query, limit=1, filter = "songs", ignore_spelling=True)
        if list:    
            add = [list[0]["videoId"]]
            print(add)
            ytmusic.add_playlist_items(playlist, add)
            # for item in list:
                # print(item["videoId"])
                # print("\n")
    # for item in list:
    #     print(item)
    #     print("\n")

asyncio.run(main())

log.close()