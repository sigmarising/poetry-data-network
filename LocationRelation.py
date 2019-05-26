"""
File: LocationRelation.py
Desc:
    脚本 - 使用类似的关联规则
    从诗人提及的地点中
    构建地点之间的关联关系
"""

import os
import json
import settings
import networkx as nx
from collections import Counter

INPUT_DIR = os.path.join(settings.INPUT_PATH, "nerResult")
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, "relation")
FRE_THRESHOLD = 4
COUNT_THRESHOLD = 0.9
RESULT_THRESHOLD = 3

if __name__ == '__main__':
    all_sets = []
    all_loc = set()

    graph = nx.DiGraph()

    for dynasty in os.listdir(INPUT_DIR):
        dynasty_path = os.path.join(INPUT_DIR, dynasty)
        for file in os.listdir(dynasty_path):
            file_path = os.path.join(dynasty_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            locs_counter = Counter(raw["location"])
            locs = []
            for k, v in locs_counter.items():
                if v >= FRE_THRESHOLD and len(k) > 1:
                    locs.append(k)
            if len(locs) > 0:
                all_sets.append(locs)
                all_loc.update(locs)

    count = 0
    sum_all = len(all_loc)
    for k1 in all_loc:
        r = {"summary": 0}
        for arr in all_sets:
            if k1 in arr:
                r["summary"] += 1
                for item in arr:
                    if k1 != item:
                        if item in r.keys():
                            r[item] += 1
                        else:
                            r[item] = 1

        count += 1
        print("\rHandling {:.2f}%".format(count * 100 / sum_all), end="")
        num1 = r["summary"]
        for k2 in all_loc:
            if k1 != k2 and k2 in r.keys() and r[k2] >= RESULT_THRESHOLD:
                num2 = r[k2]
                val = num2 / num1
                # print(val)
                if val >= COUNT_THRESHOLD:
                    if not graph.has_node(k1):
                        graph.add_node(k1)
                    if not graph.has_node(k2):
                        graph.add_node(k2)
                    graph.add_edge(k1, k2, weight=val)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    nx.write_gexf(graph, os.path.join(OUTPUT_DIR, "relationLoc.gexf"))
