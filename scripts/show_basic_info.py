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
        infos.extend(basic_item_info(item))
    print('\n'.join(infos))


def basic_item_info(item: modo.Item) -> list[str]:
    str1 = f'<{item.name}>::<{item.id}>:<{item.type}>:{item=}'
    if item.parent:
        str2 = f'<{item.name}>::<{item.parent.name=}>:<{item.parent=}>'
    else:
        str2 = f'<{item.name}>::<{item.parent=}>'
    str3 = f'<{item.name}>::<{item.parentIndex=}>:<{item.rootIndex=}>:<{item.index=}>'

    return str1, str2, str3


if __name__ == '__main__':
    main()
