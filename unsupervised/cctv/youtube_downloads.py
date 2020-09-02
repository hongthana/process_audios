import os
from pytube import Playlist, YouTube
from pytube import Playlist


# cur_url = "https://www.youtube.com/playlist?list=PLBEB-HAHNzdMZihe_JUroUGIds4TUMSP5"   # 今日说法订阅号的youtube首页--2019
# cur_url = "https://www.youtube.com/playlist?list=PLBEB-HAHNzdO1czhGAPqNukXJbdCHIzw5"     # 今日说法订阅号的youtube首页--2020
# cur_url = "https://www.youtube.com/playlist?list=PL0eGJygpmOH5xQuy8fpaOvKrenoCsWrKh"   # 新闻联播youtube播放列表地址
# cur_url = "https://www.youtube.com/playlist?list=PL0eGJygpmOH6SOH7RK3BexJFWkHTxbmZi"     # 焦点访谈
# cur_url = "https://www.youtube.com/playlist?list=PL0eGJygpmOH5whCTrU1_pvvq5husjnkqD"     # 面对面
# cur_url = "https://www.youtube.com/playlist?list=PL0eGJygpmOH7QNF2BJma-9PZ9-NUqvU6M"      # 等着我
# cur_url = "https://www.youtube.com/playlist?list=PL0eGJygpmOH7cjGN3ECIboq-6W2rCPWJM"      # 百家讲坛
cur_url = "https://www.youtube.com/playlist?list=PL0eGJygpmOH5NxGol_P_kTE_hvmzy7IoZ"     # 生活提示

print("------下载完整的Youtube播放列表-----")
pl = Playlist(cur_url)
print("视频的总个数: {}".format(len(pl)))

# print(pl.video_urls[316])
# exit()

# cur_url1 = "https://www.youtube.com/watch?v=Y2loSK9iS-s"
# YouTube(cur_url1).streams.filter(type='audio', file_extension='webm').order_by('abr').desc().first().download()

for cur_url in pl.video_urls[316:]:
    try:

        # YouTube(cur_url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()   # 下载分辨率最高的视频
        YouTube(cur_url).streams.filter(type='audio', file_extension='webm').order_by('abr').desc().first().download()     # 下载webm音频

    except:
        print("{} downloads failed".format(cur_url))
        continue


