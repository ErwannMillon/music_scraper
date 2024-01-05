from tracemalloc import start
from imageio import save
from pytube import YouTube, Playlist
import ssl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import * 
from scrape_playlist_links import scrape_playlist_links
import os 
import random

from moviepy.editor import VideoFileClip

def get_video_duration(file_path):
    video = AudioFileClip(file_path)
    duration = video.duration
    video.close()
    return int(duration)


ssl._create_default_https_context = ssl._create_unverified_context
jazz_playlist = "https://music.youtube.com/playlist?list=RDCLAK5uy_k3-yjf13QIvUoJbOuOTtTe9NFSP1eruLQ"
afterlife_playlist = "https://music.youtube.com/playlist?list=PLa4hHMeIrG2eVe03bfTb-mV_2xEa2vQEh"
anyma= "https://music.youtube.com/playlist?list=PL5fY5X_Y2UwOS8aVaxLRoM1fZGpLShDh4"
more_afterlife = "https://music.youtube.com/playlist?list=PLukbDkvR954k5Hdn6Qd3tRki3fS5u81Gp"
b = "https://music.youtube.com/playlist?list=PLJpsAlK0tFsboTrRykBU-D_PMz3lYxAcq"





def mp4_to_mp3(mp4_path, save_dir, start_min_offset=20, end_min_offset=10, samples=4, len=None):     
    if len is not None:
        for i in range(samples):
            tmp_trimmed = "tmp_trimmed.mp4"
            duration = get_video_duration(mp4_path)
            start = random.randint(start_min_offset, duration - len - end_min_offset)
            end = start + len
            ffmpeg_extract_subclip(mp4_path, start, end, targetname=tmp_trimmed)
            mp4_without_frames = AudioFileClip(tmp_trimmed)
            mp3_filename = os.path.basename(mp4_path).split(".")[0] + "_" + str(i) + ".mp3"
            mp4_without_frames.write_audiofile(os.path.join(save_dir, mp3_filename))     
        # print(audio_dir + mp3_filename)
        mp4_without_frames.close()


def create_path_if_not_present(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def init_dirs(save_path="./audio"):
    create_path_if_not_present("./tmp")
    create_path_if_not_present(save_path)

def download_playlist(playlist_url, audio_path="./audio_files", video_url_file=None):
    init_dirs(save_path=audio_path)
    song_list = scrape_playlist_links(playlist_url)
    with open ("downloaded_file_log.txt", "r+") as dl_log:
        downloaded_list = dl_log.readlines()
    with open ("downloaded_file_log.txt", "a") as dl_log:
        for song_url in song_list:
            # print(downloaded_list)
            if song_url in downloaded_list:
                print("Already downloaded: ", song_url)
                continue
            song_url.strip("\n")
            try:
                streams = YouTube(song_url).streams
                stream = streams.filter(type="audio").first()
                mp4_path = stream.download(output_path="./tmp")
                mp4_to_mp3(mp4_path, audio_path, len=10, samples=7)
                os.remove(mp4_path)
                dl_log.write(song_url)
            except:
                print("Error downloading: ", song_url)
                continue
    # p = Playlist(test_playlist2)


    # print(p)
    # print()
    # print(p.videos)
    # for song in p.videos:
    #     print(song)
    #     streams = song.streams
    #     stream = streams.filter(type="audio").first()
    #     path = stream.download()
if __name__ == "__main__":
    # download_playlist(test_playlist)
    # mp4_to_mp3("./tmp/Astral.mp4", "./audio")
    # download_playlist(test_playlist)
    # download_playlist(afterlife_playlist, audio_path="./afterlife")
    melodic="https://music.youtube.com/playlist?list=PLSAfbnWypUjTFsqos8lqN-CbHRG2DliFv"
    m2="https://music.youtube.com/playlist?list=PLn7UMvliZ-STmNsp6QijEzn_XI_un5Y2o"
    m3="https://music.youtube.com/playlist?list=PL90e0hlftnXbzid1Wb0Ip_LuH86_RSMjL"
    m4="https://music.youtube.com/playlist?list=PLY_xmUKNvOGy__OeL0mn8p_cdMZgK2K6c"
    m5="https://music.youtube.com/playlist?list=RDCLAK5uy_nX21_ZSVbClYkXhcLsVUEbABHn3ZqgCvs"

    min="https://music.youtube.com/playlist?list=PL25f4TBCk2TZG2fEs44_zg_30S_I0tesa"
    min2="https://music.youtube.com/playlist?list=RDCLAK5uy_lRr2S1Nmk-a4qeSFpU0WoLuVETphGyBP8"

    x = [min, min2, "https://music.youtube.com/playlist?list=PLsCE3Lh_sPx6MPVPQLmon4V3hSwDj0ckv", "https://music.youtube.com/playlist?list=PLMZdEM2S-ZC79vXg4yU2i_OXddCV-KvZP"]
    for playlist in x:
        download_playlist(playlist, audio_path="./afterlife")