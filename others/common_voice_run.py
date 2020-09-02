import os
import math


wavdir = '../data/commonVoice/zh/clips'
rm_cnt = 0
for wav_id in os.listdir(wavdir):
    if wav_id.lower().endswith("mp3"):
        cur_mp3_wavfile = os.path.join(wavdir, wav_id)
        cur_wav_wavfile = os.path.join(wavdir, wav_id.lower().replace(".mp3", ".wav"))
        cmd = "ffmpeg -i {} -acodec pcm_s16le -ac 1 -ar 16000 {}".format(cur_mp3_wavfile, cur_wav_wavfile)
        os.system(cmd)
        os.remove(cur_mp3_wavfile)
        rm_cnt += 1
print('total remove cnt = %d ' % rm_cnt)
