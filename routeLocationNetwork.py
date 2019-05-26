"""
Desc:
    脚本 - 从唐宋编年史地图数据中
    使用自定义的规则
    构建地点之间的关联关系
"""

import os
import re
import json
import settings
import networkx as nx

INPUT_DIR = os.path.join(settings.INPUT_PATH, 'route')
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, 'route')
FRE_THRESHOLD = 10


def main():
    r_route = re.compile(r" → |;")
    graph = nx.DiGraph()
    result = {}

    with open(os.path.join(INPUT_DIR, 'geolocation.json'), 'r+', encoding='utf-8') as f:
        geolocation = json.load(f)["RECORDS"]

    for item in geolocation:
        locations = r_route.split(item["geo_route"])
        len_locations = len(locations)
        for index in range(len_locations):
            if index > 0:
                loc1 = locations[index - 1]
                loc2 = locations[index]
                if loc1 in result.keys():
                    if loc2 in result[loc1].keys():
                        result[loc1][loc2] += 1
                    else:
                        result[loc1][loc2] = 1
                else:
                    result[loc1] = {}
                    result[loc1][loc2] = 1

    for k1, v1 in result.items():
        for k2, v2 in v1.items():
            print(v2)
            if v2 >= FRE_THRESHOLD:
                loc1 = k1
                loc2 = k2
                if not graph.has_node(loc1):
                    graph.add_node(loc1)
                if not graph.has_node(loc2):
                    graph.add_node(loc2)
                graph.add_edge(loc1, loc2, weight=v2)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    nx.write_gexf(graph, os.path.join(OUTPUT_DIR, 'routeLocation.gexf'))


if __name__ == '__main__':
    main()
