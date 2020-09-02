# -*- coding: UTF-8 -*-
import sox
import os


ext = "wav"

audio_len_all = 0
audios_num = 0

gg = os.walk(r"/home/psc/Desktop/code/asr/data/mandarin/unsupervised/govern")
for path, dir_list, file_list in gg:
    for file_name in file_list:
        cur_audio_path = os.path.join(path, file_name)
        if not cur_audio_path.endswith(ext):
            continue
        try:
            audio_len = sox.file_info.duration(cur_audio_path)
        except:
            continue
        audio_len_all += audio_len
        audios_num += 1

print("audios_num = {}".format(audios_num))
print("audio_len_all = {}".format(audio_len_all))

# basedir = "/home/psc/Desktop/code/asr/process_audios/lists_new1111"
# rst_dict = {}
# search_path = os.path.join(basedir, '**/*' + ".lst")
# for fname in glob.iglob(search_path, recursive=True):
#     cur_trans_path = os.path.realpath(fname)
#     print("cur process trans_file: %s" % cur_trans_path)
#     with open(cur_trans_path, "r") as fr:
#         for cur_line in fr:
#             audio_handle, audio_path, audio_len, cur_trans = cur_line.strip().split("\t")
#             if audio_handle not in rst_dict:
#                 rst_dict[audio_handle] = float(audio_len)
#             else:
#                 rst_dict[audio_handle] += float(audio_len)
#
# read_subpaths = ["guijitts-wav", "prime-wav", "ST-wav", "aishell1-wav", "commonVoice-wav"]
# speak_subpaths = ["dataTang-wav", "guiji-wav", "htrs-wav", "guiji_70w-wav"]
#
# total_read_hours = 0
# total_speak_hours = 0
# total_hours = 0
# for k, v in rst_dict.items():
#     v = v / 3600.0
#     print(k, v)
#     total_hours += v
#     if k in read_subpaths:
#         total_read_hours += v
#     elif k in speak_subpaths:
#         total_speak_hours += v
#
# print("total_read_hours = %f " % total_read_hours)
# print("total_speak_hours = %f " % total_speak_hours)
# print("total_hours = %f " % total_hours)

'''
guijitts-wav 11.558074990833282
aishell1-wav 178.84521354555298
htrs-wav 8.925449097222222
guiji-wav 6.796116666666692
guiji_70w-wav 519.4475525347228
commonVoice-wav 26.19660666666676
dataTang-wav 178.7171682291641
prime-wav 98.94977777777676
ST-wav 109.58289111111047

total_read_hours = 425.132564 
total_speak_hours = 713.886287 
total_hours = 1139.018851 
'''


