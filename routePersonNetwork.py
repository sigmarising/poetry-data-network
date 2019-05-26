"""
Desc:
    脚本 - 从唐宋编年史地图数据中
    使用自定义的规则
    构建人物之间的关联关系
"""

import os
import re
import json
import settings
import Levenshtein
import networkx as nx

INPUT_DIR = os.path.join(settings.INPUT_PATH, 'route')
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, 'route')
RATIO_THRESHOLD = 0.40


def __find_loc(location: str, name: str, data: list) -> (float, float):
    for i in data:
        if location == i["loc_name"] and name == i["person_name"]:
            return i["loc_lng"], i["loc_lat"]


def main():
    r_route = re.compile(r" → |;")
    graph = nx.Graph()

    with open(os.path.join(INPUT_DIR, 'geolocation.json'), 'r+', encoding='utf-8') as f:
        geolocation = json.load(f)["RECORDS"]
    # with open(os.path.join(INPUT_DIR, 'location.json'), 'r+', encoding='utf-8') as f:
    #     all_location = json.load(f)["RECORDS"]

    geo_len = len(geolocation)
    for i in range(geo_len):
        for j in range(i+1, geo_len):
            loc1 = r_route.split(geolocation[i]["geo_route"])
            loc2 = r_route.split(geolocation[j]["geo_route"])
            val = Levenshtein.ratio("".join(loc1), "".join(loc2))
            print(val)
            if val >= RATIO_THRESHOLD:
                person1 = geolocation[i]["geo_dynasty"] + " " + geolocation[i]["geo_name"]
                person2 = geolocation[j]["geo_dynasty"] + " " + geolocation[j]["geo_name"]
                if not graph.has_node(person1):
                    graph.add_node(person1)
                if not graph.has_node(person2):
                    graph.add_node(person2)
                graph.add_edge(person1, person2, weight=val)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    # with open(os.path.join(OUTPUT_DIR, "threeMan.json"), "w+", encoding="utf-8") as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)
    nx.write_gexf(graph, os.path.join(OUTPUT_DIR, 'routePerson.gexf'))


if __name__ == '__main__':
    main()
