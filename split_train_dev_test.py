import os
import glob
import random


def write_lst_file(cur_list, cur_file_path):
    with open(cur_file_path, "w") as fw:
        for cur_line in cur_list:
            fw.write(cur_line)
    return


basedir = "/home/psc/Desktop/code/asr/process_audios/lists_new1111"
all_lines = []

search_path = os.path.join(basedir, '**/*' + ".lst")
for fname in glob.iglob(search_path, recursive=True):
    cur_trans_path = os.path.realpath(fname)
    print("cur process trans_file: %s" % cur_trans_path)
    with open(cur_trans_path, "r") as fr:
        for cur_line in fr:
            audio_handle, audio_path, audio_len, cur_trans = cur_line.strip().split("\t")

            writeline = []
            writeline.append(audio_handle)
            writeline.append(audio_path)
            writeline.append(audio_len)
            new_trans = ""
            for cur_char in cur_trans:
                new_trans += cur_char + " "
            new_trans = new_trans.strip(" ")
            writeline.append(new_trans)
            new_line = "\t".join(writeline) + "\n"
            all_lines.append(new_line)


random.shuffle(all_lines)
total_len = len(all_lines)
pos1 = int(total_len*0.9)
pos2 = int(total_len*0.95)
print("total_len = %d, pos1 = %d, pos2 = %d " % (total_len, pos1, pos2))
train_lines = all_lines[:pos1]
dev_lines = all_lines[pos1:pos2]
test_lines = all_lines[pos2:]

train_lst_file = os.path.join(basedir, "train.lst")
dev_lst_file = os.path.join(basedir, "dev.lst")
test_lst_file = os.path.join(basedir, "test.lst")

write_lst_file(train_lines, train_lst_file)
write_lst_file(dev_lines, dev_lst_file)
write_lst_file(test_lines, test_lst_file)

