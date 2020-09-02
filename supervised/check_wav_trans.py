import os


basedir = '/devdata/home/pishichan/code/asr/data/mandarin/supervised/speak'
discard_num = 0
for cls_name in os.listdir(basedir):
    print("cur process folder: %s " % cls_name)
    cls_folder_path = os.path.join(basedir, cls_name)
    audio_folder_path = os.path.join(cls_folder_path, "wav")
    trans_path = os.path.join(cls_folder_path, "trans.txt")
    valid_audios = []
    less_num = 0
    new_trans_list =[]
    with open(trans_path, "r") as fr:
        for cur_line in fr:
            audio_name, cur_trans = cur_line.strip().split("<--->")
            cur_audio_path = os.path.join(audio_folder_path, audio_name + ".wav")
            if os.path.exists(cur_audio_path):
                valid_audios.append(audio_name)
                new_trans_list.append(cur_line)
            else:
                # print("%s in the trans, but not in disk." % audio_name)
                less_num += 1
    if less_num != 0:
        print("cur folder exist some audios (%d) in trans, but not in disk" % less_num)
        dst_trans_path = trans_path.replace(".txt", "_new.txt")
        with open(dst_trans_path, "w") as fw:
            for cur_line in new_trans_list:
                fw.write(cur_line)
    for audio_name in os.listdir(audio_folder_path):
        audio_path = os.path.join(audio_folder_path, audio_name)
        if audio_name.replace(".wav", "") not in valid_audios:
            discard_num += 1
            os.remove(audio_path)

print("total less_num = %d " % less_num)
print("total discard_num = %d " % discard_num)

'''
有效音频个数：
speak
dataTang, guiji, htrs,  guiji_70w
165343,   7413,  11186, 442947

read
ST,     aishell1, commonVoice, guijitts, prime
102376, 141379,      16264,      9779,   50369
'''
