import os
import glob
from collections import Counter

basedir = "/devdata/home/pishichan/code/asr/data/mandarin/supervised"
all_lines = []

search_path = os.path.join(basedir, '*/*/' + "trans.txt")
for fname in glob.iglob(search_path, recursive=True):
    cur_trans_path = os.path.realpath(fname)
    cur_dir = os.path.dirname(cur_trans_path)
    print("cur process trans_file: %s" % cur_trans_path)
    save_line_list = []
    rm_cnt = 0
    audio_handle_list = []
    with open(cur_trans_path, "r") as fr:
        for cur_line in fr:
            audio_handle, cur_trans = cur_line.strip().split("<--->")
            audio_handle_list.append(audio_handle)
            audio_path = os.path.join(cur_dir, "wav", audio_handle + ".wav")
            if os.path.exists(audio_path):
                save_line_list.append(cur_line)
            else:
                rm_cnt += 1
                print("cur audio: %s do not exist. " % audio_path)

    print("len(audio_handle_list) = %d " % len(audio_handle_list))
    b = dict(Counter(audio_handle_list))
    print([key for key, value in b.items() if value > 1])  # 只展示重复元素
    audio_handle_list = list(set(audio_handle_list))
    print("len(audio_handle_list) = %d " % len(audio_handle_list))

    if rm_cnt > 0:
        new_file_path = cur_trans_path.replace(".txt", "_new.txt")
        with open(new_file_path, "w") as fw:
            for cur_line in save_line_list:
                fw.write(cur_line)
print("all done!")