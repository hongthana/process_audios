import os


all_num = 0
train_dir = "/devdata/home/jiangda/code/SLU/end-to-end-SLU/Date_700k/audio/70w/train"
train_dir_dst = "/devdata/home/pishichan/code/asr/data/mandarin/supervised/guiji_70w"
os.makedirs(train_dir_dst, exist_ok=True)

src_trans_path = "trans_new.txt"
dst_trans_path = "trans.txt"
with open(dst_trans_path, "w") as fw:
    with open(src_trans_path, "r") as fr:
        for cur_line in fr:
            all_num += 1
            audio_name, cur_trans = cur_line.strip().split("<--->")
            audio_path = os.path.join(train_dir, audio_name+".wav")
            audio_path_dst = os.path.join(train_dir_dst, os.path.basename(audio_name)+".wav")
            if os.path.exists(audio_path):
                # cp_cmd = "cp %s %s" % (audio_path, audio_path_dst)
                # print(cp_cmd)
                sox_cmd = "sox -v 0.99 %s -r 16000 -c 1 %s" % (audio_path, audio_path_dst)
                print(sox_cmd)
                # os.system(sox_cmd)
                new_line = os.path.basename(audio_name) + "<--->" + cur_trans
                fw.write(new_line + "\n")