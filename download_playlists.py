from tracemalloc import start
from imageio import save
from pytube import YouTube, Playlist
import ssl
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import * 
from scrape_playlist_links import scrape_playlist_links
ssl._create_default_https_context = ssl._create_unverified_context
jazz_playlist = "https://music.youtube.com/playlist?list=RDCLAK5uy_k3-yjf13QIvUoJbOuOTtTe9NFSP1eruLQ"
test_playlist = "https://music.youtube.com/playlist?list=RDCLAK5uy_lRr2S1Nmk-a4qeSFpU0WoLuVETphGyBP8"
def mp4_to_mp3(mp4, audio_dir, start_time=40, len=None):     
	tmp_trimmed = mp4
	if len is not None:
		tmp_trimmed = "tmp_trimmed.mp4"
		ffmpeg_extract_subclip(mp4, start_time, start_time + len, targetname=tmp_trimmed)
	mp4_without_frames = AudioFileClip(tmp_trimmed)
	mp3_filename = mp4[mp4.rfind("/"):mp4.find(".mp4")] + ".mp3"
	# print(audio_dir + mp3_filename)
	mp4_without_frames.write_audiofile(audio_dir + mp3_filename)     
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
			print(downloaded_list)
			if song_url in downloaded_list:
				continue
			song_url.strip("\n")
			streams = YouTube(song_url).streams
			stream = streams.filter(type="audio").first()
			mp4_path = stream.download(output_path="./tmp")
			mp4_to_mp3(mp4_path, audio_path)
			os.remove(mp4_path)
			dl_log.write(song_url)
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
	download_playlist(jazz_playlist, audio_path="./jazz_songs")