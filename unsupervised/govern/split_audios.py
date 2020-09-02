# -*- coding: UTF-8 -*-
import sox
import os
import shutil


def check_audio_len_and_16k(folder_in):
    for wav_id in os.listdir(folder_in):
        cur_audio_path = os.path.join(folder_in, wav_id)
        audio_len = sox.file_info.duration(cur_audio_path)
        if audio_len > 5 and audio_len < 30.1:
            continue
        else:
            os.remove(cur_audio_path)


cur_ext = ".wav"

# src_path = "/home/psc/Desktop/code/asr/data/wav2vec_src/govern/雨花政务/20190415"
# dst_path = "/home/psc/Desktop/code/asr/data/mandarin/unsupervised/govern/雨花政务20190415"
src_path = "/home/psc/Desktop/code/asr/data/wav2vec_src/govern/中基协录音/201901"
dst_path = "/home/psc/Desktop/code/asr/data/mandarin/unsupervised/govern/中基协录音201901"
# 音频采样率是8k的, 有的音频的长度在1秒以下
for cur_file in os.listdir(src_path):
    cur_audio_file = os.path.join(src_path, cur_file)
    audio_save_path = os.path.join(dst_path, cur_file)
    try:
        audio_len = sox.file_info.duration(cur_audio_file)
    except:
        print("{} open failed".format(cur_audio_file))
        continue
    if audio_len < 5:
        print("length of %s is too short!" % cur_audio_file)
        continue
    else:
        audio_sr = sox.file_info.sample_rate(cur_audio_file)
        if int(audio_sr) != 16000:
            cmd = "ffmpeg -i {} -hide_banner -loglevel 0 -ac 1 -ar 16000 {}".format(cur_audio_file, audio_save_path)
            os.system(cmd)

            cur_split_dir = os.path.join(dst_path, cur_file.replace(".wav", ""))
            os.makedirs(cur_split_dir, exist_ok=True)
            os.system("python3 ../../audiosplit.py --target_dir {} --output_dir {}".format(audio_save_path, cur_split_dir))
            os.remove(audio_save_path)
            os.system("python3 ../../audiosplit.py --target_dir {} --output_dir {}".format(cur_split_dir, cur_split_dir))

            check_audio_len_and_16k(cur_split_dir)


new_dst_path = dst_path + "_new"
os.makedirs(new_dst_path, exist_ok=True)
for cur_folder in os.listdir(dst_path):
    cur_folder_path = os.path.join(dst_path, cur_folder)
    for cur_file in os.listdir(cur_folder_path):
        cur_audio_path = os.path.join(cur_folder_path, cur_file)
        cur_audio_path_new = os.path.join(new_dst_path, cur_file)
        shutil.move(cur_audio_path, cur_audio_path_new)


