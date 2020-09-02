import os
import glob
import string
import re
import numpy as np


dataTang_trans_path = "/home/psc/Desktop/code/asr/trans_dataTang.txt"
dataTang_list = []
print("cur process txt file: %s " % dataTang_trans_path)
with open(dataTang_trans_path, "r") as fr:
    for cur_line in fr:
        audio_name, cur_trans = cur_line.strip().split("<--->")
        dataTang_list.append(cur_trans)
print("total trans len of dataTang = %d " % len(dataTang_list))

# dataTang_trans_path_saved = dataTang_trans_path.replace(".txt", "_saved.txt")
# with open(dataTang_trans_path_saved, "w") as fw:
#     for cur_line in dataTang_list:
#         fw.write(cur_line + "\n")


guiji_70w_trans_path = "trans_guiji_70w.txt"
guiji_70w_list = []
print("cur process txt file: %s " % guiji_70w_trans_path)
overlap_cnt = 0
with open(guiji_70w_trans_path, "r") as fr:
    for cur_line in fr:
        audio_name, cur_trans = cur_line.strip().split("<--->")
        guiji_70w_list.append(cur_trans)
        if cur_trans in dataTang_list:
            overlap_cnt += 1


print("total trans len of guiji_70w = %d " % len(guiji_70w_list))
print("total overlap_cnt = %d " % overlap_cnt)

'''
cur process txt file: trans_dataTang.txt 
total trans len of dataTang = 165343 
cur process txt file: trans_guiji_70w.txt 
total trans len of guiji_70w = 442947 
total overlap_cnt = 84219
'''
