# -*- coding: utf-8 -*-

import os, re
import util_funcs
import wave


def cut_wav_by_time(wavfile_in, wavfile_out, t0, t1):
    win = wave.open(wavfile_in, 'rb')
    try:
        wout = wave.open(wavfile_out, 'wb')
    except Exception as e:
        print("wave write failed: " + str(type(e).__name__))
        print(str(wavfile_out) + ": " + str(t0) + "<--->" + str(t1))
        return
    s0, s1 = int(t0 * win.getframerate()), int(t1 * win.getframerate())
    win.readframes(s0)  # discard
    frames = win.readframes(s1 - s0)

    wout.setparams(win.getparams())
    wout.writeframes(frames)

    win.close()
    wout.close()


def process_scripts(src_txt):
    seg_dict = {}

    line_list_all = []
    usrful_begin, usrful_end = 0, 0
    with open(src_txt,"r") as fr:
        for line in fr:
            cur_line = line.strip()
            if "item [1]:" in cur_line:
                usrful_begin = len(line_list_all)
            elif "item [2]:" in cur_line:
                usrful_end = len(line_list_all)
            line_list_all.append(cur_line)

    print("usrful_begin = ", usrful_begin)
    print("usrful_end = ", usrful_end)
    line_list = line_list_all[usrful_begin:usrful_end]
    index_str1 = "intervals ["
    index_str2 = "]:"
    index = usrful_begin+6
    while index < len(line_list):
        cur_line = line_list[index]
        print(cur_line)
        pos_index_begin = cur_line.find(index_str1)
        pos_index_end = cur_line.rfind(index_str2)
        index_str = cur_line[pos_index_begin + len(index_str1):pos_index_end]
        time_begin = line_list[index+1].replace("xmin = ", "")
        time_end = line_list[index + 2].replace("xmax = ", "")
        script_str = line_list[index + 3].replace("text = ", "")
        seg_dict[int(index_str)] = [float(time_begin), float(time_end), script_str]
        index += 4
    return seg_dict


def seg_wav_bydict(wavfile_in, paras_dict, wavseg_folder):
    file_script_dict = {}
    print("wavfile_in = ", wavfile_in)
    basename = os.path.basename(wavfile_in).replace(".wav", "")

    for index, list_cont in paras_dict.items():
        time_start = list_cont[0]
        time_end = list_cont[1]
        script = list_cont[2]
        file_name = "%s-%d" % (basename, index)
        cur_seg_wavpath = os.path.join(wavseg_folder, "%s.wav" % file_name)
        file_script_dict[file_name] = script
        cut_wav_by_time(wavfile_in, cur_seg_wavpath, float(time_start), float(time_end))
    return file_script_dict


def move_wavs_txts(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    wav_list = []
    txt_list = []
    for sub_folder in os.listdir(src_dir):
        sub_folder_path = os.path.join(src_dir, sub_folder)
        if os.path.isdir(sub_folder_path):
            for file in os.listdir(sub_folder_path):
                src_wav = os.path.join(sub_folder_path, file)
                if any(src_wav.lower().endswith("." + ext) for ext in ["wav"]):
                    wav_list.append(src_wav)
        elif os.path.isfile(sub_folder_path):
            if any(sub_folder_path.lower().endswith("." + ext) for ext in ["txt"]):
                txt_list.append(sub_folder_path)
        else:
            pass

    for src_wav in wav_list:
        if os.path.isfile(src_wav):
            cur_filename = os.path.basename(src_wav)
            dst_wav = os.path.join(dst_dir, cur_filename)
            os.system("mv %s %s" % (src_wav, dst_wav))
    all_label_list = []
    for src_txt in txt_list:
        if os.path.isfile(src_txt):
            cur_txt_list = util_funcs.read_txt_2_list(src_txt)
            all_label_list += cur_txt_list
    all_txtfile = dst_dir + ".txt"
    util_funcs.write_list_2_txt(all_label_list, all_txtfile)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_txt_rm(all_dir):
    match1 = re.compile(r'\[.*?\]')
    all_txtfile = all_dir + ".txt"
    if not os.path.isfile(all_txtfile):
        print("%s not exist "% all_txtfile)
    all_line_list = util_funcs.read_txt_2_list(all_txtfile)
    all_out_list = []
    for line in all_line_list:
        try:
            wav_file, cur_label = line.split("<--->")
        except:
            print("cur line %s , split failed", line)
            continue
        cur_label1 = match1.sub('', cur_label)
        cur_label2 = cur_label1.replace("\"", "")
        if len(cur_label2) < 1:
            wav_file_path = os.path.join(all_dir, wav_file + ".wav")
            if os.path.exists(wav_file_path):
                os.system("rm %s" % wav_file_path)
            else:
                print("%s not exist " % wav_file_path)
        else:
            line_new = wav_file + "<--->" + cur_label2
            all_out_list.append(line_new)
        # if len(cur_label) > 5:
        #     if cur_label[5] == " " and is_number(cur_label[2:5]) and cur_label[0]=="1":
        #         print("cur_label = ", cur_label)
        #         cur_label2 = cur_label[6:]
        #         line_new = wav_file + "<--->" + cur_label2
        #         all_out_list.append(line_new)
        #     else:
        #         all_out_list.append(line)
        # else:
        #     all_out_list.append(line)

    os.system("mv %s %s"%(all_txtfile, all_txtfile.replace(".txt", "-bak.txt")))
    util_funcs.write_list_2_txt(all_out_list, all_txtfile)


def main_process(base_dir):
    print("step1: 按照TextGrid里的时间段的要求分割音频到各自同名文件夹中")
    exts = ["textgrid"]
    wav_folder = os.path.join(base_dir, "wav")
    txt_folder = os.path.join(base_dir, "txt")
    wavseg_folder = os.path.join(base_dir, "wavseg")
    os.makedirs(wavseg_folder, exist_ok=True)
    for file in os.listdir(txt_folder):
        src_txt = os.path.join(txt_folder, file)
        if any(src_txt.lower().endswith("." + ext) for ext in exts):
            if os.path.isfile(src_txt):
                print("cur process textgrid : ", src_txt)
                seg_dict = process_scripts(src_txt)

                wavfile_in = os.path.join(wav_folder, file.replace(".TextGrid", ".wav"))
                if os.path.exists(wavfile_in):
                    cur_filename = os.path.basename(wavfile_in).replace(".wav", "")
                    cur_wavseg_dir = os.path.join(wavseg_folder, cur_filename)
                    cur_txtfile = os.path.join(wavseg_folder, cur_filename + ".txt")
                    os.makedirs(cur_wavseg_dir, exist_ok=True)
                    name_map_dict = seg_wav_bydict(wavfile_in, seg_dict, cur_wavseg_dir)
                    print("name_map_dict_len = " + str(len(name_map_dict)))
                    util_funcs.write_dict_to_txt(name_map_dict, cur_txtfile)

    print("all done")
    # print("step2: 将分割文件夹中音频和txt整理统一到单独的文件夹和目录")
    # wav_dir_out = wavseg_folder + "_out"
    # os.makedirs(wav_dir_out, exist_ok=True)
    # move_wavs_txts(wavseg_folder, wav_dir_out)

    # print("step3: 剔除不符合要求的txt_line及对应的wav")
    # wav_dir_out = "/sdb/speechRecong/chinese/dataTang/tt/220h/all"
    # check_txt_rm(wav_dir_out)



if __name__ == '__main__':
    base_dir = "/home/psc/Desktop/code/asr/data/mandarin/supervised/dataTang/616"
    main_process(base_dir)
