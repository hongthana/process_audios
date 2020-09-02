from pytube import Playlist, YouTube

cur_url = "https://www.youtube.com/channel/UCrmRhJoIXkaCPJLX_mqnbqQ/videos"

# cur_url = "https://www.youtube.com/watch?v=_06PFsfJbrU"
# YouTube(cur_url).streams.first().download()

# 您可能会注意到列出的某些流同时具有视频编解码器和音频编解码器，而其他流只有视频或音频，这是YouTube支持称为动态自适应HTTP流传输（DASH）的流技术的结果。
yt = YouTube(cur_url)
print("------查看所有可用格式------")
for ii in yt.streams.all():
    print(ii)

# yt.streams.get_by_itag(251).download()

exit()
#
# print("------仅查看这些渐进式下载流-----")
# for ii in yt.streams.filter(progressive=True).all():
#     print(ii)
#
# print("------只查看DASH流（也称为“自适应”）-----")
# for ii in yt.streams.filter(adaptive=True).all():
#     print(ii)

# print("------仅列出音频流-----")
# yt.streams.filter(only_audio=True).all()
# print("------仅列出📛mp4流-----")
# yt.streams.filter(subtype='mp4').all()


print("------下载完整的Youtube播放列表-----")
from pytube import Playlist
pl = Playlist("https://www.youtube.com/playlist?list=PL0eGJygpmOH5xQuy8fpaOvKrenoCsWrKh")
print("视频的总个数: {}".format(len(pl)))
# index = 0
# for video_curl in pl:
#     index += 1
#     if 162 < index and index < 423:
#         print(video_curl)

for u in pl.video_urls[162:423]:
    # YouTube(u).streams.first().download()
    # YouTube(u).streams[1].download()
    YouTube(u).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()



# pl.download_all()
# or if you want to download in a specific directory
# pl.download_all('/path/to/directory/')


