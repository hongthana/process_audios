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


def read_trans(transcriptfile):
    transcripts_dict = {}
    all_chars = []
    with open(transcriptfile, "r") as fr:
        for cur_line in fr:
            line_list = cur_line.strip().split("<--->")
            if len(line_list) != 2:
                print(cur_line.strip())
            else:
                audio_name, cur_trans = cur_line.strip().split("<--->")
                transcripts_dict[audio_name] = cur_trans
            for c in cur_trans:
                if is_Chinese(c):
                    all_chars.append(c)
                else:
                    pass
                    # print("%s not a chinese char" % c)
                    # print(cur_line.strip())
    return transcripts_dict, all_chars


def write_lst(basedir, subpaths, lists_dst):
    for subpath in subpaths:
        print("cur process %s" % subpath)
        cur_wav_dir = os.path.join(basedir, subpath)
        cur_trans_file = cur_wav_dir + ".txt"
        cur_transcripts_dict, cur_chars = read_trans(cur_trans_file)

        assert os.path.exists(cur_wav_dir), "Unable to find the directory - '{src}'".format(src=cur_wav_dir)
        dst = os.path.join(lists_dst, os.path.basename(subpath) + ".lst")
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
    parser.add_argument("--base_dir", default='/devdata/home/pishichan/code/asr/data/test', help="source directory")
    parser.add_argument("--dst", default='output', help="destination directory")
    args = parser.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    lists_dst = os.path.join(args.dst, "lists")
    os.makedirs(lists_dst, exist_ok=True)

    read_subpaths = ["yitu/chat", "yitu/reverb", "xinwen/20200504", "guiji_test/audios_16k"]   # , "all/supervised"]
    write_lst(args.base_dir, read_subpaths, lists_dst)



