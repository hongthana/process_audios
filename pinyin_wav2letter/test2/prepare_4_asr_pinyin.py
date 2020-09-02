# -*- coding: utf-8 -*-

import os
import re
import string
import string
from pypinyin import pinyin, lazy_pinyin, Style
from collections import defaultdict


all_flag = string.punctuation + u'“《》「」』『·—□〈〉•’●‘×”・∫,?!.'
pattern_flag = re.compile('[%s]' % re.escape(all_flag))
alpha_char = u'gǚmḿàpádōúùiūǎjcfrbuyatèzāīkǜǘexshónlǒwoǐéìüòqíǔēńě 桛瓼嗧甅瓧瓱鿞烪龹瓰龼兙兡鿠龺'
pattern_alpha = re.compile('[%s]' % re.escape(alpha_char))

trantab = str.maketrans('，。！？【】（）％＃＠＆１２３４５６７８９０、', ',.!?[]()%#@&1234567890,')


def write_token_lexicon():
    tokens_file = "/home/psc/Desktop/code/asr/process_audios/data/test2/data/am/tokens.txt"
    all_wrd_list = []
    with open(tokens_file, "r") as fr:
        for line in fr:
            cur_word = line.strip()
            all_wrd_list.append(cur_word)
    all_wrd_list = list(set(all_wrd_list))
    print("len(all_wrd_list) = %d " % len(all_wrd_list))

    lexicon_file = os.path.join(os.path.dirname(tokens_file), "lexicon_new.txt")
    with open(lexicon_file, "w") as fw:
        for cur_wrd in all_wrd_list:
            cur_pinyins = pinyin(cur_wrd, heteronym=True)
            for cur_py in cur_pinyins:
                fw.write(cur_wrd)
                fw.write("\t")
                lls = ""
                for ll in cur_py[0]:
                    lls += ll + " "
                fw.write(lls[:-1])
                fw.write(" |\n")
    print("lexicon done ")


def get_tokens():
    # word_dict = defaultdict(set)
    base_dir = "/home/psc/Desktop/data/nlp/pinyin_tone"
    for sub_name in os.listdir(base_dir):
        print("cur sub_dir: ", sub_name)
        sub_dir = os.path.join(base_dir, sub_name)
        for cur_file in os.listdir(sub_dir):
            word_dict = defaultdict(set)
            cur_file_path = os.path.join(sub_dir, cur_file)
            # print("cur file: ", cur_file)
            with open(cur_file_path, "r") as fr:
                for line in fr:
                    str_1 = pattern_flag.sub(u'', line.strip().replace("  ", " "))
                    str_2 = pattern_alpha.sub(u'', str_1)
                    if len(str_2) > 0:
                        print(str_2)
                    word_dict["all"].update(str_1.split(" "))
            lexicon_words = sorted(word_dict["all"])
            print("len(lexicon_words) = %d " % len(lexicon_words))

            char_list = []
            for cur_word in lexicon_words:
                for cur_char in cur_word:
                    char_list.append(cur_char)
            char_list = list(set(char_list))
            char_list_sort = sorted(char_list)
            print("len(char_list) = %d " % len(char_list_sort))
            print(char_list)
            print(char_list_sort)
            print("\n".join(char_list_sort))
            exit()


def check_all():
    token_file  = "/home/psc/Desktop/code/asr/process_audios/data/test2/data/am/tokens.txt"
    lexicon_txt = "/home/psc/Desktop/code/asr/process_audios/data/test2/data/am/lexicon.txt"
    char_list = []
    with open(token_file, "r") as fr:
        for line in fr:
            char_list.append(line.strip())
    char_list = list(set(char_list))
    print("len(char_list) = %d " % len(char_list))

    l_char_list = []
    with open(lexicon_txt, "r") as fr:
        for line in fr:
            wrd, chars = line.strip().split("\t")
            l_char_list += chars.split(" ")
    l_char_list = list(set(l_char_list))
    print("len(l_char_list) = %d " % len(l_char_list))

    for rr in l_char_list:
        if rr not in char_list:
            print(rr)
    print("************************************")
    for ll in char_list:
        if ll not in l_char_list:
            print(ll)


if __name__ == "__main__":
    # write_token_lexicon()
    print("write_token_lexicon done")

    # get_tokens()
    print("get_tokens done")

    check_all()

