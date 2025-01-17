#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Output basic item info to Modo's Event Log
# ================================

import modo


def main():
    selected_items = modo.Scene().selected
    infos = []
    for item in selected_items:
        infos.append(basic_item_info(item))
    print('\n'.join(infos))


def basic_item_info(item: modo.Item) -> str:
    return f'{item.name} : {item.id} : {item.type} {item.parent=} {item.parentIndex=} {item.rootIndex=} {item.index=}>'


if __name__ == '__main__':
    main()
