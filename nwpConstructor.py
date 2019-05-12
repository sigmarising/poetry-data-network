import os
import json
import settings
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from networkx.readwrite import json_graph
from module.ColorLogDecorator import ColorLogDecorator

INPUT_DIR = os.path.join(settings.INPUT_PATH, 'nerResult')
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, 'networkRaw')
COS_THRESHOLD = 0.8


def __flush_str(msg: str):
    fixed_len = 100
    if len(msg) <= fixed_len:
        return msg[0:fixed_len].ljust(fixed_len, ' ')
    else:
        return msg[0:fixed_len - 3] + "..."


def __calculate_cos(list1: list, list2: list):
    if not list1 or not list2:
        return 0.0

    space1 = list1
    space2 = list2
    space = list(set(space1 + space2))

    counter1 = Counter(space1)
    counter2 = Counter(space2)
    array1 = []
    array2 = []

    for item in space:
        if item in counter1:
            array1.append(counter1[item])
        else:
            array1.append(0)

        if item in counter2:
            array2.append(counter2[item])
        else:
            array2.append(0)

    vector1 = np.array(array1)
    vector2 = np.array(array2)
    cos_val = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    return cos_val


def main():
    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START -", "strong"))

    # the data structure
    all_filepath_list = []
    graph = nx.Graph()

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
    for i in range(len(all_filepath_list)):
        for j in range(i, len(all_filepath_list)):
            if i != j:
                with open(all_filepath_list[i], 'r+', encoding='utf-8', errors='ignore') as f1:
                    content1 = json.load(f1)
                with open(all_filepath_list[j], 'r+', encoding='utf-8', errors='ignore') as f2:
                    content2 = json.load(f2)

                node1 = content1["dynasty"] + " " + content1["author"]
                node2 = content2["dynasty"] + " " + content2["author"]

                msg = __flush_str("Step 2 - construct network {.2f}%: compare {} with {}".format(
                    (i + 1) * 100 / len(all_filepath_list),
                    node1,
                    node2)
                )
                msg = ColorLogDecorator.yellow(msg)
                print("\r{}".format(msg), end="")

                cos_val = __calculate_cos(content1["location"], content2["location"])
                if cos_val >= COS_THRESHOLD:
                    graph.add_node(node1)
                    graph.add_node(node2)
                    graph.add_edge(node1, node2, weight=cos_val)
    print("\r" + ColorLogDecorator.yellow(__flush_str("Step 2 - construct network: Done")))

    # step 3: the result output
    print(ColorLogDecorator.yellow("Step 3 - output data in json"), end="")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, "person.json"), 'w+', encoding='utf-8', errors='ignore') as f:
        json.dump(json_graph.node_link_data(graph), f, ensure_ascii=False, indent=4)
    nx.draw_networkx(graph, node_size=5, width=0.5)
    plt.savefig(os.path.join(OUTPUT_DIR, "person.png"))
    print(": Done")

    print(ColorLogDecorator.green("- ALL DONE -", "strong"))


if __name__ == '__main__':
    main()
