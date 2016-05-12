import shlex
import subprocess
import os
from itertools import product

test_path = 'test/test.txt'

for _, _, files in os.walk('train'):
    for f in files:
        out_file = 'results/' + f + '.result'
        subprocess.run('test.exe {} {} {}'.format(f, test_path, out_file))


# learn train_features.txt 5 .01 model_iter5_gamma.01
