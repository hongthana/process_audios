import os
import glob
import string
import re
import numpy as np
import matplotlib.pyplot as plt
import random

def filterPunctuation(words):
    new_words = []
    illegal_char = string.punctuation + u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:： '
    pattern = re.compile('[%s]' % re.escape(illegal_char))
    for word in words:
        new_word = pattern.sub(u'', word)
        if not new_word == u'':
            new_words.append(new_word)
    return new_words


def filterDigistAlpha(words):
    new_words = []
    illegal_char = string.punctuation + u'1234567890abcdefghigklmnopqrstuvwxyz'
    pattern = re.compile('[%s]' % re.escape(illegal_char))
    for word in words:
        new_word = pattern.sub(u'', word.lower())
        if not new_word == u'':
            new_words.append(new_word)
    return new_words


all_num = 0
discard_num = 0
sent_lens = np.zeros(300, dtype=np.int)
max_sent_len = 0

train_dir = "/devdata/home/jiangda/code/SLU/end-to-end-SLU/Date_700k/audio/70w/train"
# train_dir = "/home/psc/Desktop/code/asr/process_audios/supervised/data/train"
disk_dict = {}
search_path = os.path.join(train_dir, '**/*' + ".wav")
for fname in glob.iglob(search_path, recursive=True):
    audio_path = os.path.realpath(fname)
    audio_name = os.path.basename(audio_path).replace(".wav", "")
    sub_name = os.path.basename(os.path.dirname(audio_path))
    disk_dict[audio_name] = sub_name + "/" + audio_name


src_trans_path = os.path.join(os.path.dirname(train_dir), "trans.txt")
print("cur process txt file: %s " % src_trans_path)
dst_trans_path = "trans_new.txt"  # src_trans_path.replace(".txt", "_new.txt")
with open(dst_trans_path, "w") as fw:
    with open(src_trans_path, "r") as fr:
        for cur_line in fr:
            all_num += 1
            pos = cur_line.strip().find(" ")
            audio_name = cur_line.strip()[:pos]
            cur_trans = cur_line.strip()[pos + 1:]
            # audio_name, cur_trans = cur_line.strip().split(" ")
            cur_trans_new1 = filterPunctuation(cur_trans)        # 过滤标点符号
            cur_trans_new2 = filterDigistAlpha(cur_trans_new1)   # 是否包含数字或者英文
            sent_lens[len(cur_trans_new2)] += 1
            max_sent_len = max(len(cur_trans_new2), max_sent_len)
            if len(cur_trans_new2) != len(cur_trans_new1):
                discard_num += 1
                continue
            # if len(cur_trans_new2) == 10:
            #     print("".join(cur_trans_new2))

            cur_trans_len = len(cur_trans_new2)
            if cur_trans_len >= 10 and cur_trans_len <= 52:
                if audio_name in disk_dict:
                    w_line = disk_dict[audio_name] + "<--->" + "".join(cur_trans_new2)
                    fw.write(w_line + "\n")
                    continue
                else:
                    discard_num += 1
                    print("%s not in disk " % audio_name)
            else:
                discard_num += 1
print("total trans len small than 10 is = %d " % discard_num)
print("total trans len = %d " % all_num)
print(max_sent_len)
print(sent_lens)

# plt.plot(sent_lens[0:53])
# plt.show()

'''
4~52:  211,4920 - 207211
8~52:  211,4920 - 1413196
10~52: 211,4920 - 1671971
'''