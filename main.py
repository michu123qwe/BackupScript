import argparse
import os
import shutil

from engine import utils
from engine import backup


def parse_arguments():
    """Parse arguments from console.
    
    Parse two arguments from console, original directory and
    backup directory paths and return them.

    Returns:
        Tuple(str): tuple consisting of original directory and
                    backup directory paths.
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


def make_backup(original_dirpath, backup_dirpath):
    """Perform backup.
    
    Main backup function. It lists all files to be copied, asks for
    consent to perform backup, and copies all files to backup_dirpath
    preserving the same file and directory tree.

    Args:
        original_dirpath (str): path to directory with files to back-up,
        backup_dirpath (str): path to directory to save files.

    Returns:
        bool: True if backup was performed without errors, False if 
              there was not consent to perform back-up.
    """
    
    relative_filepaths = utils.get_list_of_relative_filepaths(original_dirpath)
    backups = backup.parse_backup_objects(
        relative_filepaths, original_dirpath, backup_dirpath)
    
    size_sum = sum([obj.get_size() for obj in backups])
    utils.print_backup_objects(backups, size_sum=size_sum, files_limit=50)
    
    utils.print_proceed_info()
    answer = input()
    
    if answer.lower() == 'y':
        size_copied = 0
        for obj in backups:
            utils.clear_terminal()
            size_state = utils.formatted_size_state(size_copied, size_sum)
            print(f'{size_state}\nCopying:\n{obj}')
            
            obj.make_backup()
            size_copied += obj.get_size()
            
        return True
    else:
        return False
    

if __name__ == "__main__":
    original_dirpath, backup_dirpath = parse_arguments()
    
    if not os.path.isdir(original_dirpath):
        # Given original_dirpath argument is not a directory.
        print(utils.colored('First argument is not a directory.', 'red'))
        quit()

    if not os.path.isdir(backup_dirpath):
        # Backup dir doesn't exist, create it.
        os.mkdir(backup_dirpath)
    
    make_backup(original_dirpath, backup_dirpath)
