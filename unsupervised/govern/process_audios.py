# -*- coding: UTF-8 -*-
import sox
import os
import glob
import shutil


def check_audio_len_and_16k(folder_in):
    for wav_id in os.listdir(folder_in):
        cur_audio_path = os.path.join(folder_in, wav_id)
        audio_len = sox.file_info.duration(cur_audio_path)
        if audio_len > 0.9:
            continue
        else:
            os.remove(cur_audio_path)



# base_dir = "/home/psc/Desktop/code/asr/data/mandarin/unsupervised/govern/中基协录音"
# for cur_sub in os.listdir(base_dir):
#     sub_path = os.path.join(base_dir, cur_sub)
#     if os.path.isdir(sub_path):
#         for cur_file in os.listdir(sub_path):
#             cur_file_path = os.path.join(sub_path, cur_file)
#             if os.path.exists(cur_file_path) and cur_file_path.endswith("wav"):
#                 print("this is a audio, ", cur_file_path)
#                 # os.system("mv %s ../" % cur_file_path)


# base_dir = "/home/psc/Desktop/code/asr/data/mandarin/unsupervised/govern/中基协录音"
# for cur_sub in os.listdir(base_dir):
#     sub_path = os.path.join(base_dir, cur_sub)
#     if os.path.isdir(sub_path):
#         check_audio_len_and_16k(sub_path)


# base_dir = "/home/psc/Desktop/code/asr/data/mandarin/unsupervised/govern/雨花政务/20190415"
#
# for cur_sub in os.listdir(base_dir):
#     sub_path = os.path.join(base_dir, cur_sub)
#     if os.path.isdir(sub_path):
#         sub_dir_path = os.path.join(sub_path, "通话录音")
#         for cur_file in os.listdir(sub_dir_path):
#             cur_file_path = os.path.join(sub_dir_path, cur_file)
#             if os.path.exists(cur_file_path) and cur_file_path.endswith("WAV"):
#                 print("this is a audio, ", cur_file_path)
#                 os.system("mv %s %s" % (cur_file_path, os.path.join(base_dir, cur_sub + "_" + cur_file.lower())))


ext = "wav"
g = os.walk(r"/home/psc/Desktop/code/asr/data/录音数据/useful/中基协录音")
dst_dir = "/home/psc/Desktop/code/asr/data/录音数据/useful/中基协录音_new"

for path, dir_list, file_list in g:
    for file_name in file_list:
        cur_audio_path = os.path.join(path, file_name)
        if not cur_audio_path.endswith(ext):
            continue
        wav_name = os.path.basename(cur_audio_path).replace(".wav", "")
        try:
            name_data = wav_name.split("_")[1]
        except:
            print(wav_name)
            continue
        cur_dir = ""
        if "201901" in name_data:
            cur_dir = os.path.join(dst_dir, "201901")
        elif "201902" in name_data:
            cur_dir = os.path.join(dst_dir, "201902")
        elif "201903" in name_data:
            cur_dir = os.path.join(dst_dir, "201903")
        else:
            print(name_data)
        sub_dir = os.path.join(cur_dir, name_data[-2:])
        os.makedirs(sub_dir, exist_ok=True)
        new_path = os.path.join(sub_dir, wav_name + ".wav")
        os.system("mv %s %s" % (cur_audio_path, new_path))

