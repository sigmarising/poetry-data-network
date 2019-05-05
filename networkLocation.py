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
    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START -"))

    graph = nx.Graph()
    for file in os.listdir(INPUT_DIR):
        print(ColorLogDecorator.blue("Handling: {}".format(file)))
        file_path = os.path.join(INPUT_DIR, file)
        with open(file_path, 'r+', encoding='utf-8', errors='ignore') as f:
            raw = json.load(f)
            location = list(set(raw["location"]))
            for i in range(len(location)):
                for j in range(i, len(location)):
                    if i != j:
                        graph.add_edge(location[i], location[j])

    output_path = os.path.join(settings.OUTPUT_PATH, "location")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(os.path.join(output_path, "result.json"), 'w+', encoding='utf-8', errors='ignore') as f:
        json.dump(json_graph.node_link_data(graph), f, ensure_ascii=False, indent=4)

    nx.draw_networkx(graph, node_size=10, width=0.5)
    plt.savefig(os.path.join(output_path, "testResult.png"))

    print(ColorLogDecorator.green("- DONE -"))


if __name__ == '__main__':
    main()
