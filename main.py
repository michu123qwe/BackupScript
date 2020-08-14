import argparse
import os
import shutil

import backup
import utils
import info


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
    backups = []
    
    for rel_filepath in relative_filepaths:
        original_filepath = os.path.join(original_dirpath, rel_filepath)
        backup_filepath = os.path.join(backup_dirpath, rel_filepath)
        old_version_dirpath = backup.get_dirpath_for_old_versions(backup_filepath)
        old_version_filepath = os.path.join(old_version_dirpath, backup.get_filename_for_old_version(backup_filepath))
        
        backup_object = backup.SingleFileBackup(
            original_filepath,
            backup_filepath,
            old_version_dirpath,
            old_version_filepath
        )
        backups.append(backup_object)
    
    for i in range(min(len(backups), 50)):
        print(backups[i])
        
    remaining = len(backups) - 50
    if remaining > 0:
        print(f'...and {remaining} more.')
    
    size_sum = sum([obj.get_size() for obj in backups])
    print('Size:', utils.format_size(size_sum))
    
    info.print_proceed_info()
    answer = input()
    
    if answer.lower() == 'y':
        size_copied = 0
        for obj in backups:
            obj.make_backup()
            
            size_copied += obj.get_size()
            utils.clear_terminal()
            size_state = info.formatted_size_state(size_copied, size_sum)
            print(f'{size_state}\n{obj.original_filepath} saved!')
            
        return True
    else:
        return False
    

if __name__ == "__main__":
    original_dirpath, backup_dirpath = parse_arguments()
    
    assert os.path.isdir(original_dirpath)
    if not os.path.isdir(backup_dirpath):
        # Backup dir doesn't exist, create it.
        os.mkdir(backup_dirpath)
    
    make_backup(original_dirpath, backup_dirpath)
