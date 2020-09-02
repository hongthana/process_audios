import os
import glob
import re
import string


illegal_char = string.punctuation + u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:： '
pattern = re.compile('[%s]' % re.escape(illegal_char))


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

tokens_list = []
with open("./vocab_all.txt", "r") as fr:
    for cur_line in fr:
        cur_trans = cur_line.strip()
        for cur_char in cur_trans:
            new_char = pattern.sub(u'', cur_char)
            if is_Chinese(new_char):
                tokens_list.append(new_char)
            else:
                print(new_char)


basedir = "/devdata/home/pishichan/code/asr/data/mandarin/supervised"
# basedir = "/home/psc/Desktop/code/asr/process_audios/supervised/data"

search_path = os.path.join(basedir, '**/**/*' + ".txt")
for fname in glob.iglob(search_path, recursive=True):
    cur_trans_path = os.path.realpath(fname)
    print("cur process trans_file: %s" % cur_trans_path)
    with open(cur_trans_path, "r") as fr:
        for cur_line in fr:
            audio_name, cur_trans = cur_line.strip().split("<--->")
            for cur_char in cur_trans:
                new_char = pattern.sub(u'', cur_char)
                if is_Chinese(new_char):
                    tokens_list.append(new_char)
                else:
                    print(new_char)

tokens_list = list(set(tokens_list))
print("len of tokens = %d " % len(tokens_list))

tkn_file = "tokens.txt"
with open(tkn_file, "w") as ft:
    for token in tokens_list:
        ft.write(token + "\n")

lexicon_file = "lexicon.txt"
with open(lexicon_file, "w") as fl:
    for token in tokens_list:
        fl.write(token + "\t" + token + "\n")