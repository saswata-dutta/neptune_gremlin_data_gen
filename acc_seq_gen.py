import random
import sys

SIZE = 200000000 # num accounts in sample
if len(sys.argv) == 2:
    SIZE = int(sys.argv[1])

with open('acc_seq', 'w') as fout:
    for id in range(0, SIZE):
        prefix = str(random.randrange(1000)).zfill(3)
        suffix = str(id).zfill(9)
        print(prefix + suffix, file=fout)
