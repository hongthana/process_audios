import os
import sox
import glob
import csv
import shutil

# -----------------------处理tsv文件------------------------
# infile = '/home/psc/Desktop/code/asr/data/mandarin/supervised/commonVoice/validated.tsv'
# base_dir = os.path.dirname(infile)
# clips_dir = os.path.join(base_dir, "clips")
# audio_dir = os.path.join(base_dir, "audios")
# os.makedirs(audio_dir, exist_ok=True)
#
# audio_trans_path = infile.replace(".tsv", ".txt")
# with open(audio_trans_path, "w") as fw:
#     with open(infile, encoding='utf-8', newline='') as fr:
#             reader = csv.reader(fr, delimiter='\t')
#             # 返回一个列表的迭代，每一行都是一个列表
#             for row in reader:
#                 # print(row)
#                 audio_name = row[1]
#                 audio_path = os.path.join(clips_dir, audio_name)
#                 if os.path.exists(audio_path):
#                     audio_path_new = os.path.join(audio_dir, audio_name)
#                     shutil.move(audio_path, audio_path_new)
#                     new_line = audio_name.replace(".mp3", "") + "<--->" + row[2]
#                     fw.write(new_line + "\n")


# --------------------mp3_2_wav-------------------------------
basedir = '/home/psc/Desktop/code/asr/data/mandarin/supervised/commonVoice/audios'

search_path = os.path.join(basedir, '*' + ".mp3")
for fname in glob.iglob(search_path, recursive=True):
    audio_path = os.path.realpath(fname)
    # audio_sr = sox.file_info.sample_rate(audio_path)
    # if int(audio_sr) != 16000:
    audio_path_16k = audio_path.replace(".mp3", "_16k.wav")
    cmd = "ffmpeg -i {} -loglevel 1 -ac 1 -ar 16000 {}".format(audio_path, audio_path_16k)
    os.system(cmd)
    os.remove(audio_path)
    shutil.move(audio_path_16k, audio_path.replace(".mp3", ".wav"))


