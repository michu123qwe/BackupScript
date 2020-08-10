import argparse
import os

import backup
import utils
import info


def parse_arguments():
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


if __name__ == "__main__":
    original_path, backup_path = parse_arguments()
    filepaths_to_backup = utils.get_list_of_filepaths(original_path)
    
    info.print_list_of_files_to_backup(filepaths_to_backup)

    ans = input("\nProceed?(y/n) ")
    if ans.lower() == "y":
        backup.backup_directory(original_path, backup_path)
    else:
        print("Goodbye")
        quit()
