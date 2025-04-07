#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# specify output directory
# ================================

import modo

from h3d_utilites.scripts.h3d_utils import get_user_value, set_user_value

from scripts.kit_versions import USERVAL_NAME_OUTPUT_PATH


def main():
    openpath = get_user_value(USERVAL_NAME_OUTPUT_PATH)
    outputpath = modo.dialogs.fileOpen('text', 'Select local kits version info file', path=openpath)
    if not outputpath:
        return
    set_user_value(USERVAL_NAME_OUTPUT_PATH, outputpath)


if __name__ == '__main__':
    main()
