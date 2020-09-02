# -*- coding: utf-8 -*-
import os
from pypinyin import pinyin, lazy_pinyin, Style

dict_file = "dict.txt"
word_list = []
word_py_dict = {}
token_list = []
with open(dict_file, "r") as fr:
    for line in fr:
        cur_py, words = line.strip().split('\t')
        token_list.append(cur_py)
        for e_wrd in words:
            word_list.append(e_wrd)
            word_py_dict[e_wrd] = cur_py
word_list = list(set(word_list))
print("len(word_list) = %d " % len(word_list))

lexicon_file = "lexicon.txt"
lexicon_list = []
with open(lexicon_file, "r") as fr:
    for line in fr:
        cur_wrd, wrd = line.strip().split('\t')
        lexicon_list.append(cur_wrd)
lexicon_list = list(set(lexicon_list))
print("len(lexicon_list) = %d " % len(lexicon_list))
token_list = list(set(token_list))
print("len(token_list) = %d " % len(token_list))

for cur_wrd in lexicon_list:
    if cur_wrd not in word_list:
        word_list.append(cur_wrd)
        # print(cur_wrd)
        cur_pinyins = pinyin(cur_wrd, style=Style.TONE3, heteronym=True)
        for cur_char in cur_pinyins[0]:
            word_py_dict[cur_wrd] = cur_char
            token_list.append(cur_char)
word_list = list(set(word_list))
print("len(word_list) = %d " % len(word_list))

word_py_list = sorted(word_py_dict.items(), key=lambda item: item[1])   # dict sorted by value
print("len(word_py_list) = %d " % len(word_py_list))
lexicon_file_new = "lexicon_new.txt"
if os.path.exists(lexicon_file_new):
    os.remove(lexicon_file_new)
with open(lexicon_file_new, "w") as fw:
    for cur_item in word_py_list:
        w_line = cur_item[0] + "\t" + cur_item[1] + "\n"
        fw.write(w_line)

token_file = "tokens.txt"
token_list = list(set(token_list))
print("len(token_list) = %d " % len(token_list))
with open(token_file, "w") as fw:
    for cur_item in token_list:
        fw.write(cur_item + "\n")