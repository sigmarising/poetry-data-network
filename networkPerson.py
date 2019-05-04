import os
import json
import settings
import networkx as nx
from collections import Counter
from module.ColorLogDecorator import ColorLogDecorator

INPUT_DIR = os.path.join(settings.INPUT_PATH, "nerResult")


def __test_xy():
    def __check(file_x, file_y):
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
                sum_common += counter_x[k] + counter_y[k]
            else:
                sum_uncommon += counter_x[k]

        for k in counter_y.keys():
            if k not in counter_x.keys():
                sum_uncommon += counter_y[k]

        common_str = raw_x["dynasty"] + "_" + raw_x["author"] + " and " + raw_y["dynasty"] + "_" + raw_y["author"]
        if sum_common > sum_uncommon:
            char = '>'
        elif sum_common < sum_uncommon:
            char = '<'
        else:
            char = '='
        msg = "common {2} uncommon: {0} {2} {1} in {3}".format(sum_common, sum_uncommon, char, common_str)
        if sum_uncommon != 0 and sum_common != 0 and char in ['>', '=']:
            print(ColorLogDecorator.blue(msg))

    files_list = os.listdir(INPUT_DIR)
    for i in range(0, len(files_list)):
        for j in range(i, len(files_list)):
            if not i == j:
                __check(files_list[i], files_list[j])


def main():
    ColorLogDecorator.active()
    __test_xy()


if __name__ == '__main__':
    main()
