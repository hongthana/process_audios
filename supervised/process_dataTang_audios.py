import os
import sox
import glob
import shutil

def read_asr_rst_2_str(src_file):
    asr_rst_list = []
    with open(src_file, 'r') as fr:
        for cur_line in fr:
            audio_name, index_str, cur_trans = cur_line.strip().split("\t")
            new_line = audio_name.replace(".wav", "") + "<--->" + cur_trans
            asr_rst_list.append(new_line)
    if len(asr_rst_list) > 1:
        print("%s trans is more than one line." % src_file)
    return asr_rst_list[0]


# ----------------------------- dataTang 149----------------------------------------
# basedir = '/home/psc/Desktop/code/asr/data/mandarin/supervised/dataTang/149'
#
# for sub_folder in os.listdir(basedir):
#     print("cur process folder: %s " % sub_folder)
#     sub_folder_path = os.path.join(basedir, sub_folder)
#     all_asr_rsts = []
#     all_asr_rsts_file = os.path.join(sub_folder_path, os.path.basename(sub_folder_path) + "_src.txt")
#
#     with open(all_asr_rsts_file, 'wb') as fw:
#         search_path = os.path.join(sub_folder_path, '**/*' + ".wav")
#         for fname in glob.iglob(search_path, recursive=True):
#             audio_path = os.path.realpath(fname)
#             trans_path = audio_path.replace(".wav", ".txt")
#             info_path = audio_path.replace(".wav", ".metadata")
#             if os.path.exists(info_path):
#                 os.remove(info_path)
#             if not os.path.exists(trans_path):
#                 os.remove(audio_path)
#                 continue
#             audio_sr = sox.file_info.sample_rate(audio_path)
#             if int(audio_sr) != 16000:
#                 audio_path_16k = audio_path.replace(".wav", "_16k.wav")
#                 cmd = "ffmpeg -i {} -loglevel 1 -ac 1 -ar 16000 {}".format(audio_path, audio_path_16k)
#                 os.system(cmd)
#                 os.remove(audio_path)
#                 shutil.move(audio_path_16k, audio_path)
#             rst_line = read_asr_rst_2_str(trans_path)
#             fw.write((rst_line + '\n').encode('utf-8'))
#             # os.remove(trans_path)



basedir = '/home/psc/Desktop/code/asr/data/mandarin/supervised/dataTang/149'

search_path = os.path.join(basedir, '**/*' + ".wav")
for fname in glob.iglob(search_path, recursive=True):
    audio_path = os.path.realpath(fname)
    audio_sr = sox.file_info.sample_rate(audio_path)
    if int(audio_sr) != 16000:
        audio_path_16k = audio_path.replace(".wav", "_16k.wav")
        # cmd = "ffmpeg -i {} -loglevel 1 -ac 1 -ar 16000 {}".format(audio_path, audio_path_16k)
        cmd = "sox -v 0.99 {} -r 16000 -c 1 {}".format(audio_path, audio_path_16k)
        os.system(cmd)
        os.remove(audio_path)
        shutil.move(audio_path_16k, audio_path)