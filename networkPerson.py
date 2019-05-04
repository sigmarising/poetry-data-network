import os
import json
import settings
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from networkx.readwrite import json_graph
from module.ColorLogDecorator import ColorLogDecorator

INPUT_DIR = os.path.join(settings.INPUT_PATH, "nerResult")


def main():
    def __check_sum(file_x, file_y):
        file_x_path = os.path.join(INPUT_DIR, file_x)
        file_y_path = os.path.join(INPUT_DIR, file_y)

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

        for k in counter_y.keys():
            if k not in counter_x.keys():
                sum_uncommon += 1

        if sum_common >= sum_uncommon:
            return True, sum_common
        else:
            return False, 0

    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START -"))

    graph = nx.Graph()
    files_list = os.listdir(INPUT_DIR)
    for i in range(0, len(files_list)):
        print(ColorLogDecorator.blue("Handling: {}".format(files_list[i])))
        for j in range(i, len(files_list)):
            if i != j:
                result, value = __check_sum(files_list[i], files_list[j])
                if result:
                    author1 = files_list[i].split('.')[0]
                    author2 = files_list[j].split('.')[0]
                    graph.add_edge(author1, author2, weight=value)

    output_path = os.path.join(settings.OUTPUT_PATH, "person")
    with open(os.path.join(output_path, "result.json"), 'w+', encoding='utf-8', errors='ignore') as f:
        json.dump(json_graph.node_link_data(graph), f, ensure_ascii=False, indent=4)

    nx.draw_networkx(graph, node_size=10, width=0.5)
    plt.savefig(os.path.join(output_path, "testResult.png"))

    print(ColorLogDecorator.green("- DONE -"))


if __name__ == '__main__':
    main()
