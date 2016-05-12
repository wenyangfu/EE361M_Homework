import shlex
import subprocess
from itertools import product

iters = list(range(5, 55, 5))
learning_rate = [.1, .01, .001]

for num_iter, learning_rate in product(iters, learning_rate):
    subprocess.run('learn.exe train_features.txt {0} {1} model_iter{0}_gamma{1}'.format(
        num_iter, learning_rate))

# learn train_features.txt 5 .01 model_iter5_gamma.01
