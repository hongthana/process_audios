import os
import sox


# ----------------------------- aishell v1 ----------------------------------------
# basedir = '/home/psc/Desktop/code/asr/data/aishell_v1'
# srcdir = os.path.join(basedir, 'data_aishell/wav')
# dstdir = os.path.join(basedir,  'wav2vec_data')
# os.makedirs(dstdir, exist_ok=True)
#
# use_cnt = 0
# for sub_folder in os.listdir(srcdir):
#     sub_folder_path = os.path.join(srcdir, sub_folder)
#     for speaker_id in os.listdir(sub_folder_path):
#         speaker_folder_path = os.path.join(sub_folder_path, speaker_id)
#         for wav_id in os.listdir(speaker_folder_path):
#             if wav_id.lower().endswith("wav"):
#                 cur_audio_path = os.path.join(speaker_folder_path, wav_id)
#                 audio_len = sox.file_info.duration(cur_audio_path)
#                 if audio_len > 9.9 and audio_len < 30.1:
#                     dst_audio_path = os.path.join(dstdir, speaker_id + "_" + wav_id)
#                     os.system("cp %s %s" % (cur_audio_path, dst_audio_path))
#                     use_cnt += 1
# print('total useful cnt = %d ' % use_cnt)



# ----------------------------- aishell v2 ----------------------------------------
srcdir = '/devdata/home/pishichan/code/asr/data/aishell_v2/data/wav'
dstdir = '/devdata/home/pishichan/code/asr/data/aishell_v2/data/wav_choose'
os.makedirs(dstdir, exist_ok=True)
use_cnt = 0

for speaker_id in os.listdir(srcdir):
    speaker_folder_path = os.path.join(srcdir, speaker_id)
    for wav_id in os.listdir(speaker_folder_path):
        if wav_id.lower().endswith("wav"):
            cur_audio_path = os.path.join(speaker_folder_path, wav_id)
            audio_len = sox.file_info.duration(cur_audio_path)
            if audio_len > 9.9 and audio_len < 30.1:
                use_cnt += 1
                dst_audio_path = os.path.join(dstdir, wav_id)
                os.system("cp %s %s " % (cur_audio_path, dst_audio_path))
print('total useful cnt = %d ' %use_cnt)