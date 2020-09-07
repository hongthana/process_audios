import os
import glob
import random


def read_trans(src_file):
    asr_rst_list = []
    with open(src_file, 'r') as fr:
        for cur_line in fr:
            asr_rst_list.append(cur_line.strip())
    return asr_rst_list


def write_trans(dataset_name, src_list, write_file_path):
    with open(write_file_path, 'a+') as fw:
        for cur_line in src_list:
            new_line = os.path.join(dataset_name, "wav", cur_line)
            fw.write(new_line + "\n")
    return


def appand_tsv():
    src_file = "/home/psc/Desktop/code/asr/fairseq/examples/wav2vec/output/zh/wav2vec/supervised/train.tsv"
    src_dict = {}
    with open(src_file, "r") as tsv_fr:
        root = next(tsv_fr).strip()
        for line in tsv_fr:
            wav_name, wav_len = line.strip().split("\t")
            src_dict[wav_name] = wav_len

    add_file = "/home/psc/Desktop/code/asr/fairseq/examples/wav2vec/output/zh/wav2vec/unsupersived/train.tsv"
    add_dict = {}
    with open(add_file, "r") as tsv_f:
        root = next(tsv_f).strip()
        for line in tsv_f:
            wav_name, wav_len = line.strip().split("\t")
            add_dict["unsupersived/" + wav_name] = wav_len

    dictMerged = src_dict.copy()
    dictMerged.update(add_dict)

    keys = list(dictMerged.keys())
    random.shuffle(keys)

    dst_tsv = "train.tsv"
    dataset_path = "/devdata/home/pishichan/code/asr/data/mandarin/"
    with open(dst_tsv, 'w') as tsv_fw:
        print(dataset_path, file=tsv_fw)

        for audio_name, frames in dictMerged.items():
            print('{}\t{}'.format(audio_name, frames), file=tsv_fw)


appand_tsv()
exit()


basedir = '/devdata/home/pishichan/code/asr/data/mandarin/'
# basedir = "/home/psc/Desktop/code/asr/data/mandarin/"
dict_all = {}
wav_cnt = 0
search_path = os.path.join(basedir, '*/*/*/' + "trans.txt")
for fname in glob.iglob(search_path, recursive=True):
    trans_path = os.path.realpath(fname)
    dataset_name = trans_path.replace(basedir, "").replace("/trans.txt", "")
    dict_all[dataset_name] = read_trans(trans_path)
    print("len(%s) = %d " % (dataset_name, len(dict_all[dataset_name])))
    wav_cnt += len(dict_all[dataset_name])
print("wav_cnt = %d " % wav_cnt)

rate = 0.5
new_dict_all = {}
new_wav_cnt = 0
for dataset_name, dataset_list in dict_all.items():
    cur_len = round(rate * len(dataset_list))
    random.shuffle(dataset_list)
    new_dataset_list = dataset_list[:cur_len]
    new_dict_all[dataset_name] = new_dataset_list
    new_wav_cnt += len(new_dataset_list)
print("new_wav_cnt = %d " % new_wav_cnt)

train_file = "train.txt"
dev_file = "dev.txt"
test_file = "test.txt"

train_rate = 0.9
dev_rate = 0.98
for dataset_name, dataset_list in new_dict_all.items():
    cur_num = len(dataset_list)
    cur_train = dataset_list[:round(cur_num*train_rate)]
    cur_dev = dataset_list[round(cur_num * train_rate):round(cur_num * dev_rate)]
    cur_test = dataset_list[round(cur_num * dev_rate):]
    print("len(%s) = %d " % (dataset_name, cur_num))
    write_trans(dataset_name, cur_train, train_file)
    write_trans(dataset_name, cur_dev, dev_file)
    write_trans(dataset_name, cur_test, test_file)

