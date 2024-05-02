#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:18:50 PM CET 2024

@author hielke
"""

import os
import random
import sys
from collections import defaultdict

seed = abs(int(os.environ.get('SEED', 42)))
random.seed(seed)

included = defaultdict(set)  # Keep track of all traces included given size 'key'
# amount of traces sampled from a single Moore trace
k = abs(int(os.environ.get('KSIZE', 8)))
k = k or 1

alphabet_size = 2

sys.stderr.write(f'Run with {k=}, {seed=}\n')

# at some point all traces of size less than skip are sampled, and are just skipped.
skip = 1

# this keeps track of the amount of traces sampled for each size
maximums = [alphabet_size ** i for i in range(0, 30)]

for line in sys.stdin:

    line = line.strip()
    # print(line)
    splitted = line.split(' -> ', 1)
    if len(splitted) == 1:
        sys.stderr.write("Error with " + line)
        continue

    inp, out = splitted
    inp = inp.split(',')
    out = out.split(',')

    # print("nums", skip, len(out))
    max_k = min(len(out) - skip, k)
    if max_k < 1:
        continue
    # print(k, max_k, skip, len(out))
    taking = random.sample(range(skip, len(out)), max_k)
    for i in taking:
        tr = inp[:i]
        tr_str = ' '.join(tr)
        if tr_str in included[i]:
            continue
        included[i].add(tr_str)
        if i == skip and maximums[i] <= len(included[i]):
            del maximums[skip]
            del included[skip]
            skip += 1

        print(out[i], len(tr), tr_str)
