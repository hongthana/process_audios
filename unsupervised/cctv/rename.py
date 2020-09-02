import glob
import os
import re
import shutil

d = '/home/psc/Desktop/code/asr/process_audios/unsupervised/cctv/data'
# fns = glob.glob('%s/*.webm' % d)
# index = 3
# for fn in fns:
#     mo = re.search(r'\[等着我第二季\]', fn)
#     if mo:
#         new_fn = os.path.join(d, '等着我第二季' + str(index) + '.webm')   # mp4
#         mfn = os.path.basename(fn)
#         print('renaming:', mfn)
#         print('    to:', new_fn)
#         # os.rename(fn, new_fn)
#         shutil.move(fn, new_fn)
#         index += 1
#     else:
#         print(fn, 'not matched')


fns = glob.glob('%s/*.webm' % d)
for fn in fns:
    mo = re.search(r'\d{8}', fn)
    if mo:
        new_fn = os.path.join(d, '生活提示' + mo.group(0) + '.webm')   # mp4
        mfn = os.path.basename(fn)
        print('renaming:', mfn)
        print('    to:', new_fn)
        # os.rename(fn, new_fn)
        shutil.move(fn, new_fn)
    else:
        print(fn, 'not matched')

'''
d = '/home/psc/Desktop/code/asr/data/talkShow/徐杰慢半拍'

fns = glob.glob('%s/*.webm' % d)
for fn in fns:
    mo = re.search(r'\d{8}', fn)
    if mo:
        new_fn = os.path.join(d, '徐杰慢半拍' + mo.group(0) + '.webm')
        mfn = os.path.basename(fn)
        print('renaming:', mfn)
        print('    to:', new_fn)
        if os.path.exists(new_fn):
            print("{} alreadly exists. ".format(new_fn))
        else:
            shutil.move(fn, new_fn)
    else:
        print(fn, 'not matched')
'''
