# -*- coding: utf-8 -*-

from pypinyin import pinyin, lazy_pinyin, Style
import sentencepiece as spm


print("Creating word -> word pieces lexicon...\n", flush=True)
model_file = "/home/psc/Desktop/code/asr/process_audios/data/test1/model/zh-train-all-unigram-397.model"
sp = spm.SentencePieceProcessor()
sp.Load(model_file)


# lexicon_file = "lexicon.txt"
# pinyin_list = []
# with open(lexicon_file, "r") as fr:
#     for line in fr:
#         cur_zh = line.strip().split("\t")[0]
#         cur_pinyins = pinyin(cur_zh, style=Style.TONE3, heteronym=True)
#         for cur_char in cur_pinyins:
#             cur_pinyin = cur_char[0].replace("1", "").replace("2", "").replace("3", "").replace("4", "")
#             pinyin_list.append(cur_pinyin)
# pinyin_list = list(set(pinyin_list))
# print("len(pinyin_list) = %d " % len(pinyin_list))
#
#
# lexicon_wrd_file = "lexicon_wrdpiece.txt"
# pinyin_list_before = []
# with open(lexicon_wrd_file, "r") as fr:
#     for line in fr:
#         cur_wrd = line.strip().split("\t")[0]
#         if cur_wrd not in pinyin_list_before:
#             pinyin_list_before.append(cur_wrd)
#
# pinyin_list_before = list(set(pinyin_list_before))
# print("len(pinyin_list_before) = %d " % len(pinyin_list_before))
# print("----------------------------------------------------")
# for cur_py in pinyin_list_before:
#     if cur_py not in pinyin_list:
#         print(cur_py)
# print("----------------------------------------------------")


lexicon_file = "lexicon.txt"
lexicon_new = "lexicon_new.txt"
with open(lexicon_new, "w") as f_lexicon:
    with open(lexicon_file, "r") as fr:
        for line in fr:
            cur_zh = line.strip().split("\t")[0]
            cur_pinyins = pinyin(cur_zh, style=Style.TONE3, heteronym=True)
            cur_list = []
            for cur_char in cur_pinyins[0]:
                cur_pinyin = cur_char.replace("1", "").replace("2", "").replace("3", "").replace("4", "")
                if cur_pinyin not in cur_list:
                    cur_list.append(cur_pinyin)
                    wps = sp.NBestEncodeAsPieces(cur_pinyin, 10)
                    for wp in wps:  # the order matters for our training
                        f_lexicon.write(
                            cur_zh
                            + "\t"
                            + " ".join([w.replace("\u2581", "_") for w in wp])
                            + "\n")