"""
File: handleRoute.py
Desc:
    脚本 - 用于处理将唐宋编年史地图数据
    单纯依据轨迹地点指向信息 创建地点关系网络
"""

import os
import json
import settings
import networkx as nx
# import matplotlib.pyplot as plt

INPUT_DIR = os.path.join(settings.INPUT_PATH, 'route')
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, 'route')


def main():
    graph = nx.DiGraph()

    with open(os.path.join(INPUT_DIR, 'geolocation.json'), 'r+', encoding='utf-8', errors='ignore') as f:
        raw = json.load(f)

    all_record = raw["RECORDS"]
    for item in all_record:
        routes = item["geo_route"].split(';')
        for route in routes:
            locations = route.split(" → ")
            loc_pre = None
            for loc_this in locations:
                if loc_pre:
                    if not graph.has_node(loc_pre):
                        graph.add_node(loc_pre)
                    if not graph.has_node(loc_this):
                        graph.add_node(loc_this)
                    graph.add_edge(loc_pre, loc_this)
                loc_pre = loc_this
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    nx.write_gexf(graph, os.path.join(OUTPUT_DIR, "route.gexf"))
    # nx.draw(graph, pos=nx.random_layout(graph), node_color='b', edge_color='r', with_labels=False, node_size=20)
    # plt.savefig(os.path.join(OUTPUT_DIR, "route.png"))
    print("- DONE -")


if __name__ == '__main__':
    main()
