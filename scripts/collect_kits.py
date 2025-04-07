#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# collect a kits to export using the comparison results of the compare kits versions utility
# ================================

import os
import re
import shutil

import modo

from h3d_utilites.scripts.h3d_utils import get_user_value

from scripts.kit_versions import USERVAL_NAME_OUTPUT_PATH


EXPORT_DIR = 'Export'
PYCACHE = 'scripts/__pycache__'


def main():
    outputpath = get_user_value(USERVAL_NAME_OUTPUT_PATH)
    if not os.path.isdir(outputpath):
        outputpath, _ = os.path.split(outputpath)

    filepath = modo.dialogs.fileOpen('text', 'Select comparison to open', path=outputpath)
    if not filepath:
        return
    if isinstance(filepath, list):
        raise ValueError('Multiple files selected. Please select one file only.')

    exports: dict[str, str] = read_comparison(filepath)

    export_dir = os.path.join(outputpath, EXPORT_DIR)

    if exports:
        os.makedirs(export_dir, exist_ok=True)
    else:
        return

    for kit_name, kit_root in exports.items():
        export_kit(kit_root, os.path.join(export_dir, kit_name))


def read_comparison(path: str) -> dict[str, str]:
    with open(path) as file:
        lines = file.readlines()

    exports: dict[str, str] = dict()
    pattern = r"<export> +?<(.*?)>.+<(.*?)>"
    for line in lines:
        match = re.search(pattern, line)
        if not match:
            continue
        exports[match.group(1)] = (match.group(2))

    return exports


def export_kit(source_dir: str, dest_dir: str):
    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
    shutil.rmtree(os.path.join(dest_dir, PYCACHE), ignore_errors=True)


if __name__ == '__main__':
    main()
