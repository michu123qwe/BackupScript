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
    relative_paths = utils.get_list_of_relative_filepaths(original_dirpath)
    
    original_filepaths = [os.path.join(original_dirpath, path) for path in relative_paths]
    backup_filepaths = [os.path.join(backup_dirpath, path) for path in relative_paths]
    
    # Print files that will be backed up.
    info.print_list_of_files_to_backup(original_filepaths)
    
    # Print proceed info and get consent from user to back up files.
    info.print_proceed_info()
    answer = input()
    
    if answer.lower() == 'y':
        current_size = 0
        size_sum = sum([os.path.getsize(path) for path in original_filepaths])
        
        for original_path, backup_path in zip(original_filepaths, backup_filepaths):
            # Create needed directories for this file.
            if not os.path.exists(os.path.dirname(backup_path)):
                os.makedirs(os.path.dirname(backup_path))
            
            backup.backup_file(original_path, backup_path)
            
            current_size += os.path.getsize(original_path)
            print(f'{original_path} saved! ', end='')
            info.print_size_state(current_size, size_sum)
            
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
