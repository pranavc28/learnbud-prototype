#!/usr/bin/env python3
"""Maps has ids as keys.
Calculate sim score for each other id.

Output is formatted as such:
id  (other_id, sim_score)
other_id  (id, sim_score)

This is because other_id always > id.
"""

import csv
import sys

from itertools import islice

WEIGHTS = [0.0, 0.0, 0.0, 0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.1, 0.1, 0.1, 0.05]

def get_score(line1, line2):
    sim_score = 0
    for i in range(3, 16):
        if line1[i] == line2[i]:
            sim_score += WEIGHTS[i]

    return sim_score

with open("input/input.csv", "r") as f1:
    reader1 = csv.reader(f1)
    next(reader1)
    for i, line1 in enumerate(reader1):
        with open("input/input.csv", "r") as f2:
            reader2 = csv.reader(f2)
            next(reader2)
            for j, line2 in islice(enumerate(reader2), i+1, None):
                sim_score = get_score(line1, line2)
                sim_tuple1 = (line2[0], sim_score)
                sim_tuple2 = (line1[0], sim_score)
                print(f"{line1[0]}\t{sim_tuple1}")
                print(f"{line2[0]}\t{sim_tuple2}")
