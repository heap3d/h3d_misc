#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# Compare kit versions (file in kits directory vs specified file)
# ================================

import os
import re
import time
import datetime
import subprocess
from dataclasses import dataclass

import modo

from h3d_utilites.scripts.h3d_utils import get_user_value, set_user_value

from scripts.kit_versions import KitInfo, KitsInfo, DATETIME_FORMAT, USERVAL_NAME_OUTPUT_PATH


USERVAL_NAME_COMPARISON_PATH = 'h3d_ckv_comp_dir'
EXPORT = 'export'
IMPORT = 'import'
OK = 'OK'
VERSION_UNKNOWN = 'Unknown'
VERSION_NONE = 'None'


@dataclass
class KitComparison:
    action = ''
    kit_local: KitInfo
    kit_comparable: KitInfo
    kit_local_root = ''
    kit_comparable_root = ''


def main():
    local_filepath = get_user_value(USERVAL_NAME_OUTPUT_PATH)
    if not os.path.isfile(local_filepath) or not os.path.exists(local_filepath):
        modo.dialogs.alert('Local kits info not found', 'Specify local kits info file first')
        return

    kits_info_local = read_kits_info(local_filepath)

    COMPARISON_PATH = get_user_value(USERVAL_NAME_COMPARISON_PATH)
    comparable_filepath = modo.dialogs.fileOpen(
        'text', title='Select comparable kit info to load', path=COMPARISON_PATH)
    if not comparable_filepath:
        return
    if isinstance(comparable_filepath, list):
        raise ValueError('Multiple files selected. Please select one file only.')
    set_user_value(USERVAL_NAME_COMPARISON_PATH, comparable_filepath)

    kits_info_comparable = read_kits_info(comparable_filepath)

    comparison = compare_kits(kits_info_local, kits_info_comparable)

    local_filename = os.path.splitext(os.path.split(local_filepath)[1])[0]
    comparable_filename = os.path.splitext(os.path.split(comparable_filepath)[1])[0]
    filename = f'{local_filename} vs {comparable_filename}.txt'
    filepath = os.path.join(os.path.split(local_filepath)[0], filename)
    write_comparison(filepath, comparison)

    print(f'Comparison successfully saved to {filepath}')
    subprocess.Popen(f'explorer /select,"{filepath}"')


def read_kits_info(filepath: str) -> KitsInfo:
    kits_info: KitsInfo = dict()
    with open(filepath) as file:
        lines = [line.strip() for line in file.readlines()]
    for line in lines:
        name, kit_info = get_kit_info(line)
        if not name:
            continue
        kits_info[name] = kit_info

    if not kits_info:
        raise ValueError(f'Error reading kits info from the file {filepath}')
    return kits_info


def compare_kits(kits_local: KitsInfo, kits_comparable: KitsInfo) -> dict[str, KitComparison]:
    if not kits_local:
        raise ValueError('Kits local not provided.')
    if not kits_comparable:
        raise ValueError('Kits comparable not provided.')

    comparison: dict[str, KitComparison] = dict()

    for name in kits_local:
        comparison[name] = KitComparison(('Unknown', 0, ''), ('Unknown', 0, ''))

        if name not in kits_comparable:
            comparison[name].action = EXPORT
            comparison[name].kit_local = kits_local[name]
            comparison[name].kit_comparable = ('None', 0, '')
            continue

        if kits_local[name][0] > kits_comparable[name][0]:
            comparison[name].action = EXPORT
            comparison[name].kit_local = kits_local[name]
            comparison[name].kit_comparable = kits_comparable[name]
            continue
        if kits_local[name][0] < kits_comparable[name][0]:
            comparison[name].action = IMPORT
            comparison[name].kit_local = kits_local[name]
            comparison[name].kit_comparable = kits_comparable[name]
            continue

        if float(kits_local[name][1]) > float(kits_comparable[name][1]):
            comparison[name].action = EXPORT
            comparison[name].kit_local = kits_local[name]
            comparison[name].kit_comparable = kits_comparable[name]
            continue
        if float(kits_local[name][1]) < float(kits_comparable[name][1]):
            comparison[name].action = IMPORT
            comparison[name].kit_local = kits_local[name]
            comparison[name].kit_comparable = kits_comparable[name]
            continue

        comparison[name].action = OK
        comparison[name].kit_local = kits_local[name]
        comparison[name].kit_comparable = kits_comparable[name]

    for name in kits_comparable:
        if name not in kits_local:
            comparison[name] = KitComparison(('Unknown', 0, ''), ('Unknown', 0, ''))
            comparison[name].action = IMPORT
            comparison[name].kit_local = ('None', 0, '')
            comparison[name].kit_comparable = kits_comparable[name]
            continue

    return comparison


def write_comparison(filepath: str, comparison: dict[str, KitComparison]):
    act_len = max(len(i) for i in (EXPORT, IMPORT, OK))
    name_len = max(len(i) for i in comparison)
    ver_loc_len = max(len(i.kit_local[0]) for i in comparison.values())
    ver_comp_len = max(len(i.kit_comparable[0]) for i in comparison.values())

    with open(filepath, 'w') as file:
        MTIME_LEN = 19
        for kit, info in comparison.items():
            act = info.action
            v_loc = info.kit_local[0] if info.kit_local[0] != VERSION_NONE else ''
            v_comp = info.kit_comparable[0] if info.kit_comparable[0] != VERSION_NONE else ''

            act_s = f'<{act}>{" " * (act_len - len(act))}'
            kit_s = f'<{kit}>{" " * (name_len - len(kit))}'
            ver_s = f'{v_loc:{ver_loc_len}}   {v_comp:{ver_comp_len}}'

            if info.kit_local[1] != 0:
                mtime_loc = datetime.datetime.fromtimestamp(info.kit_local[1])
            else:
                mtime_loc = ''

            if info.kit_comparable[1] != 0:
                mtime_comp = datetime.datetime.fromtimestamp(info.kit_comparable[1])
            else:
                mtime_comp = ''

            root = ''
            if info.action == EXPORT:
                root = info.kit_local[2]
            if info.action == IMPORT:
                root = info.kit_comparable[2]
            if root:
                root_s = f'<{root}>'
            else:
                root_s = ''

            mtime = f'{str(mtime_loc):{MTIME_LEN}}   {str(mtime_comp):{MTIME_LEN}}'

            file.write(f'{act_s}   {kit_s}   {ver_s}   {mtime}   {act_s}   {root_s}\n')


def get_kit_info(line: str) -> tuple[str, KitInfo]:
    pattern = r"<(.*?)> +?<(.*?)> +?<(.*?)> +?<(.*?)>"
    match = re.search(pattern, line)

    if not match:
        return ('', KitInfo(('None', 0, '')))

    name = match[1]

    version = match[2]
    if not version:
        version = VERSION_UNKNOWN

    timestamp = time.mktime(datetime.datetime.strptime(match[3], DATETIME_FORMAT).timetuple())

    kitroot = match[4]

    kit_info: KitInfo = (version, timestamp, kitroot)
    return (name, kit_info)


if __name__ == '__main__':
    main()
