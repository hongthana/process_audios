import os
import glob
import re
import string


illegal_char = string.punctuation + u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:：・·「」『』〈〉／－□䴕 '
pattern = re.compile('[%s]' % re.escape(illegal_char))


def sentence_is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            continue
        else:
            return False
    return True


basedir = "/home/psc/Desktop/code/asr/process_audios/lists"
save_dir = basedir + "_new"
os.makedirs(save_dir, exist_ok=True)
tokens_list = []

search_path = os.path.join(basedir, '**/*' + ".lst")
for fname in glob.iglob(search_path, recursive=True):
    cur_trans_path = os.path.realpath(fname)
    print("cur process trans_file: %s" % cur_trans_path)
    dst_trans_path = os.path.join(save_dir, os.path.basename(cur_trans_path))
    with open(dst_trans_path, "w") as fw:
        with open(cur_trans_path, "r") as fr:
            for cur_line in fr:
                audio_handle, audio_path, audio_len, cur_trans = cur_line.strip().split("\t")
                if sentence_is_Chinese(cur_trans):
                    for cur_char in cur_trans:
                        tokens_list.append(cur_char)
                    fw.write(cur_line)
                else:
                    print(cur_line, " contains illegal_char")
                    new_trans = pattern.sub(u'', cur_trans)
                    if sentence_is_Chinese(new_trans):
                        for cur_char in new_trans:
                            tokens_list.append(cur_char)
                        writeline = []
                        writeline.append(audio_handle)
                        writeline.append(audio_path)
                        writeline.append(audio_len)
                        writeline.append(new_trans)
                        fw.write("\t".join(writeline) + "\n")
                    else:
                        print(cur_line, " is not a chinese char!")

tokens_list = list(set(tokens_list))
print("len of tokens_list = %d " % len(tokens_list))

tokens_src = []
with open("am/tokens.txt", "r") as fr:
    for cur_line in fr:
        tokens_src.append(cur_line.strip())
tokens_src = list(set(tokens_src))
print("len of tokens_src = %d " % len(tokens_src))

for cur_tk in tokens_list:
    if cur_tk not in tokens_src:
        print(cur_tk, " is in tokens_src, but not in tokens_list")
