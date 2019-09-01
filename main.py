import os
import backup
import utils.utils as utils
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("backup_folder", type=str, help="Folder with backup files")
parser.add_argument("new_folder", type=str, help="Folder with files to be backed up")
args = parser.parse_args()

BACKUPPATH = args.backup_folder
NEWPATH = args.new_folder

# try to open backup folder
if not os.path.isdir(BACKUPPATH):
    print("Cannot open {}".format(BACKUPPATH))
    input("Click enter to exit...")
    quit()

# try to open new folder
if not os.path.isdir(NEWPATH):
    print("Cannot open {}".format(NEWPATH))
    input("Click enter to exit...")
    quit()

files_new, files_different, files_move, files_directory = backup.list_backup(BACKUPPATH, NEWPATH)

if len(files_new) + len(files_directory) + len(files_move) + len(files_different) == 0:
    print("Backup folder is up to date.")
    input("Click enter to exit...")
    quit()

if len(files_new) > 0:
    print("\nNew files:")
    utils.print_files_list(files_new)

if len(files_directory) > 0:
    print("\nFolders for old versions:")
    for path in files_directory:
        print("Create {}".format(path))

if len(files_move) > 0:
    print("\nMove old versions:")
    utils.print_files_list(files_move)

if len(files_different) > 0:
    print("\nDifferent files:")
    utils.print_files_list(files_different)

ans = input("\nProceed?(y/n) ")
if ans.lower() == "y":
    backup.make_backup(files_new, files_different, files_directory, files_move)
else:
    print("Goodbye")
    quit()


