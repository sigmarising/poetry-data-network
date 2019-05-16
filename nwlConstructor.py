import os
import json
import settings
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from networkx.readwrite import json_graph
from module.ColorLogDecorator import ColorLogDecorator

INPUT_DIR = os.path.join(settings.INPUT_PATH, "nerResult")
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, 'networkRaw')
ABS_THRESHOLD = 1
NUM_THRESHOLD = 1


def __flush_str(msg: str):
    fixed_len = 70
    if len(msg) <= fixed_len:
        return msg[0:fixed_len].ljust(fixed_len, ' ')
    else:
        return msg[0:fixed_len - 3] + "..."


def main():
    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START -", "strong"))

    # the data structure
    all_filepath_list = []
    graph = nx.DiGraph()

    # step 1: init all file list
    print(ColorLogDecorator.yellow(__flush_str("Step 1 - init files list")), end="")
    for dynasty in os.listdir(INPUT_DIR):
        dynasty_path = os.path.join(INPUT_DIR, dynasty)
        for file in os.listdir(dynasty_path):
            msg = __flush_str("Step 1 - init files list: {}".format(dynasty + " " + file))
            msg = ColorLogDecorator.yellow(msg)
            print("\r{}".format(msg), end="")

            file_path = os.path.join(dynasty_path, file)
            all_filepath_list.append(file_path)
    all_filepath_list.sort()
    print("\r" + ColorLogDecorator.yellow(__flush_str("Step 1 - init files list: Done")))

    # step 2: construct the network
    print(ColorLogDecorator.yellow(__flush_str("Step 2 - construct network")), end="")
    for index in range(len(all_filepath_list)):
        with open(all_filepath_list[index], 'r+', encoding='utf-8', errors='ignore') as f:
            content = json.load(f)

        msg = __flush_str("Step 2 - construct network {:.2f}%: handle {}".format(
            (index + 1) * 100 / len(all_filepath_list),
            all_filepath_list[index]
        ))
        msg = ColorLogDecorator.yellow(msg)
        print("\r{}".format(msg), end="")
        location_counter = Counter(content["location"])
        location_list = location_counter.most_common()
        for i in range(len(location_list)):
            for j in range(i, len(location_list)):
                if i != j:
                    location1 = location_list[i]
                    location2 = location_list[j]
                    location1_num = location_counter[location1]
                    location2_num = location_counter[location2]
                    if location1_num < NUM_THRESHOLD:
                        continue
                    if abs(location1_num - location2_num) <= ABS_THRESHOLD:
                        if not graph.has_node(location1):
                            graph.add_node(location1)
                        if not graph.has_node(location2):
                            graph.add_node(location2)
                        if location1_num >= location2_num:
                            x = location1
                            y = location2
                        else:
                            x = location2
                            y = location1
                        graph.add_edge(x, y, weight=abs(location1_num - location2_num))
    print("\r" + ColorLogDecorator.yellow(__flush_str("Step 2 - construct network: Done")))

    # step 3: the result output
    print(ColorLogDecorator.yellow("Step 3 - output data in json"), end="")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, "location.json"), 'w+', encoding='utf-8', errors='ignore') as f:
        json.dump(json_graph.node_link_data(graph), f, ensure_ascii=False, indent=4)
    nx.draw_networkx(graph, node_size=5)
    plt.savefig(os.path.join(OUTPUT_DIR, "location.png"))
    print(ColorLogDecorator.yellow(": Done"))

    print(ColorLogDecorator.green("- ALL DONE -", "strong"))


if __name__ == '__main__':
    main()
