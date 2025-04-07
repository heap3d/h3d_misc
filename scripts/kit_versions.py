#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Output kit versions
# ================================

import os
import datetime
import re
from typing import Iterable

import modo

from h3d_utilites.scripts.h3d_utils import TagSplit, get_user_value, set_user_value, show_in_explorer

TS = TagSplit

KitInfo = tuple[str, float, str]
KitsInfo = dict[str, KitInfo]


DATETIME_FORMAT = r'%Y-%m-%d %H:%M:%S'
CONFIG = 'index.CFG'
TAG_VERSION = 'version='
USERVAL_NAME_KITS_PATH = 'h3d_ckv_kits_dir'
USERVAL_NAME_OUTPUT_PATH = 'h3d_ckv_output_dir'


def main():
    scanpath = get_user_value(USERVAL_NAME_KITS_PATH)
    kits_info = scan_kits_info(scanpath)

    outputpath, _ = os.path.splitext(get_user_value(USERVAL_NAME_OUTPUT_PATH))
    filepath = modo.dialogs.fileSave('text', 'text', 'format', 'Save local kits version info', outputpath)
    if not filepath:
        return
    set_user_value(USERVAL_NAME_OUTPUT_PATH, filepath)
    write_kits_info(filepath, kits_info)

    print(f'Kits info successfully saved to {filepath}')
    show_in_explorer(filepath)


def scan_kits_info(path: str) -> KitsInfo:
    kits: KitsInfo = dict()
    for kitname in [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]:
        version, timestamp, root = get_kit_version(path, kitname)
        kits[kitname] = (version, timestamp, root)

    return kits


def write_kits_info(filepath: str, kits_info: KitsInfo):
    name_len = max((len(name) for name in kits_info))
    version_len = max((len(info[0]) for info in kits_info.values()))
    with open(filepath, 'w') as file:
        for kit, info in kits_info.items():
            mtime = datetime.datetime.fromtimestamp(info[1])
            name_sp = " " * (name_len - len(kit))
            ver_sp = " " * (version_len - len(info[0]))
            file.write(f'<{kit}>{name_sp}   <{info[0]}>{ver_sp}   <{mtime:{DATETIME_FORMAT}}>   <{info[2]}>\n')


def get_kit_version(kits_root: str, kit_name: str) -> KitInfo:
    ignores = ('__pycache__',)
    pattern = r'kit=\"(.*?)\" +version=\"(.*?)\"'
    filename = os.path.join(kits_root, kit_name, CONFIG)
    kit_root = os.path.join(kits_root, kit_name)

    maxmtime = 0
    for dirpath, _, files in os.walk(os.path.join(kits_root, kit_name)):
        if is_ignore(dirpath, ignores):
            continue
        for kitfile in files:
            mtime = os.path.getmtime(os.path.join(dirpath, kitfile))
            maxmtime = max(maxmtime, mtime)

    try:
        with open(filename) as file:
            lines = [i.strip() for i in file.readlines()]
            for line in lines:
                match = re.search(pattern, line)
                if match:
                    return (match.group(2), maxmtime, kit_root)

    except FileNotFoundError:
        return ('Unknown', maxmtime, kit_root)

    return ('None', maxmtime, kit_root)


def is_ignore(path: str, ignores: Iterable[str]):
    for ignore_str in ignores:
        if ignore_str in path:
            return True

    return False


if __name__ == '__main__':
    main()
