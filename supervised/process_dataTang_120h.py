# -*- coding: utf-8 -*-

import os
import util_funcs


def main_process(base_dir):
    exts = ["wav"]
    all_dir = os.path.join(base_dir, "all")
    if not os.path.exists(all_dir):
        os.mkdir(all_dir)

    print("-----------step1: 移动音频和txt文件到统一的all的目录-----------")
    # wav_list = []
    # for sub_folder in os.listdir(base_dir):
    #     sub_folder_path = os.path.join(base_dir, sub_folder)
    #     if os.path.isdir(sub_folder_path):
    #         for file in os.listdir(sub_folder_path):
    #             src_wav = os.path.join(sub_folder_path, file)
    #             if any(src_wav.lower().endswith("." + ext) for ext in exts):
    #                 wav_list.append(src_wav)
    #
    # for src_wav in wav_list:
    #     if os.path.isfile(src_wav):
    #         file = os.path.basename(src_wav)
    #         dst_wav = os.path.join(all_dir, file)
    #         os.system("mv %s %s" % (src_wav, dst_wav))
    #         src_txt = src_wav.replace(".wav", ".txt")
    #         dst_txt = dst_wav.replace(".wav", ".txt")
    #         os.system("mv %s %s" % (src_txt, dst_txt))
    #         src_metadata = src_wav.replace(".wav", ".metadata")
    #         os.system("rm %s" % src_metadata)
    #
    # print("-----------step2: 删除不需要的只含有metadata的文件夹-----------")
    # for sub_folder in os.listdir(base_dir):
    #     sub_folder_path = os.path.join(base_dir, sub_folder)
    #     if os.path.isdir(sub_folder_path):
    #         if "all" not in sub_folder:
    #             os.system("rm -rf %s" % sub_folder_path)

    print("-----------step3: 提取txt里面的内容,写到all.txt里面-----------")
    all_list = []
    all_txt = all_dir + ".txt"
    for file in os.listdir(all_dir):
        src_wav = os.path.join(all_dir, file)
        if any(src_wav.lower().endswith("." + ext) for ext in exts):
            if os.path.isfile(src_wav):
                src_txt = src_wav.replace(".wav", ".txt")
                cur_line = util_funcs.read_txt_2_str(src_txt)
                strlist = cur_line.split("\t")
                if len(strlist) != 3:
                    print("error line : ", cur_line)
                    print("cur_label_hanzi : ", strlist[2])
                cur_label_hanzi = strlist[2]
                cur_line_save = file.replace(".wav", "") + "<--->" + cur_label_hanzi
                all_list.append(cur_line_save)
    util_funcs.write_list_2_txt(all_list, all_txt)


if __name__ == '__main__':
    base_dir = "/sdb/speechRecong/chinese/dataTang/zips/120h"
    main_process(base_dir)