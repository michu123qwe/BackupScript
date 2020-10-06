import argparse
import os
from typing import Tuple, List

from engine import utils
from engine import backup


def parse_arguments() -> Tuple[str, str]:
    """Parse arguments from console.

    Parse two arguments from console, original directory and
    backup directory paths. Return them.

    @return: original directory path and backup directory path.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "original_directory",
        type=str,
        help="Path to directory with files to back up.")
    parser.add_argument(
        "backup_directory",
        type=str,
        help="Path to directory to which save backed up files.")
    args = parser.parse_args()

    return args.original_directory, args.backup_directory


def check_directories(directories: List[str]) -> Tuple[bool, str]:
    """Check if directories exist and if user has permissions to
    work with them.

    @param directories: list of directories to check
    @return: Status whether user can use given directories (True) or
    not (False) and error message or empty string if message
    is not specified.
    """

    for directory in directories:
        if not os.path.isdir(directory):
            # Given directory argument is not a directory.
            return False, f'"{directory}" is not a directory.'
        if not os.access(directory, os.W_OK):
            # User doesn't have permission to use this directory.
            return False, f'Permission denied for: {directory}'

    return True, ''


def make_backup(original_dirpath: str, backup_dirpath: str) -> bool:
    """Perform backup.

    Main backup function. It lists all files to be copied, asks for
    consent to perform backup, and copies all files to backup_dirpath
    preserving the same file and directory tree.

    @param original_dirpath: path to directory with files to back-up,
    @param backup_dirpath: path to directory to save files.
    @return: True if backup was performed without errors, False if
    there was not consent to perform back-up.
    """

    single_file_backups = backup.parse_backup_objects(
        original_dirpath, backup_dirpath)
    size_sum = sum([obj.get_size() for obj in single_file_backups])

    utils.print_backup_objects(
        single_file_backups, size_sum=size_sum, files_limit=50)
    utils.print_proceed_info()
    answer = input()

    if answer.lower() == 'y':
        size_copied = 0
        for obj in single_file_backups:
            utils.clear_terminal()
            size_state = utils.formatted_size_state(size_copied, size_sum)
            print(f'{size_state}\nCopying:\n{obj}')

            obj.make_backup()
            size_copied += obj.get_size()

        utils.clear_terminal()
        print(utils.formatted_size_state(size_copied, size_sum))
        print(utils.colored('Backup finished!', 'green'))

        return True
    else:
        return False


if __name__ == "__main__":
    original_dirpath, backup_dirpath = parse_arguments()

    if not os.path.isdir(backup_dirpath):
        # Backup directory doesn't exist, create it.
        try:
            os.mkdir(backup_dirpath)
        except PermissionError as e:
            # User doesn't have permission to use given backup_dirpath.
            utils.quit_with_error(f'Permission denied for: {backup_dirpath}')

    status, message = check_directories([original_dirpath, backup_dirpath])
    if not status:
        utils.quit_with_error(message)

    make_backup(original_dirpath, backup_dirpath)
