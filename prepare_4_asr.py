from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys
import sox


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def findtranscriptfiles(dir):
    files = []
    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".trans.txt"):
                files.append(os.path.join(dirpath, filename))
    return files


def read_trans(transcriptfile):
    transcripts_dict = {}
    all_chars = []
    with open(transcriptfile, "r") as fr:
        for line in fr:
            fname, transcript = line.strip().split("<--->")
            transcripts_dict[fname] = transcript
            for c in transcript:
                if is_Chinese(c):
                    all_chars.append(c)
                else:
                    print("%s not a chinese char" % c)
                    print(line.strip())
    return transcripts_dict, all_chars


def write_lst(basedir, subpaths, lists_dst):
    for subpath in subpaths:
        print("cur process %s" % subpath)
        cur_wav_dir = os.path.join(basedir, subpath)
        cur_trans_file = os.path.join(cur_wav_dir, "trans.txt")
        cur_transcripts_dict, cur_chars = read_trans(cur_trans_file)

        assert os.path.exists(cur_wav_dir), "Unable to find the directory - '{src}'".format(src=cur_wav_dir)
        dst = os.path.join(lists_dst, subpath + ".lst")
        sys.stdout.write("analyzing {src}...\n".format(src=cur_wav_dir))
        sys.stdout.flush()

        with open(dst, "w") as f:
            for dirpath, _, filenames in os.walk(cur_wav_dir):
                for filename in filenames:
                    if filename.endswith(".wav"):
                        wav_filename = filename.replace(".wav", "")
                        audio_path = os.path.join(dirpath, filename)
                        handle = os.path.basename(dirpath)
                        if not os.path.exists(audio_path):
                            print("'{src}' cannot find wav file".format(src=filename))
                            continue

                        cur_transcript = cur_transcripts_dict.get(wav_filename, "")
                        if "" == cur_transcript:
                            print(wav_filename, " don't have trans")
                            continue

                        writeline = []
                        writeline.append(subpath + "-" + handle)  # sampleid
                        writeline.append(audio_path)
                        writeline.append(str(sox.file_info.duration(audio_path)))  # length
                        writeline.append(cur_transcript)
                        f.write("\t".join(writeline) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Librispeech Dataset creation.")
    parser.add_argument("--base_dir", default='/devdata/home/pishichan/code/asr/data/mandarin/supervised', help="source directory")
    # parser.add_argument("--base_dir", default='/home/psc/data', help="source directory")
    parser.add_argument("--dst", default='output', help="destination directory")
    args = parser.parse_args()

    read_dir = os.path.join(args.base_dir, "read")
    speak_dir = os.path.join(args.base_dir, "speak")
    assert os.path.isdir(str(read_dir)), "read_dir directory not found - '{d}'".format(d=read_dir)
    assert os.path.isdir(str(speak_dir)), "speak_dir directory not found - '{d}'".format(d=speak_dir)
    os.makedirs(args.dst, exist_ok=True)
    lists_dst = os.path.join(args.dst, "lists")
    os.makedirs(lists_dst, exist_ok=True)
    am_dst = os.path.join(args.dst, "am")
    os.makedirs(am_dst, exist_ok=True)

    read_subpaths = ["guijitts", "prime", "ST", "aishell1", "commonVoice"]
    write_lst(read_dir, read_subpaths, lists_dst)

    speak_subpaths = ["dataTang", "guiji", "htrs", "guiji_70w"]
    write_lst(speak_dir, speak_subpaths, lists_dst)


    # # create tokens dictionary
    # tkn_file = os.path.join(am_dst, "tokens.txt")
    # sys.stdout.write("creating tokens file {t}...\n".format(t=tkn_file))
    # sys.stdout.flush()
    # with open(tkn_file, "w") as f:
    #     for c in list(set(all_chars)):
    #         f.write(c + "\n")
    #
    # # create leixcon
    # lexicon_file = os.path.join(am_dst, "lexicon.txt")
    # sys.stdout.write("creating train lexicon file {t}...\n".format(t=tkn_file))
    # sys.stdout.flush()
    # with open(lexicon_file, "w", encoding="utf-8") as f:
    #     for w in train_dev_words.keys():
    #         f.write(w)
    #         f.write("\t")
    #         f.write(" ".join(w))
    #         f.write(" \n")
    # sys.stdout.write("Done !\n")


