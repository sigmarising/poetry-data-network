import os
import json
import settings
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from networkx.readwrite import json_graph
from module.ColorLogDecorator import ColorLogDecorator

INPUT_DIR = os.path.join(settings.INPUT_PATH, "nerResult")
OUTPUT_DIR = os.path.join(settings.OUTPUT_PATH, "personRaw")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def __check_sum(file_x_path, file_y_path):
    with open(file_x_path, 'r+', encoding='utf-8', errors='ignore') as f_x:
        raw_x = json.load(f_x)
    with open(file_y_path, 'r+', encoding='utf-8', errors='ignore') as f_y:
        raw_y = json.load(f_y)

    counter_x = Counter(raw_x["location"])
    counter_y = Counter(raw_y["location"])

    sum_common = 0
    sum_uncommon = 0

    for k in counter_x.keys():
        if k in counter_y.keys():
            sum_common += 1
        else:
            sum_uncommon += 1

    sum_uncommon += len(counter_y.keys()) - sum_common

    if sum_common >= sum_uncommon:
        return True, sum_common
    else:
        return False, 0


def __handle(author_list, files_path_list, dynasty):

    graph = nx.Graph()  # use to record the graph in this dynasty

    length = len(files_path_list)
    index = 0

    for i in range(length):

        index += 1
        msg = "Handling {0} - {1:.2f}% : {2}".format(dynasty, index * 100 / length, author_list[i])
        print(ColorLogDecorator.blue(msg))

        for j in range(i, length):

            if i != j:
                author1 = author_list[i]
                author2 = author_list[j]
                path1 = files_path_list[i]
                path2 = files_path_list[j]
                result, value = __check_sum(path1, path2)
                if result:
                    graph.add_edge(author1, author2, weight=value)

        output_path = os.path.join(OUTPUT_DIR, dynasty + ".json")
        with open(output_path, 'w+', encoding='utf-8', errors='ignore') as f:
            json.dump(json_graph.node_link_data(graph), f, ensure_ascii=False, indent=4)
        nx.draw_networkx(graph, node_size=10, width=0.5)
        plt.savefig(os.path.join(OUTPUT_DIR, dynasty + ".png"))


def main():
    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START -"))

    all_path_list = []  # record all the path in all dynasty
    all_author_list = []

    for dynasty in os.listdir(INPUT_DIR):  # handle all dynasty in single

        dynasty_path = os.path.join(INPUT_DIR, dynasty)
        files_list = os.listdir(dynasty_path)  # use to record the files in this dynasty
        author_list = []
        path_list = []

        for file in files_list:
            author = file.split('.')[0]
            path = os.path.join(dynasty_path, file)

            author_list.append(author)
            path_list.append(path)
            all_author_list.append(author)
            all_path_list.append(path)

        __handle(author_list, path_list, dynasty)

    # handle 汇总
    __handle(all_author_list, all_path_list, "汇总")

    print(ColorLogDecorator.green("- DONE -"))


if __name__ == '__main__':
    main()
