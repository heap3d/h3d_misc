#!/usr/bin/python
# ================================
# (C)2019 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# inspect selected item graphs
# ================================

import modo
from h3d_utilites.scripts.h3d_debug import h3dd, prints, replace_file_ext

INSPECT_LOG = '_inspect.log'


def inspect_graphs(items: list[modo.Item]):
    for item in items:
        prints(f'{item.name=} {item.id=} {item.type=}')
        for graphname in item.itemGraphNames:
            prints(f'{graphname=}', 1)
            for idx in item.itemGraph(graphname).connectedItems:
                prints(f'{idx=}', 2)
                for item_detail in item.itemGraph(graphname).connectedItems[idx]:
                    prints(f'{item_detail.name=}, {item_detail.type=}, {item_detail=}', 3)


def main():
    selected_items = modo.Scene().selected
    inspect_graphs(selected_items)


if __name__ == '__main__':
    if not h3dd.log_path.endswith(INSPECT_LOG):
        h3dd.log_path = replace_file_ext(h3dd.log_path, INSPECT_LOG)
    h3dd.enable_debug_output()
    main()
