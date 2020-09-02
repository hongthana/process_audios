# coding=utf-8
#! /usr/bin/env python3

import os, sys
import re


def read_txt_2_str(src_txt):
    lineCnt = 0
    with open(src_txt, 'r') as fr:
        for line in fr:
            lineCnt += 1
            line = line.strip('\r\n')
            return line


def get_label_2_dict(src_txt):
    dst_dict = {}
    with open(src_txt, 'r') as fr:
        for line in fr:
            filename, label = line.strip('\r\n').split('<--->')
            dst_dict[filename] = label
    return dst_dict


def read_txt_2_list(src_txt):
    lineCnt = 0
    dst_list = []
    with open(src_txt, 'r') as fr:
        for line in fr:
            lineCnt += 1
            line = line.strip('\r\n')
            dst_list.append(line)
    return dst_list


def rm_flags(sentence):
    if sentence == None:
        return ""
    specific_symbol = u'\W'  # \W	匹配非字符、非汉字、非下划线和非数字
    sentence1 = re.sub(specific_symbol, "", sentence)  # 去除特殊符号，保留下划线
    sentence_rst = sentence1.replace("_", "")  # 去除下划线
    return sentence_rst


def rm_flags_no_alpha(sentence):
    if sentence != None:
        out_str = ""
        xx = u"([\u4e00-\u9fff]+)"
        pattern = re.compile(xx)
        results = pattern.findall(sentence)
        for result in results:
            out_str += result
        return out_str
    else:
        return ""


def check_alpha_digist(str_in):
    cur_label = rm_flags(str_in)
    rm_ad_label = rm_flags_no_alpha(cur_label)
    if len(cur_label) != len(rm_ad_label):
        return False
    else:
        return True


def write_dict_to_txt(src_dict, txt_file):
    with open(txt_file, 'wb') as fw:
        for key in sorted(src_dict.keys()):
            value = src_dict[key]
            w_line = str(key) + "<--->" + str(value)
            fw.write((w_line + '\n').encode('utf-8'))


def write_list_2_txt(src_list, txt_file):   
    with open(txt_file, 'wb') as fw:
        for ii in range(len(src_list)):
            w_line = src_list[ii]
            fw.write((w_line+'\n').encode('utf-8'))
            #fw.write((str(ii+1) + ': ' + w_line+'\n').encode('utf-8'))


def write_truelabel_2_txt(w_line, txt_file):
    with open(txt_file, 'wb') as fw:
        fw.write((w_line +'\n').encode('utf-8'))



def get_label_true_markSys(txt_file):
    if os.path.exists(txt_file):
        label_true = ''
        lineCnt = 0
        with open(txt_file, 'r') as fr:
            for line in fr:
                lineCnt += 1
                if (lineCnt == 1):
                    line = line.strip('\r\n')
                    label_true = line.replace(' ','')
    else:
        label_true = os.path.basename(txt_file.replace(".txt", ""))
    return label_true
