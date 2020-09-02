import glob
import os
import re
import shutil


# base_dir = '/home/psc/Desktop/code/asr/data/wav2vec/src_downloads/talkShow/周周侃'
#
# index = 0
# fns = glob.glob('%s/*.webm' % base_dir)
# for fn in fns:
#     index += 1
#     src_fn = os.path.basename(fn)
#     index_str = str(index).zfill(4)
#     new_fn = os.path.join(base_dir, '周周侃' + index_str + '.webm')
#     if os.path.exists(new_fn):
#         print("{} alreadly exists. ".format(new_fn))
#     else:
#         print('renaming: {}  to: {}'.format(fn, new_fn))
#         shutil.move(fn, new_fn)


base_dir = "/home/psc/Desktop/code/asr/process_audios/talkShow/第四季"

fns = glob.glob('%s/*.webm' % base_dir)
for fn in fns:
    mo = re.search(r'\d{8}', fn)
    if mo:
        l1 = mo.span()[1]
        l2 = l1 + 5
        # new_fn = os.path.join(base_dir, '奇葩说第四季' + mo.group(0) + fn[l1:l2] + '.webm')
        new_fn = os.path.join(base_dir, '奇葩说第四季' + mo.group(0) + '.webm')
        mfn = os.path.basename(fn)
        print('renaming:', mfn)
        print('    to:', new_fn)
        if os.path.exists(new_fn):
            print("{} alreadly exists. ".format(new_fn))
        else:
            shutil.move(fn, new_fn)
    else:
        print(fn, 'not matched')