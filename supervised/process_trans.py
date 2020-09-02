import os
import glob
import string
import re
import numpy as np
import matplotlib.pyplot as plt
import random

def filterPunctuation(words):
    new_words = []
    illegal_char = string.punctuation + u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:：· '
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


basedir = '/home/psc/Desktop/code/asr/data/mandarin/txts/speak'

all_num = 0
discard_num = 0
sent_lens = np.zeros(300, dtype=np.int)
max_sent_len = 0
search_path = os.path.join(basedir, '**/etc/' + "prompts-original-src")
for fname in glob.iglob(search_path, recursive=True):
    src_trans_path = os.path.realpath(fname)
    print("cur process txt file: %s " % src_trans_path)
    dst_trans_path = src_trans_path.replace("etc/prompts-original-src", "trans.txt")
    with open(dst_trans_path, "w") as fw:
        with open(src_trans_path, "r") as fr:
            for cur_line in fr:
                all_num += 1
                pos = cur_line.strip().find(" ")
                audio_name = cur_line.strip()[:pos]
                cur_trans = cur_line.strip()[pos+1:]
                # audio_name, cur_trans = cur_line.strip().split("<--->")
                cur_trans_new1 = filterPunctuation(cur_trans)   # 过滤标点符号
                cur_trans_new2 = filterDigistAlpha(cur_trans_new1)   # 是否包含数字或者英文
                sent_lens[len(cur_trans_new2)] += 1
                max_sent_len = max(len(cur_trans_new2), max_sent_len)
                if len(cur_trans_new2) != len(cur_trans_new1):
                    print(cur_trans_new1)
                    print("".join(cur_trans_new2))
                    print("---------------------")
                # if len(cur_trans_new2) == 1:
                #     print("".join(cur_trans_new2))    # 啊, 嗯， 对，唉，
                # if len(cur_trans_new2) == 2:
                #     print("".join(cur_trans_new2))     # 不要， 哪位，嗯嗯，唉说，没有
                # if len(cur_trans_new2) == 3:
                #     print("".join(cur_trans_new2))      # 哪里啊  嗯对的  唉你好  零零零

                cur_trans_len = len(cur_trans_new2)
                if cur_trans_len >= 4 and cur_trans_len <= 52:
                    w_line = audio_name + "<--->" + "".join(cur_trans_new2)
                    fw.write(w_line + "\n")
                    continue
                elif cur_trans_len == 3:
                    if random.random() > 0.5:
                        # print("".join(cur_trans_new2))
                        w_line = audio_name + "<--->" + "".join(cur_trans_new2)
                        fw.write(w_line + "\n")
                        continue
                    else:
                        discard_num += 1
                else:
                    discard_num += 1
    os.system("rm -rf %s" % os.path.dirname(src_trans_path))
print("total trans len small than 10 is = %d " % discard_num)     # 丢弃率约为16%, 与read文件夹差不多
print("total trans len = %d " % all_num)
print(max_sent_len)
print(sent_lens)

plt.plot(sent_lens[0:53])
plt.show()

