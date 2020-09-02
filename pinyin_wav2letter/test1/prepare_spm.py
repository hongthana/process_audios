# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import re
import string
from collections import defaultdict

import sentencepiece as spm


en_char = string.punctuation + u'abcdefghijklmnopqrstuvwxyz.?, '
pattern_char = re.compile('[%s]' % re.escape(en_char))
illegal_char = string.punctuation + u'“《》「」』『·—□〈〉•’●‘×”・∫'
pattern_ilflag = re.compile('[%s]' % re.escape(illegal_char))

all_flag = string.punctuation + u'“《》「」』『·—□〈〉•’●‘×”・∫,?!.'
pattern_flag = re.compile('[%s]' % re.escape(all_flag))
alpha_char = string.punctuation + u'abcdefghijklmnopqrstuvwxyz '
pattern_alpha = re.compile('[%s]' % re.escape(alpha_char))


def simple_text_clean111(str_in):
    str_1 = str_in.strip().lower().replace("?.", "?")
    str_2 = pattern_char.sub(u'', str_1)
    if len(str_2) > 0:
        # print(str_in)
        str_3 = pattern_ilflag.sub(u'', str_2)
        if len(str_3) > 0:
            print(str_3)
            return ""
        else:
            return pattern_ilflag.sub(u'', str_1)
    else:
        return str_1


def simple_text_clean(str_in):
    str_1 = pattern_flag.sub(u'', str_in.strip().lower().replace("  ", " "))
    str_2 = pattern_alpha.sub(u'', str_1)
    if len(str_2) > 0:
        print(str_2)
        return ""
    else:
        return str_1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Librispeech Dataset creation.")
    parser.add_argument(
        "--data_dst", help="data destination directory", default="/home/psc/Desktop/data/nlp"
    )
    parser.add_argument(
        "--model_dst",
        help="model auxilary files destination directory",
        default="./model",
    )
    parser.add_argument(
        "-p", "--process", help="# of process for Multiprocessing", default=8, type=int
    )
    parser.add_argument("--wp", help="number of word pieces", default=1200, type=int)      # 拼音<=4175,否则报错
    parser.add_argument(
        "--nbest",
        help="number of best segmentations for each word (or numbers comma separated)",
        default="10",
    )
    args = parser.parse_args()

    subpaths = {
        "train": ["wiki_zh_2019", "baike2018qa", "new2016zh", "translation2019zh", "webtext2019zh"]
    }

    pinyin_path = os.path.join(args.data_dst, "pinyin")
    am_path = os.path.join(args.model_dst, "am")
    decoder_path = os.path.join(args.model_dst, "decoder")
    os.makedirs(am_path, exist_ok=True)
    os.makedirs(decoder_path, exist_ok=True)

    # Generating am/*
    num_wordpieces = args.wp
    train_all_text = os.path.join(am_path, "train.txt")
    prefix = "zh-train-all-unigram-{}".format(num_wordpieces)
    prefix = os.path.join(am_path, prefix)
    vocab_name = prefix + ".vocab"
    model_name = prefix + ".model"

    # prepare data
    print("Preparing tokens and lexicon for acoustic model...\n", flush=True)
    word_dict = defaultdict(set)
    with open(train_all_text, "w") as ftext:
        for key, names in subpaths.items():
            for name in names:
                sub_dir = os.path.join(pinyin_path, name)
                for cur_file in os.listdir(sub_dir):
                    cur_file_path = os.path.join(sub_dir, cur_file)
                    with open(cur_file_path, "r") as flist:
                        for line in flist:
                            line_out = simple_text_clean(line)
                            if len(line_out) > 0:
                                transcription = line_out.split(" ")
                                ftext.write(" ".join(transcription) + "\n")
                                word_dict[key].update(transcription)
    lexicon_words = sorted(word_dict["train"])

    # train
    print("Computing word pieces...\n", flush=True)
    train_cmd = (
        "--input={input} --model_prefix={prefix} --vocab_size={sz}"
        " --character_coverage=1.0 --model_type=unigram --train_extremely_large_corpus"
        " --split_by_unicode_script=false --shuffle_input_sentence=true".format(
            input=train_all_text, prefix=prefix, sz=num_wordpieces
        )
    )
    spm.SentencePieceTrainer.Train(train_cmd)

    # word piece dictionary
    print("Creating word piece list...\n", flush=True)
    exclude_list = {"<unk>", "<s>", "</s>"}
    with open(vocab_name.replace(".vocab", ".tokens"), "w") as fvocab_filt:
        with open(vocab_name, "r", encoding="utf-8") as fvocab:
            for line in fvocab:
                val, _ = line.strip().split("\t", 1)
                if val not in exclude_list:
                    fvocab_filt.write(val.replace("\u2581", "_") + "\n")

    # word -> word piece lexicon for loading targets
    print("Creating word -> word pieces lexicon...\n", flush=True)
    sp = spm.SentencePieceProcessor()
    sp.Load(model_name)

    for nbest in args.nbest.split(","):
        nbest = int(nbest)
        lexicon_name = "librispeech-train+dev-unigram-{sz}-nbest{n}.lexicon".format(sz=num_wordpieces, n=nbest)
        with open(os.path.join(am_path, lexicon_name), "w") as f_lexicon:
            for word in lexicon_words:
                wps = sp.NBestEncodeAsPieces(word, nbest)
                for wp in wps:  # the order matters for our training
                    f_lexicon.write(
                        word
                        + "\t"
                        + " ".join([w.replace("\u2581", "_") for w in wp])
                        + "\n"
                    )
    print("Done!", flush=True)
