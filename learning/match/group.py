#!/usr/bin/env python3
"""Grouping process.
Sorts all the lines.
"""

import sys

data = sys.stdin.readlines()
data.sort()
for i in range(len(data)):
    print(data[i], end='')
