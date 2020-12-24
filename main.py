from typing import List, Tuple
from datetime import datetime
import argparse
import os
import shutil

from utils import (
    quit_with_error,
    get_list_of_relative_filepaths
)


OLD_FILE_DIRECTORY = '_old_'


def parse_arguments():
    """Parse arguments from console.

    Parse two arguments from console, source directory and
    destination directory paths and return them.

    Returns:
        Tuple(str): tuple consisting of source directory and
                    destination directory paths.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src_dir",
        type=str,
        help="Path to directory with files to back up.")
    parser.add_argument(
        "dst_dir",
        type=str,
        help="Path to directory to which save backed up files.")
    args = parser.parse_args()

    return args.src_dir, args.dst_dir


def make_old_filepath(filepath):
    dirpath = os.path.dirname(filepath)
    filename = os.path.split(filepath)[-1]
    now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    old_filename = f'{now}_{filename}'
    old_filepath = os.path.join(dirpath, OLD_FILE_DIRECTORY, old_filename)

    return old_filepath


def copy_file(src: str, dst: str):
    if not os.path.isdir(dirpath := os.path.dirname(dst)):
        os.makedirs(dirpath)

    try:
        shutil.copy2(src, dst)
    except FileNotFoundError as fnfe:
        print(fnfe)
        input('Press enter to skip...')
    except PermissionError as pe:
        print(pe)
        input('Press enter to skip...')


def make_backup(copy_from_dir: List[str],
                copy_to_dir: List[str],
                keep_existing: bool = False) -> None:
    relative_filepaths = get_list_of_relative_filepaths(copy_from_dir)

    if keep_existing:
        for rel_path in relative_filepaths:
            src = os.path.join(copy_to_dir, rel_path)
            dst = os.path.join(copy_to_dir, make_old_filepath(rel_path))

            if os.path.isfile(src):
                print(f'from {src} to {dst}')
                copy_file(src, dst)

    for rel_path in relative_filepaths:
        src = os.path.join(copy_from_dir, rel_path)
        dst = os.path.join(copy_to_dir, rel_path)

        print(f'from {src} to {dst}')
        copy_file(src, dst)


def check_dirs(src: str, dst: str):
    if not os.path.isdir(src):
        quit_with_error('Source directory does not exist.')

    if not os.access(src, os.W_OK):
        quit_with_error(f'Permission denied for: {src}')

    if not os.access(dst, os.W_OK):
        quit_with_error(f'Permission denied for: {dst}')


def create_dst_dir(dst: str):
    if not os.path.isdir(dst):
        try:
            os.mkdir(dst)
        except PermissionError as e:
            quit_with_error(f'Permission denied for: {dst}')


if __name__ == "__main__":
    src_dir, dst_dir = parse_arguments()

    create_dst_dir(dst_dir)
    check_dirs(src_dir, dst_dir)

    make_backup(src_dir, dst_dir, True)
