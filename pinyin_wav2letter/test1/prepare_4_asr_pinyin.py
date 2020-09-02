# -*- coding: utf-8 -*-

import os
import re
import string
import unicodedata
from pypinyin import pinyin, lazy_pinyin, Style
from collections import defaultdict
import sentencepiece as spm


all_flag = string.punctuation + u'“《》「」』『·—□〈〉•’●‘×”・∫,?!.'
pattern_flag = re.compile('[%s]' % re.escape(all_flag))
alpha_char = string.punctuation + u'abcdefghijklmnopqrstuvwxyz '
pattern_alpha = re.compile('[%s]' % re.escape(alpha_char))

trantab = str.maketrans('，。！？【】（）％＃＠＆１２３４５６７８９０、', ',.!?[]()%#@&1234567890,')


def get_pinyin(str_in):
    text_1 = unicodedata.normalize('NFKC', str_in.lower().replace(" ", ""))      # 中文标点转换为英文标点
    text_2 = text_1.translate(trantab)  # 漏网之鱼手动修改对应
    cur_pinyin = pinyin(text_2, style=Style.TONE3, heteronym=False)  # 设置拼音风格, 启用多音字模式
    cur_line = ""
    for cur_char in cur_pinyin:
        cur_line += cur_char[0].replace("1", "").replace("2", "").replace("3", "").replace("4", "") + " "
    str_out = cur_line[:-1]
    str_1 = pattern_flag.sub(u'', str_out.replace("  ", " "))
    str_2 = pattern_alpha.sub(u'', str_1)
    if len(str_2) > 0:
        print(str_2)
        return ""
    else:
        return str_1


def get_all_word(list_dir):
    word_dict = defaultdict(set)
    for cur_f in os.listdir(list_dir):
        print("cur process file: %s " % cur_f)
        cur_file_path = os.path.join(list_dir, cur_f)
        cur_file_path_save = cur_file_path.replace(".lst", "_pinyin.lst")
        with open(cur_file_path_save, "w") as fw:
            with open(cur_file_path, "r") as fr:
                for line in fr:
                    sampleid, audio_path, audio_len, cur_transcript = line.strip().split("\t")
                    cur_transcript_pinyin = get_pinyin(cur_transcript)
                    if len(cur_transcript_pinyin) == 0:
                        print("cur line convert to pinyin failed, %s " % cur_transcript)
                        continue
                    word_dict["all"].update(cur_transcript_pinyin.split(" "))
                    writeline = []
                    writeline.append(sampleid)  # sampleid
                    writeline.append(audio_path)
                    writeline.append(audio_len)
                    writeline.append(cur_transcript_pinyin)
                    fw.write("\t".join(writeline) + "\n")
    print("word to pinyin done! ")
    lexicon_words = sorted(word_dict["all"])
    return lexicon_words


if __name__ == "__main__":
    list_dir = "/home/psc/Desktop/code/asr/process_audios/data/wav/wav_lists"
    train_words = get_all_word(list_dir)
    lexicon_file = "/home/psc/Desktop/code/asr/process_audios/data/model/librispeech-train+dev-unigram-397-nbest10.lexicon"
    lexicon_wrd_list = []
    with open(lexicon_file, "r") as fr:
        for line in fr:
            cur_word, wcur_rd_pieces = line.strip().split("\t")
            lexicon_wrd_list.append(cur_word)
    lexicon_wrd_list = list(set(lexicon_wrd_list))
    all_wrd_list = train_words + lexicon_wrd_list
    all_wrd_list = list(set(all_wrd_list))
    all_wrd_list_sort = sorted(all_wrd_list)
    all_wrd_file = "all_word.txt"
    with open(all_wrd_file, "w") as fw:
        for cur_wrd in all_wrd_list_sort:
            fw.write(cur_wrd + "\n")

    # word -> word piece lexicon for loading targets
    print("Creating word -> word pieces lexicon...\n", flush=True)
    model_file = "/home/psc/Desktop/code/asr/process_audios/data/model/zh-train-all-unigram-397.model"
    sp = spm.SentencePieceProcessor()
    sp.Load(model_file)

    nbest_in = "10"
    num_wordpieces = 397
    for nbest in nbest_in.split(","):
        nbest = int(nbest)
        all_wrd_lexicon_name = "unigram-{sz}-nbest{n}.lexicon".format(sz=num_wordpieces, n=nbest)
        with open(all_wrd_lexicon_name, "w") as f_lexicon:
            for word in all_wrd_list_sort:
                wps = sp.NBestEncodeAsPieces(word, nbest)
                for wp in wps:  # the order matters for our training
                    f_lexicon.write(
                        word
                        + "\t"
                        + " ".join([w.replace("\u2581", "_") for w in wp])
                        + "\n"
                    )
    print("Done!", flush=True)

