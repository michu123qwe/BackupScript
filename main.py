import argparse
import os

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
    original_filepaths = [os.path.join(original_dirpath, path) for path in relative_filepaths]
    backup_filepaths = [os.path.join(backup_dirpath, path) for path in relative_filepaths]
    
    # Print files that will be backed up.
    info.print_relative_list_of_files_to_backup(relative_filepaths, original_dirpath)
    
    # Print proceed info and get consent from user to back up files.
    info.print_proceed_info()
    answer = input()
    
    if answer.lower() == 'y':
        size_of_copied_files = 0
        size_of_all_files = sum([os.path.getsize(path) for path in original_filepaths])
        
        for i in range(len(original_filepaths)):
            backup_path = backup_filepaths[i]
            original_path = original_filepaths[i]
            relative_path = relative_filepaths[i]
            
            # Create needed directories for this file.
            if not os.path.exists(os.path.dirname(backup_path)):
                os.makedirs(os.path.dirname(backup_path))
            
            backup.backup_file(original_path, backup_path)
            
            size_of_copied_files += os.path.getsize(original_path)
            size_state = info.formatted_size_state(size_of_copied_files, 
                                                   size_of_all_files)
            
            utils.clear_terminal()
            print(f'{size_state}\n{relative_path} saved!')
            
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
