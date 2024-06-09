#!/usr/bin/python
# ================================
# (C)2019 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# inspect selected item graphs
# ================================

import modo
from h3d_utilites.scripts.h3d_debug import H3dDebug
from h3d_utilites.scripts.h3d_utils import replace_file_ext


def inspect_graphs(items: list[modo.Item]):
    for item in items:
        h3dd.print_debug(f'{item.name=} {item.id=} {item.type=}')
        for graphname in item.itemGraphNames:
            h3dd.print_debug(f'{graphname=}', 1)
            for idx in item.itemGraph(graphname).connectedItems:
                h3dd.print_debug(f'{idx=}', 2)
                for item_detail in item.itemGraph(graphname).connectedItems[idx]:
                    h3dd.print_debug(f'{item_detail.name=}, {item_detail.type=}, {item_detail=}', 3)


def main():
    selected_items = modo.Scene().selected
    inspect_graphs(selected_items)


if __name__ == '__main__':
    h3dd = H3dDebug(enable=True, file=replace_file_ext(modo.Scene().filename, '_inspect.log'))
    main()
