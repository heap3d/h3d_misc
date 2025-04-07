#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# specify kits directory
# ================================

import modo

from h3d_utilites.scripts.h3d_utils import get_user_value, set_user_value

from scripts.kit_versions import USERVAL_NAME_KITS_PATH


def main():
    openpath = get_user_value(USERVAL_NAME_KITS_PATH)
    scanpath = modo.dialogs.dirBrowse('Specify Kits directory', openpath)
    if not scanpath:
        return
    set_user_value(USERVAL_NAME_KITS_PATH, scanpath)


if __name__ == '__main__':
    main()
