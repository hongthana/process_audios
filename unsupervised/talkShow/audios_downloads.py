from pytube import Playlist, YouTube
from pytube import Playlist

# 周周侃
curl_dicts = {"周周侃": "https://www.youtube.com/playlist?list=PLDBKCF_fpgH6OwEYL-TMwUs1oDb0LtiIH",
              "侃盲点": "https://www.youtube.com/playlist?list=PLDBKCF_fpgH46jFCSnIsPyP-iTxGFF9PV",   # 不更新
              "侃观点": "https://www.youtube.com/playlist?list=PLDBKCF_fpgH7r3qDdRRG8fZ7NZJVWc3rG",   # 不更新
}


# 徐杰慢半拍
# curl_dicts = {"晚间直播": "https://www.youtube.com/playlist?list=PLoB7UEKXBdawrWATv3kj1ntyD8u2M-nI7",
#               "花絮": "https://www.youtube.com/playlist?list=PLoB7UEKXBdazgpi8jV8KBvtf8FaHvbPn9",
#                 "周末嘉宾漫谈": "https://www.youtube.com/playlist?list=PLoB7UEKXBdayFpKLAmO4XlCyqWz-BJVR9",
#                 "海外杂音": "https://www.youtube.com/playlist?list=PLoB7UEKXBdawpsVcT9bq65v4l6KJT8T_d",
#                 "闲聊台湾": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaxOzOlpcwHpsNsTkZbCW-Co",
#                 "各国抗疫百态": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaxqn3uLwmM56UI1N19qPfXV",
#                 "中国现状系列": "https://www.youtube.com/playlist?list=PLoB7UEKXBdawENilnPnBbjxkxmB4lcsxI",
#                 "墙内生存指南": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaztPd-f3y4dm9nBxsHKCCpD",
#                 "嘉宾对话": "https://www.youtube.com/playlist?list=PLoB7UEKXBday3iKvl0JXrnmuTVWXBJnJi",
#                 "中共维持对中国统治的三个前提": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaz7WjsAJUJTN1DSFCIvG_6R",
#                 "中国变革的经济基础已经显现": "https://www.youtube.com/playlist?list=PLoB7UEKXBdazLrdNtzXfp9HNkxtt4hExm",
#                 "戛然而止的青涩": "https://www.youtube.com/playlist?list=PLoB7UEKXBdawJcxNx46pDiNVU78WqB26n",
#                 "目前中国社会的乱象": "https://www.youtube.com/playlist?list=PLoB7UEKXBdazEeFfLfY27kTTLaVFOylpW",
#                 "内地杂音": "https://www.youtube.com/playlist?list=PLoB7UEKXBdawIqk-Nw3PoAv8dUeOPlt9m",
#                 "自救措施": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaxw3qfG66Q0MS02dWgM8hpl",
#                 "人民币系列": "https://www.youtube.com/playlist?list=PLoB7UEKXBdawOjK1R9tH3xyCe8Jh5Ei22",
#                 "第一阶段协议": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaz4xh1PvGB3WcuCPTaGx0vP",
#                 "闲聊台湾": "https://www.youtube.com/playlist?list=PLoB7UEKXBdayT3smImG9_xwrH8Jr-VkZm",
#                 "华为": "https://www.youtube.com/playlist?list=PLoB7UEKXBdawv3uam-HhrTfsZkpSe6QHZ",
#                 "内地乱象": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaw6lbkL6BY6neVtlLZU8LOk",
#                 "周末直播": "https://www.youtube.com/playlist?list=PLoB7UEKXBdazG05zDNpy7-jer08kE4wjm",
#                 "思路决定出路": "https://www.youtube.com/playlist?list=PLoB7UEKXBdayNsLR_3KmRL6kU-zRS_Chr",
#                 "祥瑞": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaxZqnrMMSVcXH3-bh6X0FYE",
#                 "踏出国门": "https://www.youtube.com/playlist?list=PLoB7UEKXBdaxx-T9oUX3fn4w64QMqj0Nu",
# }

# 奇葩说
# curl_dicts = {"第四季": "https://www.youtube.com/playlist?list=PL22oDPAz6y-GxOa2_jS4CgV2k1fI1bANj",
#               "第五季": "https://www.youtube.com/playlist?list=PLN2WpaYD6flMlEVgR4PzN3zZnmgdfzgM6",
#               "第六季": "https://www.youtube.com/playlist?list=PLXWf3ewMEIhCc1qH2W4f9Zz3roPW1plwh",
# }

# 明镜
# curl_dicts = {"明镜火拍": "https://www.youtube.com/playlist?list=PL7rBJWuEBrPZDH9wTO4beNnFzqSVCmw20",
#               "明镜电视": "https://www.youtube.com/playlist?list=PLiPkp_d_RCymvSOV25ONraundA2P_0FJa"
#               }

# # gwg
# curl_dicts = {"gwg_youtube": "https://www.youtube.com/playlist?list=PLpq6bGgCev7d5DtGTfrc_CT9PZ2_URcoY"}

for item_name, paylist_url in curl_dicts.items():
    print(item_name, "--->", paylist_url)
    print("------下载完整的Youtube播放列表-----")
    pl = Playlist(paylist_url)
    print("视频的总个数: {}".format(len(pl)))
    for cur_url in pl.video_urls:
        try:
            # YouTube(cur_url).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()   # 下载分辨率最高的视频
            YouTube(cur_url).streams.filter(type='audio', file_extension='webm').order_by('abr').desc().first().download()     # 下载webm音频
        except:
            print("{} downloads failed".format(cur_url))
            continue


