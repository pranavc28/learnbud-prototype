#!/usr/bin/env python3
"""Reduce calculates the highest x scores."""

import pymysql
import sys

from ast import literal_eval

# Get top n matches
prev_id = -1
matches = {}
for line in sys.stdin:
    cur_id, cur_str = line.split("\t")
    cur_tuple = literal_eval(cur_str)
    if cur_id != prev_id:
        matches[cur_id] = []
        prev_id = cur_id
    matches[cur_id].append(cur_tuple)
    matches[cur_id] = sorted(matches[cur_id], key=lambda x: -x[1])[:2]  # currently returns top 2 most similar

# Connect to MySQL database and insert data
conn = pymysql.connect(
        host = "", #endpoint link
        port = 3306, # 3306
        user = "", # admin
        password = "", #
        db = "", #test
)

cur = conn.cursor()
cur.execute("TRUNCATE TABLE Matches2")
for k, v in matches.items():
    matches_str = ""
    for t in v:
        matches_str = matches_str + ",".join(str(i) for i in t) + "\t"
    cur.execute("INSERT INTO Matches2 (id,matches) VALUES (%s,%s)", (k,matches_str))
    conn.commit()
