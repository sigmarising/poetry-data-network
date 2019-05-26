"""
Desc:
    脚本 - 从唐宋编年史地图数据中
    格式化三个诗人的轨迹信息
"""

import os
import re
import json
import settings

INPUT_DIR = os.path.join(settings.INPUT_PATH, 'route')
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, 'route')


def __find_loc(location: str, name: str, data: list) -> (float, float):
    for i in data:
        if location == i["loc_name"] and name == i["person_name"]:
            return i["loc_lng"], i["loc_lat"]


def main():
    r_route = re.compile(r" → |;")

    result = {
        "李白": None,
        "杜甫": None,
        "苏轼": None
    }

    with open(os.path.join(INPUT_DIR, 'geolocation.json'), 'r+', encoding='utf-8') as f:
        geolocation = json.load(f)["RECORDS"]
    with open(os.path.join(INPUT_DIR, 'location.json'), 'r+', encoding='utf-8') as f:
        all_location = json.load(f)["RECORDS"]

    for item_person in geolocation:
        if item_person["geo_name"] in result.keys():
            locations = r_route.split(item_person["geo_route"])
            result[item_person["geo_name"]] = {
                "edges": [],
                "nodes": []
            }
            for location in locations:
                result[item_person["geo_name"]]["nodes"].append(
                    {
                        "name": location,
                        "symbolSize": 10,
                        "value": [*__find_loc(location, item_person["geo_name"], all_location), 10]
                    }
                )
                index = len(result[item_person["geo_name"]]["nodes"]) - 1
                if index > 0:
                    result[item_person["geo_name"]]["edges"].append({
                        "coords": [
                            result[item_person["geo_name"]]["nodes"][index - 1]["value"][0:2],
                            result[item_person["geo_name"]]["nodes"][index]["value"][0:2],
                        ],
                        "fromName": result[item_person["geo_name"]]["nodes"][index - 1]["name"],
                        "toName": result[item_person["geo_name"]]["nodes"][index]["name"]
                    })

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, "threeMan.json"), "w+", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
