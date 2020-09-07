# -*- coding: UTF-8 -*-

import numpy as np


audio_len_all = 0.0
audios_num = 0
wav_lens = np.zeros(60, dtype=np.int)
max_len = 0.0
min_len = 100.0
# tsv_file = "/home/psc/Desktop/code/asr/fairseq/examples/wav2vec/output/zh/wav2vec/gpu/train.tsv"
tsv_file = "/home/psc/Desktop/code/asr/fairseq/examples/wav2vec/output/zh/wav2vec/mix/train.tsv"
with open(tsv_file, "r") as tsv_fr:
    root = next(tsv_fr).strip()
    for line in tsv_fr:
        wav_name, wav_len = line.strip().split("\t")
        cur_len = float(wav_len) / 16000.0      # second
        audio_len_all += cur_len
        audios_num += 1
        max_len = max(cur_len, max_len)
        min_len = min(cur_len, min_len)
        block_len = int(cur_len / 1)   # 向下取整
        wav_lens[block_len] += 1

print("wav_lens = ", wav_lens)
print("max_len = {}".format(max_len))
print("min_len = {}".format(min_len))
print("audios_num = {}".format(audios_num))
print("total_audio_hours = {}".format(audio_len_all/60.0/60.0))
print("avg_audio_len = {}".format(audio_len_all/audios_num))


